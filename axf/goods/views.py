from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from goods.filters import GoodsFilter
from goods.models import MainWheel, MainNav, MainShow, FoodType, Goods
from goods.serializers import MainWheelSerializer, MainNavSerializer, MainShowSerializer, FoodTypeSerializer, \
    GoodsSerializer


@api_view(['GET'])
def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_shows = MainShow.objects.all()

    res = {
        'main_wheels': MainWheelSerializer(main_wheels, many=True).data,
        'main_navs': MainNavSerializer(main_navs, many=True).data,
        'main_shows': MainShowSerializer(main_shows, many=True).data
    }
    return Response(res)


class FoodTypeView(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    queryset = FoodType.objects.all()
    serializer_class = FoodTypeSerializer


class MarketView(viewsets.GenericViewSet,
                 mixins.ListModelMixin):  # 前端访问/api/goods/market/ GET调用ListModelMixin中的list方法
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_class = GoodsFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        rule_list = [
            {'id': 1, 'order_name': '价格升序', 'order_value': '0'},
            {'id': 2, 'order_name': '价格降序', 'order_value': '1'},
            {'id': 3, 'order_name': '销量升序', 'order_value': '2'},
            {'id': 4, 'order_name': '销量降序', 'order_value': '3'},
        ]
        typeid = request.query_params.get('typeid')
        food_type = FoodType.objects.filter(typeid=typeid).first()
        # 全部分类:0#进口水果:103534#国产水果:103533
        a = food_type.childtypenames
        # d = []
        # for b in a.split('#'):
        #     c = {
        #         'child_name': b.split(':')[0],
        #         'child_value': b.split(':')[1]
        #     }
        #     d.append(c)
        d = [{'child_name': item.split(':')[0], 'child_value': item.split(':')[1]} for item in a.split('#')]
        res = {
            'goods_list': serializer.data,
            'order_rule_list': rule_list,
            'foodtype_childname_list': d
        }
        return Response(res)
