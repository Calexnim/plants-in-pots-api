from django.contrib import admin
from api.models import Category, Product, User
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)