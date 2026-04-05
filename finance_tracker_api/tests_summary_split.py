from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Transaction

class SummarySplitTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(username='admin', password='password', role='Admin')
        self.analyst = CustomUser.objects.create_user(username='analyst', password='password', role='Analyst')
        self.viewer = CustomUser.objects.create_user(username='viewer', password='password', role='Viewer')
        
        # Create a transaction for viewer
        Transaction.objects.create(
            user=self.viewer, amount=100.00, transaction_type='Income', category='Salary', date='2024-01-01'
        )
        # Create a transaction for admin
        Transaction.objects.create(
            user=self.admin, amount=500.00, transaction_type='Income', category='Investments', date='2024-01-01'
        )

    def test_personal_summary_by_default(self):
        self.client.login(username='viewer', password='password')
        url = reverse('summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see own 100.00
        self.assertEqual(float(response.data['total_income']), 100.00)
        self.assertNotIn('total_users', response.data)

    def test_global_summary_access_analyst(self):
        self.client.login(username='analyst', password='password')
        url = reverse('summary')
        response = self.client.get(url, {'global': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should see sum of all (100 + 500 = 600)
        self.assertEqual(float(response.data['total_income']), 600.00)
        self.assertEqual(response.data['total_users'], 3)

    def test_global_summary_access_admin(self):
        self.client.login(username='admin', password='password')
        url = reverse('summary')
        response = self.client.get(url, {'global': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_income']), 600.00)
        self.assertEqual(response.data['total_users'], 3)

    def test_global_summary_denied_viewer(self):
        self.client.login(username='viewer', password='password')
        url = reverse('summary')
        response = self.client.get(url, {'global': 'true'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], "Only Admins and Analysts can access the global summary.")
