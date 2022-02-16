from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, response, filters
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework import viewsets
from api import serializers
from api.models import CartItem, Fertilizer, User, Category, Product, Pot, Cart
from rest_framework.authtoken.models import Token
from api.serializers import CartItemReadSerializer, CartItemWriteSerializer, CartSerializerRead, CartSerializerWrite, CategorySerializer, FertilizerSerializer, PotSerializer, ProductSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def registration_view(request):
    """
    Create new user
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Account created!"
            token = Token.objects.get(user=account).key
            data['token'] = token
            # Get user id from token
            user_id = Token.objects.get(key=token).user_id
            data['user_id'] = user_id
            # return token and user_id once created
            return Response(data, status=status.HTTP_201_CREATED)
        #Return Error
        return Response(serializer.errors)

@api_view(['GET'])
def user_retrieve(request, pk):
    """
    Retrieve user by pk 
    """
    try:
        user = User.object.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Custom ObtainAuthToken to return user_id & token
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk
        })

# class RegistrationView(APIView):
#     """
#     Create new user
#     """

class CategoryViewSet(viewsets.ModelViewSet):
    """
    List all category, get one category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of Category
        """
        return Category.objects.all()
    
    def list(self, request):
        """
        List all objects
        """
        try:
            serializer = CategorySerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        except:
            return Response("No Category", status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Create category
        """
        serializer = CategorySerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            category_name = serializer.validated_data['name']
            category_description = serializer.validated_data['description']
            if category_name:
                category_exists = Category.objects.filter(name=category_name, 
                description=category_description) 
                # Check if category exists
                if not category_exists:    
                    serializer.save()
                    data['response'] = "Category added!"
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    data['response'] = "Category exists"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
        #Return Error
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        """
        Retrieve single object by id
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

# CRUD for Product
class ProductViewSet(viewsets.ModelViewSet):
    """
    List all Products, get one product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filter_fields = ['category']

    def get_queryset(self):
        return super().get_queryset()

class PotViewSet(viewsets.ModelViewSet):
    """
    List all Pots, get one pot
    """
    queryset = Pot.objects.all()
    serializer_class = PotSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FertilizerViewSet(viewsets.ModelViewSet):
    """
    List all Fertilizer, get one fertilizer
    """
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Different serializer based on http method for Cart
class CartsViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CartSerializerRead
        if self.action == 'update' or self.action == 'create' or self.action == 'destroy':
            return CartSerializerWrite
        return CartSerializerRead

class CartViewSet(CartsViewSet):
    """
    Create & list cart
    """
    queryset = Cart.objects.all()
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # serializer_class = CartSerializer
    lookup_field = 'user'

    def get_queryset(self):
        return super().get_queryset()

# Different serializer based on http method for Cart Item
class CartItemsViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CartItemReadSerializer
        if self.action == 'destroy' or self.action == 'list':
            return CartItemWriteSerializer
        return CartItemWriteSerializer


class CartItemViewSet(CartItemsViewSet):
    queryset = CartItem.objects.all()
    # serializer_class = CartItemSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return super().get_queryset()
    

