import uuid

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import OrderModel
from user.models import UserModel
from user.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from utils.auth import UserAuth
from utils.errors import ParamsException


class UserView(viewsets.GenericViewSet,
               mixins.ListModelMixin):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (UserAuth,)

    def list(self, request, *args, **kwargs):
        # 通过token获取用户信息
        user = request.user
        orders_not_pay_num = OrderModel.objects.filter(user=user, o_status=0).count()
        orders_not_send_num = OrderModel.objects.filter(user=user, o_status=1).count()
        res = {
            'user_info': {
                'u_username': user.username
            },
            'orders_not_pay_num': orders_not_pay_num,
            'orders_not_send_num': orders_not_send_num,
        }
        return Response(res)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        # 请求地址：/api/user/auth/register/
        # 请求方式：
        # 1. 获取前端传递的参数
        data = self.request.data
        # 2. 字段校验（重新定义UserRegisterSerializer）
        serializer = UserRegisterSerializer(data=data)
        # 3. 注册功能实现
        result = serializer.is_valid()
        if not result:
            res = {'code': 1004, 'msg': '字段校验错误', 'data': serializer.errors}
            raise ParamsException(res)
        user = UserModel.objects.create(
            username=serializer.data.get('u_username'),
            password=make_password(serializer.data.get('u_password')),
            email=serializer.data.get('u_email')
        )
        # 4. 返回数据
        res = {
            'user_id': user.id
        }
        return Response(res)

    @action(detail=False, methods=['POST'], serializer_class=UserLoginSerializer)
    def login(self, request):
        # 请求地址：/api/user/auth/login/
        data = request.data
        # self.get_serializer调用UserLoginSerializer
        serializer = self.get_serializer(data=data)
        result = serializer.is_valid()
        if not result:
            res = {'code': 1007, 'msg': '校验登录参数失败', 'data': serializer.errors}
            raise ParamsException(res)
        # 登录标识符的操作
        # 1.获取唯一的标识符传递给前端
        token = uuid.uuid4().hex
        # 2.存储标识符和当前登录用户的关联关系(redis)
        username = serializer.data.get('u_username')
        user = UserModel.objects.filter(username=username).first()
        # 使用redis中的string类型进行存储， 存储的key为token值，value为当前登录用户的id值
        cache.set(token, user.id, timeout=12000)
        res = {
            'token': token
        }
        return Response(res)
