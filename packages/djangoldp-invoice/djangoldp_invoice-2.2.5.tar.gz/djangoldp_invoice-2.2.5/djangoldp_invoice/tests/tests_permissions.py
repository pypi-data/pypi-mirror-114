import uuid

from rest_framework.test import APITestCase, APIClient

from djangoldp_project.models import Project, Member
from djangoldp_invoice.models import Batch, CustomerInvoice
from djangoldp_invoice.tests.models import User


class PermissionsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def setUpLoggedInUser(self):
        self.user = User(email='test@mactest.co.uk', first_name='Test', last_name='Mactest', username='test',
                         password='glass onion')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def _get_random_project(self):
        return Project.objects.create(name=str(uuid.uuid4()), status='Public')

    def _get_random_customer_invoice(self, project=None, customer=None):
        return CustomerInvoice.objects.create(project=project, customer=customer, identifier=str(uuid.uuid4()),
                                              title=str(uuid.uuid4()), tvaRate=20)

    def _get_random_batch(self, customer_invoice):
        return Batch.objects.create(invoice=customer_invoice, title=str(uuid.uuid4()))

    def _get_random_user(self):
        return User.objects.create(email='{}@test.co.uk'.format(str(uuid.uuid4())), first_name='Test', last_name='Test',
                                   username=str(uuid.uuid4()))

    # accessing the invoices directly - whether anonymous or authenticated, should return empty list
    def test_list_invoices_anonymous_user(self):
        self._get_random_customer_invoice()

        response = self.client.get('/customer-invoices/')
        self.assertEqual(response.status_code, 403)

    # accessing the invoices directly - whether anonymous or authenticated, should return empty list
    def test_list_invoices_authenticated(self):
        self.setUpLoggedInUser()
        self._get_random_customer_invoice()

        response = self.client.get('/customer-invoices/')
        self.assertEqual(response.status_code, 403)

    # accessing in a nested object (project) is OK if I am authenticated
    def test_list_invoice_nested_in_project_anonymous(self):
        project = self._get_random_project()
        self._get_random_customer_invoice(project=project)

        response = self.client.get('/projects/{}/customerInvoices/'.format(project.pk))
        self.assertEqual(response.status_code, 403)

    # accessing in a nested object (project) is OK if I am authenticated
    def test_list_invoice_nested_in_project_authenticated(self):
        self.setUpLoggedInUser()
        project = self._get_random_project()
        self._get_random_customer_invoice(project=project)

        response = self.client.get('/projects/{}/customerInvoices/'.format(project.pk))
        self.assertEqual(response.status_code, 200)
        self.assertIn('ldp:contains', response.data)
        self.assertEqual(len(response.data['ldp:contains']), 1)

    def test_get_invoice_anonymous_user(self):
        invoice = self._get_random_customer_invoice()

        response = self.client.get('/customer-invoices/{}/'.format(invoice.pk))
        self.assertEqual(response.status_code, 403)

    def test_get_invoice_authenticated(self):
        self.setUpLoggedInUser()
        invoice = self._get_random_customer_invoice()

        response = self.client.get('/customer-invoices/{}/'.format(invoice.pk))
        self.assertEqual(response.status_code, 200)

    def test_get_invoice_batches_anonymous(self):
        invoice = self._get_random_customer_invoice()
        self._get_random_batch(invoice)

        response = self.client.get('/customer-invoices/{}/batches/'.format(invoice.pk))
        self.assertEqual(response.status_code, 200)

    # TODO: https://git.startinblox.com/djangoldp-packages/djangoldp-invoice/issues/11
    def test_get_invoice_batches_authenticated(self):
        self.setUpLoggedInUser()
        invoice = self._get_random_customer_invoice()
        self._get_random_batch(invoice)

        response = self.client.get('/customer-invoices/{}/batches/'.format(invoice.pk))
        self.assertEqual(response.status_code, 200)
