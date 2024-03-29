import django_filters

from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    # 接口中过滤的参数 = CharFilter(数据库中过滤的字段, methods='', lookup_expr='')
    # lookup_expr 写表达式 模糊查询等
    # 字段名不能省略 名字与过滤参数名不一样
    typeid = django_filters.CharFilter('categoryid')
    # 字段名可以省略
    childcid = django_filters.CharFilter(method='filter_childcid')
    order_rule = django_filters.CharFilter(method='filter_order_rule')

    class Meta:
        model = Goods
        fields = []

    def filter_childcid(self, queryset, name, value):
        if value == '0':
            return queryset
        else:
            return queryset.filter(childcid=value)

    def filter_order_rule(self, queryset, name, value):
        if value == '0':
            return queryset.order_by('price')
        elif value == '1':
            return queryset.order_by('-price')
        elif value == '2':
            return queryset.order_by('productnum')
        else:
            return queryset.order_by('-productnum')
