from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
#UserManager 
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

#User
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email', 
        max_length=60, unique=True
    )
    username = models.CharField(
        max_length=30, 
        unique=True
    )
    date_joined = models.DateTimeField(
        verbose_name='date joined', 
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        verbose_name='last login',
        auto_now_add=True
    )
    is_admin = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=False
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    object = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, permission, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

#Token Authentication
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#Address
class Address(models.Model):
    created_by = models.ForeignKey(
        User, 
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
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    image = models.ImageField()
    price = models.DecimalField(
        decimal_places=2,
        max_digits=6,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="product_category",
        null=True,
    )

#Category
class Category(models.Model):
    name = models.CharField(
        max_length=255,
    )
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    order_date = models.DateTimeField(
        auto_now_add=True,
    )
    delivery_date = models.DateTimeField()
    delivery_option = models.TextField()
    order_status = models.CharField(
        max_length=255,
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
        max_digits=6,
    )
    item_quantity = models.IntegerField()


#TODO: Create payment method
#Payment
# class Payment(models.Model):
#     payment_method = models.TextField()
#     payment_option = models.TextField()

