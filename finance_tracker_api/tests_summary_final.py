from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Transaction
import datetime

class SummaryAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='summaryuser', password='password', role='Viewer')
        self.client.login(username='summaryuser', password='password')
        
        # Create transactions
        Transaction.objects.create(
            user=self.user, amount=1000.00, transaction_type='Income', category='Salary', date='2024-01-01'
        )
        Transaction.objects.create(
            user=self.user, amount=200.00, transaction_type='Expense', category='Food', date='2024-01-05'
        )

    def test_dedicated_summary_endpoint(self):
        url = reverse('summary') # Named 'summary' in urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_income']), 1000.00)
        self.assertEqual(float(response.data['total_expense']), 200.00)
        self.assertEqual(float(response.data['balance']), 800.00)

    def test_summary_date_filtering(self):
        url = reverse('summary')
        # Filter for a date range that misses the transactions
        response = self.client.get(url, {'start_date': '2024-02-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_income']), 0.00)
