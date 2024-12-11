
import random
import logging

from datetime import timedelta
from django.utils.timezone import now
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Account
from misc.models import OTP
from misc.mixins import CustomResponseMixin
from .serializers import (
    CreateAccountWithEmailSerializer,
    LoginWithEmailSerializer,
    PasswordResetInitiateSerializer,
    PasswordResetCompleteSerializer
)

logger = logging.getLogger(__name__)


def generate_access_token(account):
    refresh = RefreshToken.for_user(account)
    return str(refresh.access_token)

class CreateAccountWithEmailView(CustomResponseMixin, APIView):
    def post(self, request):
        serializer = CreateAccountWithEmailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                account = serializer.save()
                access_token = generate_access_token(account)
                return Response({'email': account.email, 'access_token': access_token}, status=status.HTTP_201_CREATED)
            except:
                return Response({'detail': 'Account with email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginWithEmailView(CustomResponseMixin, APIView):
    def post(self, request):
        serializer = LoginWithEmailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                account = Account.objects.get(email=serializer.validated_data['email'])
                if check_password(serializer.validated_data['password'], account.password):
                    access_token = generate_access_token(account)
                    return Response({'email': account.email, 'access_token': access_token}, status=status.HTTP_200_OK)
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except account.DoesNotExist:
                return Response({'detail': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetInitiateView(CustomResponseMixin, APIView):
    def post(self, request):
        serializer = PasswordResetInitiateSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            if not Account.objects.filter(email=email).exists():
                return Response(
                    {'status': 'error', 'message': 'Email does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            otp_code = str(random.randint(100000, 999999))
            expires_at = now() + timedelta(minutes=10)
            OTP.objects.create(email=email, otp_code=otp_code, expires_at=expires_at)
            
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP code is {otp_code}',
                'noreply@example.com',
                [email]
            )
            return Response({'status': 'success', 'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetCompleteView(CustomResponseMixin, APIView):
    def post(self, request):
        serializer = PasswordResetCompleteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                otp = OTP.objects.get(
                    email=serializer.validated_data['email'],
                    otp_code=serializer.validated_data['otp']
                )
                if otp.expires_at < now():
                    logger.warning(f"Expired OTP for {otp.email}")
                    return Response({'status': 'success', 'message': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
                account = Account.objects.get(email=serializer.validated_data['email'])
                account.password = make_password(serializer.validated_data['new_password'])
                account.save()
                otp.delete()
                access_token = generate_access_token(account)
                return Response({'email': account.email, 'access_token': access_token}, status=status.HTTP_200_OK)
            except (OTP.DoesNotExist, Account.DoesNotExist):
                return Response({'status': 'error', 'message': 'Invalid OTP or email'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
