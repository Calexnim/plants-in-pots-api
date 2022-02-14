from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from api.models import CartItem, Category, Fertilizer, Pot, Product, User, Cart

class UserSerializer(serializers.ModelSerializer):
    #password1 for password confirmation
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password1']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
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


        
            