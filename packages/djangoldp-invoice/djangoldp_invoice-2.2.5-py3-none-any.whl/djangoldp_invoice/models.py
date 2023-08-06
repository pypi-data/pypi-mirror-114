# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum

from djangoldp.models import Model
from djangoldp_project.models import Customer, Project
from djangoldp_invoice.views import InvoiceLDPViewSet


class FreelanceInvoice(Model):
    STATES = (
        ('edited', 'édité'),
        ('pending', 'en attente'),
        ('sent', 'envoyé'),
        ('late', 'en retard'),
        ('paid', 'payé')
    )
    TVA_RATES = (
        (0.0, 'exonération de TVA'),
        (20.0, '20%')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="freelancerInvoices", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices", null=True, blank=True)
    freelanceFullname = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Titre facture")
    state = models.CharField(max_length=255, choices=STATES, default='pending')
    htAmount = models.DecimalField(max_digits=11, decimal_places=2)
    tvaRate = models.DecimalField(choices=TVA_RATES, max_digits=4, decimal_places=2, default=20.0)
    uploadUrl = models.URLField(blank=True, null=True)
    creationDate = models.DateField(auto_now_add=True)
    modificationDate = models.DateField(auto_now=True)
    invoicingDate = models.DateField(default=datetime.date.today)

    class Meta(Model.Meta):
        container_path = "freelance-invoices/"
        rdf_type = "sib:Invoice"
        view_set = InvoiceLDPViewSet
        anonymous_perms = []
        authenticated_perms = ['inherit', 'view', 'add', 'change', 'delete']
        owner_perms = ['inherit', 'delete', 'control']

    def __str__(self):
        return '{} ({} / {})'.format(self.freelanceFullname, self.identifier, self.title)


class CustomerInvoice(Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="customerInvoices", null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices", null=True, blank=True)
    STATES = (
        ('edited', 'édité'),
        ('pending', 'en attente'),
        ('sent', 'envoyé'),
        ('late', 'en retard'),
        ('paid', 'payé')
    )
    identifier = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=STATES, default='pending')
    tvaRate = models.DecimalField(max_digits=4, decimal_places=2)
    creationDate = models.DateField(auto_now_add=True)
    modificationDate = models.DateField(auto_now=True)
    invoicingDate = models.DateField(default=datetime.date.today)
    additionalText = models.CharField(max_length=255, blank=True, null=True)

    def htAmount(self):
        amount = Task.objects.filter(batch__invoice = self).aggregate(total=Sum('htAmount'))['total']
        if amount is None:
            amount = Decimal(0.0)
        return amount

    def tvaAmount(self):
        return Decimal(self.tvaRate * self.htAmount() / Decimal(100))

    def ttcAmount(self):
        return Decimal(self.tvaAmount() + self.htAmount())

    class Meta(Model.Meta):
        container_path = "customer-invoices/"
        serializer_fields = ["@id", "identifier", "title", "state", "htAmount", "tvaRate", "invoicingDate",
                             "tvaAmount", "ttcAmount", "batches", "additionalText", "project", "customer"]
        rdf_type = "sib:Invoice"
        view_set = InvoiceLDPViewSet
        anonymous_perms = []
        authenticated_perms = ['inherit', 'view', 'add', 'change', 'delete']
        owner_perms = ['inherit', 'delete', 'control']

    def __str__(self):
        return '{} - {} ({})'.format(self.identifier, self.title, self.htAmount())


# Lot =========================================================
class Batch(Model):
    invoice = models.ForeignKey(CustomerInvoice, on_delete=models.CASCADE, related_name='batches')
    title = models.CharField(max_length=255)
    creationDate = models.DateField(auto_now_add=True)
    modificationDate = models.DateField(auto_now=True)

    class Meta(Model.Meta):
        serializer_fields = ['@id', 'title', 'htAmount', 'tasks']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'change', 'delete']
        owner_perms = ['inherit', 'control']

    def __str__(self):
        return '{} - {} ({} € HT)'.format(self.invoice.title, self.title, self.htAmount())

    def htAmount(self):
        amount = self.tasks.all().aggregate(total=Sum('htAmount'))['total']
        if amount is None:
            amount = Decimal(0.0)
        return amount


class Task(Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='tasks')
    title = models.TextField()
    htAmount = models.DecimalField(max_digits=11, decimal_places=2)
    creationDate = models.DateField(auto_now_add=True)
    modificationDate = models.DateField(auto_now=True)

    class Meta(Model.Meta):
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'change', 'delete']
        owner_perms = ['inherit', 'control']

    def __str__(self):
        return '{} - {} ({} € HT)'.format(self.batch.title, self.title, self.htAmount)

class Term(Model):
    org_name = models.CharField(max_length=50)
    org_logo_url = models.URLField(max_length=200, blank=True)
    org_address = models.TextField()
    org_siret = models.CharField(max_length=50)
    org_status = models.CharField(max_length=50)
    org_vat_number = models.CharField(max_length=20, blank=True)
    vat_rule = models.CharField(max_length=40, blank=True)
    gcs = models.URLField(max_length=200, blank=True)
    bank_bic = models.CharField(max_length=20)
    bank_iban = models.CharField(max_length=20)
    overdue = models.TextField(blank=True)

    class Meta(Model.Meta):
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'change', 'delete']
        owner_perms = ['inherit', 'control']

    def __str__(self):
        return self.org_name

