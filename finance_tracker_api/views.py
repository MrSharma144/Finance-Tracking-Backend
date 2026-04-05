from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from .models import Transaction
from .serializers import TransactionSerializer
from .filters import TransactionFilter
from .permissions import IsAdmin, IsAnalyst, IsViewer, IsOwnerOrAdmin

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter

    def get_permissions(self):
        """
        Custom permissions for RBAC:
        - Admin: Full access.
        - Analyst: Full access to their own, view only for others (implied by queryset + IsOwnerOrAdmin).
        - Viewer: Read-only access to their own.
        """
        user = self.request.user
        
        # If user is not logged in, enforce authentication
        if not user.is_authenticated:
            return [permissions.IsAuthenticated()]

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if user.role == 'Viewer':
                # Viewers are read-only for all transaction management actions
                class IsReadOnly(permissions.BasePermission):
                    def has_permission(self, request, view): return False
                return [IsReadOnly()]
            
            # Admins and Analysts can manage transactions (Admins all, Analysts own)
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Admins and Analysts can see all transactions.
        Viewers can only see their own.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Transaction.objects.none()
            
        if user.role in ['Admin', 'Analyst']:
            return Transaction.objects.all().order_by('-date')
        
        return Transaction.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        # Automatically set the user when creating a transaction
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Returns a summary of transactions including total income, expenses, balance, 
        and category-wise breakdown. Respects filters (date range, type, category).
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Calculate total income and expenses
        summary_data = queryset.aggregate(
            total_income=Sum('amount', filter=Q(transaction_type='Income')),
            total_expense=Sum('amount', filter=Q(transaction_type='Expense'))
        )
        
        # Adjust for None values (if no transactions exist)
        total_income = summary_data['total_income'] or 0
        total_expense = summary_data['total_expense'] or 0
        balance = total_income - total_expense

        # Category-wise breakdown
        categories = queryset.values('category').annotate(
            income=Sum('amount', filter=Q(transaction_type='Income')),
            expense=Sum('amount', filter=Q(transaction_type='Expense'))
        ).order_by('category')

        # Format category breakdown to be more readable
        category_breakdown = []
        for cat in categories:
            category_breakdown.append({
                'category': cat['category'],
                'income': cat['income'] or 0,
                'expense': cat['expense'] or 0,
                'net': (cat['income'] or 0) - (cat['expense'] or 0)
            })

        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'category_breakdown': category_breakdown
        })
