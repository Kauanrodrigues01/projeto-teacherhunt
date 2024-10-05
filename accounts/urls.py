from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenBlacklistView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPI, SendRequestEmailActiveUser, ActiveUser, CustomTokenObtainPairView


app_name = 'accounts'

urlpatterns = [
    path('login', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('logout', CustomTokenBlacklistView.as_view(), name='logout'),
    path('password-reset-request', RequestPasswordResetEmail.as_view(), name='password-reset'),
    path('password-reset/<uidb64>/<token>', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPI.as_view(), name='password-reset-complete'),
    path('send-request-active-user', SendRequestEmailActiveUser.as_view(), name='send-request-active-user'),
    path('active-user/<uidb64>/<token>', ActiveUser.as_view(), name='active-user')
]