from rest_framework import serializers

from carts.models import CartModel
from goods.models import Goods
from goods.serializers import GoodsSerializer


class CartSerializer(serializers.ModelSerializer):
    # 方法3
    goods = GoodsSerializer()

    class Meta:
        model = CartModel
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['c_is_select'] = data['is_select']
        data['c_goods_num'] = data['c_num']
        # 序列化商品对象信息 方法1
        # goods = Goods.objects.filter(id=data['goods']).first()
        # goods = instance.goods
        # data['c_goods'] = GoodsSerializer(goods).data
        # 方法2
        # data['c_goods'] = {
        #     'id': instance.goods.id,
        #     'price': instance.goods.price
        # }

        data['c_goods'] = data['goods']
        del data['c_num']
        del data['user']
        del data['is_select']
        del data['goods']
        return data
