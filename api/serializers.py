from rest_framework import serializers
from api.models import User

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
