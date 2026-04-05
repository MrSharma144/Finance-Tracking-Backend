from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    ANALYST = 'Analyst'
    VIEWER = 'Viewer'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (ANALYST, 'Analyst'),
        (VIEWER, 'Viewer'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=VIEWER
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Transaction(models.Model):
    INCOME = 'Income'
    EXPENSE = 'Expense'
    
    TRANSACTION_TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    CATEGORY_CHOICES = [
        ('Salary', 'Salary'),
        ('Freelance', 'Freelance'),
        ('Investments', 'Investments'),
        ('Gift', 'Gift'),
        ('Miscellaneous Income', 'Miscellaneous Income'),
        ('Rent/Mortgage', 'Rent/Mortgage'),
        ('Groceries', 'Groceries'),
        ('Dining Out', 'Dining Out'),
        ('Transportation', 'Transportation'),
        ('Utilities', 'Utilities'),
        ('Healthcare', 'Healthcare'),
        ('Insurance', 'Insurance'),
        ('Entertainment', 'Entertainment'),
        ('Shopping', 'Shopping'),
        ('Miscellaneous Expense', 'Miscellaneous Expense'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        default='Miscellaneous Expense'
    )
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type}: {self.amount} ({self.category})"
