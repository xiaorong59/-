import re

from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from user.models import UserModel
from utils.errors import ParamsException


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class UserRegisterSerializer(serializers.Serializer):
    # 只实现字段校验功能
    u_username = serializers.CharField(required=True, max_length=6,
                                     min_length=3, error_messages={
            'required': '该参数必填',
            'max_length': '不超过6字符',
            'min_length': '不短于3字符'
        })
    u_password = serializers.CharField(required=True, max_length=20,
                                     min_length=6, error_messages={
            'required': '该参数必填',
            'max_length': '不超过20字符',
            'min_length': '不短于6字符'
        })
    u_password2 = serializers.CharField(required=True, max_length=20,
                                      min_length=6, error_messages={
            'required': '该参数必填',
            'max_length': '不超过20字符',
            'min_length': '不短于6字符'
        })
    u_email = serializers.CharField(required=True,
                                  error_messages={
                                      'required': '该参数必填',
                                  })

    def validate(self, attrs):
        # 账号必须不存在
        res = {}
        username = attrs.get('u_username')
        email = attrs.get('u_email')
        # 密码和确认密码必须一致
        # 邮箱正则匹配
        if UserModel.objects.filter(username=username):
            res = {'code': 1001, 'msg': '账号已存在'}

        if UserModel.objects.filter(email=email):
            res = {'code': 1000, 'msg': '邮箱已存在'}
        re_compile = re.compile('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
        if not re_compile.fullmatch(email):
            res = {'code': 1000, 'msg': '邮箱格式不正确'}
        if res:
            raise ParamsException(res)
        return attrs


class UserLoginSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True, max_length=6,
                                     min_length=3, error_messages={
            'required': '该参数必填',
            'max_length': '不超过6字符',
            'min_length': '不短于3字符'
        })
    u_password = serializers.CharField(required=True, max_length=20,
                                     min_length=6, error_messages={
            'required': '该参数必填',
            'max_length': '不超过20字符',
            'min_length': '不短于6字符'
        })

    def validate(self, attrs):
        #  1.登录账号存在
        username = attrs.get('u_username')
        user = UserModel.objects.filter(username=username).first()
        if not user:
            res = {'code': 1005, 'msg': '登陆账号不存在，请去注册'}
            raise ParamsException(res)
        #  2.登陆密码是否正确
        password = attrs.get('u_password')
        if not check_password(password, user.password):
            res = {'code': 1006, 'msg': '登陆账号的密码错误'}
            raise ParamsException(res)
        return attrs

