from django.urls import path
from django.conf.urls import include
from api.views import(
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
# urlpatterns = router.urls
urlpatterns = [
    path('account/register', registration_view, name='register'),
    path('account/<int:pk>/', user_retrieve),
    path('account/login', obtain_auth_token, name="login"),
    path('', include(router.urls))
]