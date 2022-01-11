from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, response, filters
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from api import serializers
from api.models import User, Category, Product
from rest_framework.authtoken.models import Token
from api.serializers import CategorySerializer, ProductSerializer, UserSerializer
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

    # def list(self, request):
    #     """
    #     List all Product objects
    #     """
    #     try:
    #         category_id = request.query_params.get('category')
    #         # Check product/?category_id endpoint
    #         if category_id:
    #             queryset = self.get_queryset().filter(category=category_id)    
    #             serializer = ProductSerializer(queryset, many=True)
    #             if not serializer.data:
    #                 return Response("No product", status=status.HTTP_404_NOT_FOUND)
    #         else:
    #             serializer = ProductSerializer(self.get_queryset(), many=True)
    #         return Response(serializer.data)
    #     except:
    #         return Response("No Product", status=status.HTTP_404_NOT_FOUND)
    
    # def retrieve(self, request, pk=None):
    #     """
    #     Retrieve one product
    #     """
    #     try:
    #         product = Product.objects.get(pk=pk)
    #         serializer = ProductSerializer(product)
    #         return Response(serializer.data)
    #     except:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

