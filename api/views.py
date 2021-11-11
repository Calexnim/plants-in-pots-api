from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from api.serializers import UserSerializer

# Create your views here.
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
