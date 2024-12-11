from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Account

class CreateAccountWithEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password']

    def create(self, validated_data):

        account = Account.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
        )
        return account

        
    
class LoginWithEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class PasswordResetInitiateSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField()
