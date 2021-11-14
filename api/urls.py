from django.urls import path
from api.views import(
    registration_view,
    user_retrieve,
)

app_name = "api"

urlpatterns = [
    path('register', registration_view, name='register'),
    path('<int:pk>/', user_retrieve)
]