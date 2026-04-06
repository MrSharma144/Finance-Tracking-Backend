from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Transaction
import datetime

class RBAC_Tests(APITestCase):
    def setUp(self):
        # Create different role users
        self.admin = CustomUser.objects.create_user(username='admin', password='password', role='Admin')
        self.analyst = CustomUser.objects.create_user(username='analyst', password='password', role='Analyst')
        self.viewer = CustomUser.objects.create_user(username='viewer', password='password', role='Viewer')
        self.other_user = CustomUser.objects.create_user(username='other', password='password', role='Viewer')

        # Create a transaction belonging to admin
        self.admin_tx = Transaction.objects.create(
            user=self.admin, amount=100.00, transaction_type='Income', category='Salary', date='2024-01-01'
        )
        # Create a transaction belonging to other_user
        self.other_tx = Transaction.objects.create(
            user=self.other_user, amount=50.00, transaction_type='Expense', category='Food', date='2024-01-02'
        )

    # Admin tests
    def test_admin_can_see_all(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('transaction-list'))
        self.assertEqual(len(response.data['results']), 2)

    def test_admin_can_delete_other_tx(self):
        self.client.login(username='admin', password='password')
        url = reverse('transaction-detail', kwargs={'pk': self.other_tx.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Analyst tests
    def test_analyst_can_see_all(self):
        self.client.login(username='analyst', password='password')
        response = self.client.get(reverse('transaction-list'))
        self.assertEqual(len(response.data['results']), 2)

    def test_analyst_cannot_delete_other_tx(self):
        self.client.login(username='analyst', password='password')
        url = reverse('transaction-detail', kwargs={'pk': self.other_tx.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Viewer tests
    def test_viewer_can_only_see_own(self):
        self.client.login(username='viewer', password='password')
        response = self.client.get(reverse('transaction-list'))
        self.assertEqual(len(response.data['results']), 0) # This user has no tx

    def test_viewer_can_create(self):
        self.client.login(username='viewer', password='password')
        data = {
            'amount': 10.00,
            'transaction_type': 'Expense',
            'category': 'Groceries',
            'date': '2024-01-01'
        }
        response = self.client.post(reverse('transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.filter(user=self.viewer).count(), 1)

    def test_viewer_cannot_delete_own_tx(self):
        # Create a tx for viewer first
        viewer_tx = Transaction.objects.create(
            user=self.viewer, amount=20.00, transaction_type='Expense', category='Groceries', date='2024-01-01'
        )
        self.client.login(username='viewer', password='password')
        url = reverse('transaction-detail', kwargs={'pk': viewer_tx.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
