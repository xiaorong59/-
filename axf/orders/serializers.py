from rest_framework import serializers

from goods.serializers import GoodsSerializer
from orders.models import OrderModel, OrderGoodsModel


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderModel
        fields = ['o_status']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 当前订单所对应的详情内容
        order_goods = instance.ordergoodsmodel_set.all()
        data['order_goods_info'] = OrderGoodsSerializer(order_goods, many=True).data
        o_price = 0
        for item in data['order_goods_info']:
            o_price += item['o_goods']['price'] * item['goods_num']
        data['o_price'] = o_price

        return data


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = OrderGoodsModel
        fields = ['goods_num', 'goods']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['o_goods'] = data['goods']
        del data['goods']
        return data

