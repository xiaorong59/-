from django.urls import path
from rest_framework.routers import SimpleRouter
from user.views import *

router = SimpleRouter()
# 地址：/api/user/auth/ /api/user/auth/[id]/
router.register('auth', UserView)

urlpatterns = [

]

urlpatterns += router.urls
