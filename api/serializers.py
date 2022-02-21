from pyexpat import model
from urllib import response
from weakref import proxy
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from api.models import CartItem, Category, Fertilizer, Order, OrderItem, PlantTip, Pot, Product, User, Cart
from pyfcm import FCMNotification
import requests
import json
import firebase_admin
from firebase_admin import credentials, messaging


cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "plant-in-pots",
    "private_key_id": "4cf1032979cb6e82f2a11b6b2c8f108e0249ab4b",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDrzu7UXmcwZY47\no3knBxqMYafCYqQAksak3PIrcvEtqMX1Kwq+8vkD5CG4NjftHm/gi0BMout56si6\nHIBbvWU/7mJ1cY52VSiX6VXMfSVhxYwtdlB5DieLXLSwsBqe+m3+olbXUYLcM0lU\ntpgj7Sx63IdFQkHI2al4uZnCB0t9reurT4EjC7QzoX4CAfqUybmvvyZi8LrnWi7r\n+BSwAQIwPLfMV58iJJLSAJgs13UJulSWRneijp555I+WU1XSFt/z0weBMKn/d9Hi\nn/BQIOTROVoT3fdntYV4mGN0vMSRaWnN7N6S9DeLV3EkkhosEq0xydbdlBEVouQq\nYEf9DMXPAgMBAAECggEADubq/aahWBP9NCs3w3b+9gLivfWUl42KdcBQfd0nM/yO\nsOrINtqWdVa1OogTM7dVfRNSDm7uwocmqdcoQ3Y3Ruc8HBakIhVJfoQshPmwh98t\nLpYIUuGSnTAZRt/NnbyF7knUOdNmq+g49oDo/SzPrUxMC90V/VbID3q0756dHQ6v\niggEYnDkT+ctR15ZhxsnSBbTsmlb/fRX8GHPQFPVIENkvt9dma6kf4YZVjK6/p+A\nWwOPiGG2SwKWmTyG2uUfvPkdxtnGU9Ad6DsZfewqK4jdNtp8PDoW2yGXTLcaUKZ9\n8uCJSXr3ijnLjIMt+p7ehAuAVYMUQ27Vqz/Jq7lS+QKBgQD9pEe7vSqYuemw2FNp\ncpfshuAUyJyAM5TELaqIXtC/bn8/vbNI0hasu+eE1ogTlAOMJ7VC7IWZFCLQVM2h\nO4fOjOfVPfHfB88JVRYfzHLysIYQAn0/lfNLCiP2OZZWV9m5mHYj0eKsjNIVpKq9\ng8bh2JiZGVDYcbjWMoNY9A4mNwKBgQDuADSf7yLZmO3MyOQNpEqiZvZ9o3b7ZH7E\n12Mn+K2yPr0laHE+N3TBNuel/y7aBvmbSoXwrHmFG5l6rIppIVpTcPn50V0fT+8A\nJxTXNfARu1q1ETum/lynb2ckPDK3RAGNPHeQCYSE9uyGg7RLDJS23QDzvhLWQhZp\nO1HELDkRKQKBgQD2DGJF3civpVHsar3nwfFc0q4Xm1AuEVuUP1R5u7i2q2Mnm0eL\nMborUJDTzSTuERyr3m05AabMC7uF624apVwl44yV0OSMXc/alr7ClBtCEDnM2A1W\nHImJ1slx9wU+tzQPlbWtI9LHXkgCFN5Iv8ezmODXS7agcRlEOHYwWXhMWwKBgCB9\n0LFg4T4ZnaVOa6vdGP9Q1SfT0COD1bajvPqw/W2PGR1pQ8R9p6fVCgzkaI4FU8A6\njUyND033tZ1EvuSZVA5+JvJO/cqPjA5WR4cV6v9Qt5Jultk2com9MLSGr1nLo/aX\nIa99TSUl3KaEhnGUdxz70Ox1r3amsQ6OtZv1eZj5AoGBAKXx+7MULLSKC/DEgagD\nSCE2enlnK9dEH+ip5/DwGrLprZH+NRIwqZeYi8A9gM3AQNPRb53XOwsmhiCaW022\nYnX+SjL8l9Y4QXOOOuhmCMKTxvJ7Z9YozN5Kwfnfzpwrp2m6rEN6uE3F4R9K5MDU\nGfBRts//7iHQ4COKf6j8TzDk\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ub02j@plant-in-pots.iam.gserviceaccount.com",
    "client_id": "112637770232461792458",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ub02j%40plant-in-pots.iam.gserviceaccount.com"
})
firebase_admin.initialize_app(cred)

