from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import PermissionsMixin


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
    
    def get_firebase_token_by_email(self, find_email):
        user = self.get(email=find_email)
        return user.firebase_token

#User
class User(AbstractBaseUser, PermissionsMixin):
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
    firebase_token = models.CharField(
        max_length=255,
        null=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    object = UserManager()

    # def __str__(self):
    #     return self.email
    
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
    description = models.TextField(
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="images/")
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
    plant_tip = models.ForeignKey(
        "PlantTip",
        null=True,
        on_delete=models.SET_NULL,
        related_name="plant_tip",
    )

    def __str__(self):
        return self.name

        
#Fertilizer
class Fertilizer(models.Model):
    name = models.CharField(
        max_length=255,
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=6,
    )

    def __str__(self):
        return self.name

#Pot
class Pot(models.Model):
    name = models.CharField(
        max_length=255,
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=6,
    )

    def __str__(self):
        return self.name
#Category
class Category(models.Model):
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        
#Plant Tip
class PlantTip(models.Model):
    name = models.CharField(
        max_length=255,
    )
    sunlight = models.TextField()
    water = models.TextField()
    humidity = models.TextField()

    def __str__(self):
        return self.name
#Cart
class Cart(models.Model):
    date_time_created = models.DateTimeField(
        auto_now=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_user_id',
    )
    cart_item = models.ManyToManyField(
        "CartItem",
        related_name="cart_item"
    )

#Cart Item
class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE, 
        related_name="cart_product",
    )
    pot = models.ForeignKey(
        Pot,
        on_delete=models.CASCADE, 
    )
    fertilizer = models.ForeignKey(
        Fertilizer,
        on_delete=models.CASCADE,
    )

#Order
class Order(models.Model):
    options = [
        ('pending', 'Pending'),
        ('ready', 'Ready for Collect'),
        ('preparing', 'Preparing'),
        ('delivering', 'Delivering'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=255,
        null=True,
    )
    email = models.EmailField(
        verbose_name='email', 
        max_length=60,
        null=True,
    )
    phone = models.CharField(
        max_length=20,
        null=True,
    )
    order_date = models.DateTimeField(
        auto_now_add=True,
    )
    total = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
    )
    delivery_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    payment_option = models.CharField(
        max_length=255,
        choices=[
            ('online', 'Email Payment Receipt'),
            ('cod', 'Cash on Delivery'),
        ],
        default='online',
    )
    delivery_option = models.CharField(
        max_length=255,
        choices=[
            ('pickup', 'Onsite Pick-up'),
            ('delivery', 'Delivery for Service'),
        ],
        default='pickup',
    )
    order_status = models.CharField(
        max_length=255,
        choices=options,
        default='pending',
    )
    latitude = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    longtitude = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

#Order Item
class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE, 
        related_name="order_product",
    )
    pot = models.ForeignKey(
        Pot,
        on_delete=models.CASCADE, 
        related_name="order_pot",
    )
    fertilizer = models.ForeignKey(
        Fertilizer,
        on_delete=models.CASCADE,
        related_name="order_fertilizer",
    )
    sub_total = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        null=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_item"
    )

class SaleSummary(Order):
    class Meta:
        proxy = True
        verbose_name = 'Sale Summary'
        verbose_name_plural = 'Sale Summaries'