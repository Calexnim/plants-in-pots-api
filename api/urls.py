from django.urls import path
from django.conf.urls import url, include
from api.views import(
    registration_view,
    user_retrieve,
    CategoryViewSet
)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
app_name = "api"

router = DefaultRouter()
router.register('', CategoryViewSet, basename='category')
# urlpatterns = router.urls
urlpatterns = [
    path('account/register', registration_view, name='register'),
    path('account/<int:pk>/', user_retrieve),
    path('account/login', obtain_auth_token, name="login"),
    path(r'category', include(router.urls))
]