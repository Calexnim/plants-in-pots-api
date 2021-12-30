from django.contrib import admin
from api.models import Category, Product, User, Pot
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Pot)