class UserSerializer(serializers.ModelSerializer):
    #password1 for password confirmation
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()
    # firebase_token = serializers.CharField()
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password1', 'firebase_token']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            firebase_token=self.validated_data['firebase_token'],
        )
        password = self.validated_data['password']
        password1 = self.validated_data['password1']

        if password != password1:
            raise serializers.ValidationError({'password': 'Password does not match.'})
        user.set_password(password)
        user.save()
        return user

    # Convert email to lowercase then check if exists in DB
    def validate_email(self, value):
        email = value.lower()
        if User.object.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        ReadOnlyField = 'id'


# Get product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        ReadOnlyField = 'id'

# Pot
class PotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pot
        fields = '__all__'
        ReadOnlyField = '__all__'

# Fertilizer
class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = '__all__'
        ReadOnlyField = '__all__'

# CartItem Read
class CartItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        depth = 1
    
# CartItem Write
class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


# CartSerializer Read
class CartSerializerRead(serializers.ModelSerializer):
    cart_item = CartItemReadSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'

# CartSerializer Write
class CartSerializerWrite(serializers.ModelSerializer):
    cart_item = CartItemWriteSerializer(many=True, partial=True)
    class Meta:
        model = Cart
        fields = '__all__'
        
    def create(self, validated_data):
        #pop all the items in cart
        cart_items = validated_data.pop('cart_item')
        user_has_cart = Cart.objects.filter(user=validated_data.get('user'))
        # Validation check to prevent user from having more than 1 cart
        if user_has_cart:
            raise serializers.ValidationError({'error': 'User already have cart'})
        # loop through products & pots inside the cart  
        else:
            cart = Cart.objects.create(**validated_data)
            for item in cart_items:
                #Check if there's items
                if item:
                    # Create CartItem Objects based on the products & pots
                    cart_item_object = CartItem.objects.create(product=item['product'], pot=item['pot'], fertilizer=item['fertilizer'])
                    # Associate the CartItem products & pots with Cart
                    cart_item_object.cart_item.add(cart)
        return cart

    def update(self, instance, validated_data):
        cart_items = validated_data.pop('cart_item')
        user_cart = Cart.objects.get(user=validated_data.get('user'))
        instance.user = validated_data.get('user', instance.user)
        instance.save()

        for item in cart_items:
            if item:
                cart_item_object = CartItem.objects.create(product=item['product'], pot=item['pot'], fertilizer=item['fertilizer'])
                cart_item_object.cart_item.add(user_cart)
        return instance



# Order item read serializer
class OrderItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'pot',
            'fertilizer',
            'sub_total',
        ]
        depth = 1

# Order item write serializer
class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'pot',
            'fertilizer',
            'sub_total',
        ]


# Order Write serializer
class OrderWriteSerializer(serializers.ModelSerializer):
    order_item = OrderItemWriteSerializer(many=True)
    order_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    payment_option = serializers.CharField()
    delivery_option = serializers.CharField()
    order_status = serializers.CharField(source='get_order_status_display', read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        #pop all the items in Order
        order_items = validated_data.pop('order_item')
        order = Order.objects.create(**validated_data)
        plant_tips = []
        all_tips_id = []
        all_tips = []
        for item in order_items:
            if item:
                items = OrderItem.objects.create(order=order, **item)
                plant_tip_queryset = Product.objects.filter(id=items.product.id).values('plant_tip_id')[:1]
                id = plant_tip_queryset[0].get('plant_tip_id')
                # Check duplicate id
                if id not in all_tips_id:
                    all_tips_id.append(id)
                    plant_tip_querysets = PlantTip.objects.filter(id=plant_tip_queryset).values()
                    plant_tips.append(plant_tip_querysets)

        registration_token = User.object.get_firebase_token_by_email(validated_data['user'])
        for tips in plant_tips:
            for tip in tips:
                print(tip)
                all_tips.append(tip)

        # See documentation on defining a message payload.
        message = messaging.Message(
            notification = messaging.Notification(
                title = 'Plant Tips',
                body = "You have made your order! Check out your plant tips!"
            ),
            data={
                "plant_tips": json.dumps(all_tips)
            },
            token=registration_token,
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        messaging.send(message)
        print('Successfully sent message:', response)

        return order

# Order Read serializer
class OrderReadSerializer(serializers.ModelSerializer):
    order_item = OrderItemReadSerializer(many=True)
    payment_option = serializers.CharField(source='get_payment_option_display')
    delivery_option = serializers.CharField(source='get_delivery_option_display')
    order_status = serializers.CharField(source='get_order_status_display')
    order_date = serializers.DateTimeField(format="%Y-%m-%d, %H:%M")
    delivery_date = serializers.DateTimeField(format="%Y-%m-%d, %H:%M")
    class Meta:
        model = Order
        fields = '__all__'

    # def create(self, validated_data):
    #     #pop all the items in Order
    #     order_items = validated_data.pop('order_item')
    #     order = Order.objects.create(**validated_data)
    #     for item in order_items:
    #         if item:
    #             OrderItem.objects.create(order=order, **item)
    #     return order
    
