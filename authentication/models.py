from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related
from django.utils.translation import gettext_lazy as _



# Create your models here.
#Customer
class Customer(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
    )
    phone = models.CharField()
    
#Address
class Address(models.Model):
    created_by = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE,
        related_name="created_by",
    )
    street = models.TextField()
    city = models.TextField()
    postal_code = models.TextField()
    state = models.TextField()
    country = models.TextField(
        max_length=2,
    )

#Product
class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    image = models.ImageField()
    price = models.DecimalField(
        decimal_places=2,
    )

#Category
class Category(models.Model):
    name = models.CharField()
    description = models.TextField()

#Plant Tip
class PlantTip(models.Model):
    sunlight = models.TextField()
    water = models.TextField()
    fertilizer_type = models.TextField()
    temperature = models.TextField()

#Cart
class Cart(models.Model):
    date_time_created = models.DateTimeField(
        auto_now=True,
    )

#Cart Item
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_item_product_id',
    )
    quantity = models.IntegerField()

#Order
class Order(models.Model):
    options = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('ready', 'Ready for Collect'),
        ('sending', 'Sending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]   
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )
    order_date = models.DateTimeField(
        auto_now_add=True,
    )
    delivery_date = models.DateTimeField()
    delivery_option = models.TextField()
    order_status = models.CharField(
        choices=options,
        default='pending',
    )

#Order Item
class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_item_product_id'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    item_price = models.DecimalField(
        decimal_places=2,
    )
    item_quantity = models.IntegerField()


#TODO: Create payment method
#TODO: Fix Error
#Payment
# class Payment(models.Model):
#     payment_method = models.TextField()
#     payment_option = models.TextField()

