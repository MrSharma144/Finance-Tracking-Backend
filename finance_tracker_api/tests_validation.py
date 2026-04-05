from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Transaction
import datetime

class ValidationTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='tester', password='password', role='Admin')
        self.client.login(username='tester', password='password')

    def test_invalid_amount_fails(self):
        url = reverse('transaction-list')
        data = {
            'amount': -100.00, # Invalid
            'transaction_type': 'Expense',
            'category': 'Food',
            'date': '2024-01-01'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Amount must be greater than zero.', str(response.data['amount']))

    def test_future_date_fails(self):
        url = reverse('transaction-list')
        future_date = (datetime.date.today() + datetime.timedelta(days=40)).strftime('%Y-%m-%d')
        data = {
            'amount': 50.00,
            'transaction_type': 'Expense',
            'category': 'Food',
            'date': future_date
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Date cannot be more than 30 days in the future.', str(response.data['date']))
