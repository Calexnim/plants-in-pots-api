from django.contrib import admin
from api.models import Category, User
# Register your models here.

admin.site.register(User)
admin.site.register(Category)