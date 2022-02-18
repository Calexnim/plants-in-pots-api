from django.contrib import admin
from api.models import CartItem, Category, Fertilizer, Order, OrderItem, Product, User, Pot, Cart
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'order_status']
    list_filter = ['order_status']

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Pot)
admin.site.register(Cart)
# admin.site.register(CartItem)
admin.site.register(Fertilizer)
admin.site.register(Order, OrderAdmin)