from rest_framework.routers import SimpleRouter
from carts.views import CartView

router = SimpleRouter()
router.register('cart', CartView)

urlpatterns = [
    # path('add_cart/', add_cart),
]

urlpatterns += router.urls