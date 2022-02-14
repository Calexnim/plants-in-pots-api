from posixpath import basename
from django.urls import path
from django.conf.urls import include
# from api.models import CartItem
from api.views import(
    CartItemViewSet,
    CartViewSet,
    CustomAuthToken,
    FertilizerViewSet,
    PotViewSet,
    ProductViewSet,
    registration_view,
    user_retrieve,
    CategoryViewSet
)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
app_name = "api"

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'pot', PotViewSet, basename='pot')
router.register(r'fertilizer', FertilizerViewSet, basename='fertilizer')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-item', CartItemViewSet, basename='cart-item')
# urlpatterns = router.urls
urlpatterns = [
    path('account/register', registration_view, name='register'),
    path('account/<int:pk>/', user_retrieve),
    path('account/login', CustomAuthToken.as_view(), name="login"),
    path('', include(router.urls))
]