from django_filters import rest_framework as filters
from .models import Transaction

class TransactionFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date", lookup_expr='lte')
    category = filters.CharFilter(field_name="category", lookup_expr='icontains')
    transaction_type = filters.CharFilter(field_name="transaction_type")

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'category', 'start_date', 'end_date']
