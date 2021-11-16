from django.urls import path
from api.views import(
    registration_view,
    user_retrieve,
)
from rest_framework.authtoken.views import obtain_auth_token
app_name = "api"

urlpatterns = [
    path('register', registration_view, name='register'),
    path('<int:pk>/', user_retrieve),
    path('login', obtain_auth_token, name="login"),
]