from rest_framework import viewsets, permissions, views, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Transaction, CustomUser
from .serializers import TransactionSerializer, UserSerializer, UserRegistrationSerializer
from .filters import TransactionFilter
from .permissions import IsAdmin, IsAnalyst, IsViewer, IsOwnerOrAdmin, IsUserOwnerOrAdmin

class SummaryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Dedicated endpoint for transaction summary analytics.
        Supported filters: start_date, end_date, category, transaction_type.
        """
        # We reuse the logic from the TransactionViewSet but in a standalone view
        user = request.user
        
        # Base queryset based on role
        if user.role in ['Admin', 'Analyst']:
            queryset = Transaction.objects.all()
        else:
            queryset = Transaction.objects.filter(user=user)

        # Apply filters
        filter_backend = TransactionFilter(request.GET, queryset=queryset)
        queryset = filter_backend.qs

        # Calculate totals
        summary_data = queryset.aggregate(
            total_income=Sum('amount', filter=Q(transaction_type='Income')),
            total_expense=Sum('amount', filter=Q(transaction_type='Expense'))
        )
        
        total_income = summary_data['total_income'] or 0
        total_expense = summary_data['total_expense'] or 0
        balance = total_income - total_expense

        # Category breakdown
        categories = queryset.values('category').annotate(
            income=Sum('amount', filter=Q(transaction_type='Income')),
            expense=Sum('amount', filter=Q(transaction_type='Expense'))
        ).order_by('category')

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

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'list':
            return [permissions.IsAuthenticated(), IsAdmin()]
        if self.action == 'me':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsUserOwnerOrAdmin()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

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
