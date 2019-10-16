import django_filters

from orders.models import OrderModel


class OrderFilter(django_filters.rest_framework.FilterSet):
    o_status = django_filters.CharFilter(method='filter_status')

    class Meta:
        model = OrderModel
        fields = []

    def filter_status(self, queryset, name, value):
        if value == 'all':
            return queryset
        elif value == 'not_pay':
            return queryset.filter(o_status=0)
        else:
            return queryset.filter(o_status=1)