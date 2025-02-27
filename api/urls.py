from django.urls import path
from .views import HealthCheckView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health'),
    # We'll add more URLs later
]