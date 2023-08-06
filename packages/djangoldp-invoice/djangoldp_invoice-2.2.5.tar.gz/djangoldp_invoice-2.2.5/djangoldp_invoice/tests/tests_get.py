import uuid
from rest_framework.test import APIRequestFactory, APIClient, APITestCase

from djangoldp_project.models import Project, Member
from djangoldp_invoice.models import CustomerInvoice
from djangoldp_invoice.tests.models import User


class TestGET(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
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

    def test_get_invoices_nested_field_on_project(self):
        '''
        GET as nested field in Project, and assert that customerInvoices and freelanceInvoices are included as a
        nested field on this model
        '''
        self.setUpLoggedInUser()
        project = self._get_random_project()
        self._get_random_customer_invoice(project=project)

        response = self.client.get('/projects/{}/'.format(project.pk))
        self.assertEqual(response.status_code, 200)
        self.assertIn('customerInvoices', response.data)
        self.assertIn('freelancerInvoices', response.data)
        self.assertEqual(len(response.data['customerInvoices']['ldp:contains']), 1)
        self.assertEqual(len(response.data['freelancerInvoices']['ldp:contains']), 0)
