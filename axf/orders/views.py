import uuid

from rest_framework import viewsets, mixins
from rest_framework.response import Response

from carts.models import CartModel
from orders.filters import OrderFilter
from orders.models import OrderModel, OrderGoodsModel
from orders.serializers import OrderSerializer


class OrderView(viewsets.GenericViewSet,
                mixins.ListModelMixin,):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    filter_class = OrderFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # 请求地址： /api/orders/orders/
        # 请求方式：post
        # 1. 获取登录用户user、获取创建的订单号
        user = request.user
        o_num = uuid.uuid4().hex
        # 2. 查询购物车中商品is_select为True的数据
        carts = CartModel.objects.filter(is_select=True, user=user).all()
        res = {}
        if carts:
            # 3. 创建订单
            order = OrderModel.objects.create(user=user, o_num=o_num)
            # 4. 创建订单详情表
            for cart in carts:
                OrderGoodsModel.objects.create(goods=cart.goods,
                                               order=order,
                                               goods_num=cart.c_num)
                cart.delete()
                res = {'msg': '下单成功'}
        else:
            # 没有需要下单的商品
            res = {'code': 1009, 'msg': '没有下单的商品，请添加'}
        return Response(res)

        # 4. 已下单的商品，应该从购物车中删掉

