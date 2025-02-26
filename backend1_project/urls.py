"""
URL configuration for backend1_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# backend1/api/urls.py
from django.urls import path
from .views import HealthCheckView, UserInfoView, Backend2ProxyView, TenantCreationView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health'),
    path('users/', UserInfoView.as_view(), name='users'),
    path('call-backend2/', Backend2ProxyView.as_view(), name='call-backend2'),
    path('create-tenant/', TenantCreationView.as_view(), name='create-tenant'),
]
