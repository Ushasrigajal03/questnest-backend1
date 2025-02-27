# backend1/api/urls.py
from django.urls import path
from .views import HealthCheckView, UserInfoView, Backend2ProxyView, TenantCreationView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health'),
    path('users/', UserInfoView.as_view(), name='users'),
    path('call-backend2/', Backend2ProxyView.as_view(), name='call-backend2'),
    path('create-tenant/', TenantCreationView.as_view(), name='create-tenant'),
]