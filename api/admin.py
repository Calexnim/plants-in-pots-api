from urllib import response
from django.contrib import admin
from api.models import CartItem, Category, Fertilizer, Order, OrderItem, PlantTip, Product, User, Pot, Cart, SaleSummary
from django.contrib.admin.models import LogEntry
from rest_framework.authtoken.models import TokenProxy
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count, Sum
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportMixin
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']

class UserAdmin(admin.ModelAdmin):
    model = User

    def has_add_permission(self, request):
        return False

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class OrderAdmin(ExportMixin, admin.ModelAdmin):
    # change_list_template = 'admin/order_admin_change_listing.html'
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'name', 'email', 'phone', 'payment_option', 'delivery_option', 'total', 'order_date', 'latitude', 'longtitude']
    list_display = ['id', 'order_date', 'order_status']
    list_filter = ['order_status', 'order_date']


    # def has_delete_permission(self, request, obj=None):
    #     return False
    def has_add_permission(self, request, obj=None):
        return False

    


# class YourModelAdmin(admin.ModelAdmin):
#     change_form_template = 'custom_change_form.html'
# LogEntry.objects.all().delete()
admin.site.unregister(TokenProxy)

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Pot)
# admin.site.register(CartItem)
admin.site.register(Fertilizer)
admin.site.register(Order, OrderAdmin)
admin.site.register(PlantTip)