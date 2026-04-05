from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Transaction
import datetime

class AnalyticsTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', 
            password='testpassword',
            role=CustomUser.VIEWER
        )
        self.client.login(username='testuser', password='testpassword')
        
        # Create some transactions
        Transaction.objects.create(
            user=self.user,
            amount=1000.00,
            transaction_type='Income',
            category='Salary',
            date=datetime.date(2024, 1, 1)
        )
        Transaction.objects.create(
            user=self.user,
            amount=200.00,
            transaction_type='Expense',
            category='Food',
            date=datetime.date(2024, 1, 5)
        )
        Transaction.objects.create(
            user=self.user,
            amount=300.00,
            transaction_type='Expense',
            category='Food',
            date=datetime.date(2024, 1, 10)
        )
        Transaction.objects.create(
            user=self.user,
            amount=500.00,
            transaction_type='Income',
            category='Freelance',
            date=datetime.date(2024, 2, 1)
        )

    def test_summary_totals(self):
        url = reverse('transaction-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_income']), 1500.00)
        self.assertEqual(float(response.data['total_expense']), 500.00)
        self.assertEqual(float(response.data['balance']), 1000.00)

    def test_summary_filtering_by_date(self):
        url = reverse('transaction-summary')
        response = self.client.get(url, {'start_date': '2024-01-01', 'end_date': '2024-01-31'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only Jan transactions: 1000 income, 500 expense
        self.assertEqual(float(response.data['total_income']), 1000.00)
        self.assertEqual(float(response.data['total_expense']), 500.00)

    def test_category_breakdown(self):
        url = reverse('transaction-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        breakdown = response.data['category_breakdown']
        
        # Check Food category (should have 500 total expense)
        food_stats = next(item for item in breakdown if item['category'] == 'Food')
        self.assertEqual(float(food_stats['expense']), 500.00)
        self.assertEqual(float(food_stats['income']), 0.00)
        
        # Check Salary category (should have 1000 total income)
        salary_stats = next(item for item in breakdown if item['category'] == 'Salary')
        self.assertEqual(float(salary_stats['income']), 1000.00)
