from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Transaction

class CategoryTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='catuser', password='password', role='Admin')
        self.client.login(username='catuser', password='password')

    def test_valid_category(self):
        url = reverse('transaction-list')
        data = {
            'amount': 50.00,
            'transaction_type': 'Expense',
            'category': 'Groceries', # Valid
            'date': '2024-01-01'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_category(self):
        url = reverse('transaction-list')
        data = {
            'amount': 50.00,
            'transaction_type': 'Expense',
            'category': 'Unknown Category', # Invalid
            'date': '2024-01-01'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('is not a valid choice', str(response.data['category']))
