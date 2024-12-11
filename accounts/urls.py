from django.urls import path
from .views import CreateAccountWithEmailView, LoginWithEmailView, PasswordResetInitiateView, PasswordResetCompleteView

urlpatterns = [
    path('create', CreateAccountWithEmailView.as_view(), name='create_account'),
    path('login', LoginWithEmailView.as_view(), name='login_account'),
    path('reset-password/initiate', PasswordResetInitiateView.as_view(), name='password_reset_initiate'),
    path('reset-password/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
