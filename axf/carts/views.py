from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from carts.models import CartModel
from carts.serializers import CartSerializer
from utils.auth import UserAuth


class CartView(viewsets.GenericViewSet,
               mixins.ListModelMixin,
               mixins.UpdateModelMixin):
    queryset = CartModel.objects.all()
    serializer_class = CartSerializer
    # 用户认证类
    # authentication_classes = (UserAuth,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = request.user
        queryset = queryset.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        # 全选按钮为True， 条件为：当前用户下的购物车中所有商品的is_select为True
        # 全选按钮为False， 条件为：当前用户下的购物车中只要有商品的is_select为False
        all_select = True
        if CartModel.objects.filter(user=user, is_select=False):
            all_select = False
        total_price = 0
        for item in serializer.data:
            if item['c_is_select']:
                total_price += item['c_goods_num'] * item['c_goods']['price']

        res = {
            'carts': serializer.data,
            'total_price': '%.2f' % total_price,
            'all_select': all_select,  # 全选按钮
            'user_info': {
                'u_username': user.username
                
            },
        }
        return Response(res)

    @action(detail=False, methods=['POST'])
    def add_cart(self, request):
        # 请求地址：/api/cart/cart/add_cart/
        # 请求方式：post
        user = request.user
        goods_id = request.data.get('goodsid')
        user_card = CartModel.objects.filter(user=user, goods_id=goods_id).first()
        if user_card:
            # 当前登录用户已添加过该商品，需修改个数字段
            user_card.c_num += 1
            user_card.save()
        else:
            CartModel.objects.create(goods_id=goods_id, user=user)
        res = {'msg': '添加商品成功'}
        return Response(res)

    @action(detail=False, methods=['POST'])
    def sub_cart(self, request):
        # 1. 获取用户user对象，前端传递的商品id
        user = request.user
        goods_id = request.data.get('goodsid')
        # 2. 根据用户和商品id获取购物车中的商品
        user_card = CartModel.objects.filter(user=user, goods_id=goods_id).first()
        # 3. 减少商品数量 商品c_num为1，删除数据，否则自减1
        if user_card.c_num == 1:
            user_card.delete()
        else:
            user_card.c_num -= 1
            user_card.save()
        res = {'msg': '商品减少成功'}
        return Response(res)

    def update(self, request, *args, **kwargs):
        # 修改当前选择的商品的is_select字段
        instance = self.get_object()
        # instance.is_select = 1 if instance.is_select == 0 else 0
        instance.is_select = not instance.is_select
        instance.save()
        res = {'msg': '商品勾选/取消成功'}
        return Response(res)

    @action(detail=False, methods=['PATCH'])
    def change_select(self, request):
        # 判断当前用户下的购物车中是否有is_select为False的商品
        user = request.user
        # 如果有， 所有的is_select修改为True
        if CartModel.objects.filter(user=user, is_select=False):
            CartModel.objects.filter(user=user).update(is_select=True)
        # 如果没有，所有的is_select修改为False
        else:
            CartModel.objects.filter(user=user).update(is_select=False)
        res = {'msg': '全选操作'}
        return Response(res)

