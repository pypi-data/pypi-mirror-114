import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.utils import json

from djangoldp_project.models import Project, Member
from djangoldp_invoice.models import Task, Batch, FreelanceInvoice, CustomerInvoice


class TestUpdate(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='john', email='jlennon@beatles.com',
                                                         password='glass onion')
        self.client.force_authenticate(user=self.user)

    def _get_random_project(self):
        return Project.objects.create(name=str(uuid.uuid4()), status='Public')

    def _get_random_customer_invoice(self, project=None, customer=None):
        return CustomerInvoice.objects.create(project=project, customer=customer, identifier=str(uuid.uuid4()),
                                              title=str(uuid.uuid4()), tvaRate=20)
    
    def _get_random_batch(self, customer_invoice):
        return Batch.objects.create(invoice=customer_invoice, title=str(uuid.uuid4()))

    def _get_random_task(self, batch):
        return Task.objects.create(batch=batch, title=str(uuid.uuid4()), htAmount=20)

    # changing existing CustomerInvoice.batch.task
    def test_update_customer_invoice_batch_edit_task(self):
        invoice = self._get_random_customer_invoice()
        batch = self._get_random_batch(customer_invoice=invoice)
        task = self._get_random_task(batch=batch)

        body = {
            "title":"facture géniale 1",
            "identifier":"FR-3463-2021",
            "state":"pending",
            "invoicingDate":"2021-04-19",
            "batches": {
                "ldp:contains": [
                    {
                        "@id": batch.urlid,
                        "title":"Lot 1.1",
                        "tasks": {
                            "ldp:contains": [
                            {
                                "title":"tache 1.1",
                                "htAmount":580,
                                "@id": task.urlid
                            }
                        ]},
                    }
                ],
            },
            "tvaRate":20,
            "additionalText":"Test",
            "@id": invoice.urlid,
            "@context":{
                "@vocab":"http://happy-dev.fr/owl/#",
                "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "rdfs":"http://www.w3.org/2000/01/rdf-schema#",
                "ldp":"http://www.w3.org/ns/ldp#",
                "foaf":"http://xmlns.com/foaf/0.1/",
                "name":"rdfs:label",
                "acl":"http://www.w3.org/ns/auth/acl#",
                "permissions":"acl:accessControl",
                "mode":"acl:mode",
                "geo":"http://www.w3.org/2003/01/geo/wgs84_pos#",
                "lat":"geo:lat",
                "lng":"geo:long"
            }
        }

        # changes to Invoice
        response = self.client.put('/customer-invoices/{}/'.format(invoice.pk), data=json.dumps(body), content_type='application/ld+json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "facture géniale 1")
        self.assertEqual(response.data['identifier'], "FR-3463-2021")
        self.assertEqual(response.data['state'], "pending")
        self.assertEqual(response.data['invoicingDate'], "2021-04-19")
        self.assertEqual(response.data['tvaRate'], '20.00')
        self.assertEqual(response.data['additionalText'], "Test")

        # changes to Batch
        self.assertIn('batches', response.data)
        self.assertIs(len(response.data['batches']['ldp:contains']), 1)
        batches = invoice.batches.all()
        self.assertEquals(batches.count(), 1)
        self.assertEquals(batches[0].title, "Lot 1.1")
        
        # changes to Task
        tasks = batch.tasks.all()
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(tasks[0].title, "tache 1.1")
