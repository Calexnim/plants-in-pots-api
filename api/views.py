from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import User

from api.serializers import UserSerializer

# Create your views here.
# class UserList(APIView):
    
@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Account created!"
            data['email'] = user.email
            data['username'] = user.username
            return Response(data, status=status.HTTP_201_CREATED)

        #Return Error
        return Response(serializer.errors)

@api_view(['GET'])
def user_retrieve(request, pk):
    """
    Retrieve user
    """
    print(pk)
    try:
        user = User.object.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response("testest", status=status.HTTP_400_BAD_REQUEST)