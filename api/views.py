import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.pdns import PowerDNSClient

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "healthy", "service": "backend1"}, status=status.HTTP_200_OK)

class UserInfoView(APIView):
    def get(self, request):
        return Response({
            "service": "backend1",
            "data": {
                "users": [
                    {"id": 1, "username": "user1", "email": "user1@example.com"},
                    {"id": 2, "username": "user2", "email": "user2@example.com"},
                ]
            }
        })

class Backend2ProxyView(APIView):
    """View to demonstrate backend-to-backend communication"""
    def get(self, request):
        try:
            # Assuming backend2 is accessible via Traefik at this URL
            backend2_url = 'http://backend2.questnest.in/api/info/'
            
            # Forward the request to backend2 with proper API key
            response = requests.get(
                backend2_url,
                headers={'X-API-KEY': 'backend2-secret-key'},
                timeout=5
            )
            
            # Return the data from backend2 along with metadata
            return Response({
                "service": "backend1",
                "proxied_response": response.json(),
                "status": "success"
            })
        except Exception as e:
            return Response({
                "service": "backend1",
                "error": str(e),
                "status": "failed"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TenantCreationView(APIView):
    """View for handling tenant creation"""
    def post(self, request):
        try:
            data = request.data
            username = data.get('username')
            
            if not username:
                return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            # Generate a subdomain for this tenant (in production you'd add more checks)
            import random
            import string
            
            # Generate a random 6-8 character alphanumeric ID
            length = random.randint(6, 8)
            subdomain = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            
            # In production, you would:
            # 1. Call PowerDNS API to create the DNS entry
            # 2. Update Traefik configuration if needed
            # 3. Store the mapping in your database
            
            return Response({
                "service": "backend1",
                "tenant": {
                    "username": username,
                    "subdomain": f"{subdomain}.questnest.in",
                    "created": True
                }
            })
        except Exception as e:
            return Response({
                "service": "backend1",
                "error": str(e),
                "status": "failed"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TenantCreationView(APIView):
    """View for handling tenant creation"""
    def post(self, request):
        try:
            data = request.data
            username = data.get('username')
            
            if not username:
                return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            # Generate a subdomain for this tenant
            import random
            import string
            
            # Generate a random 6-8 character alphanumeric ID
            length = random.randint(6, 8)
            subdomain = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            
            # Create the DNS entry
            pdns_client = PowerDNSClient()
            dns_created = pdns_client.create_subdomain(subdomain)
            
            if not dns_created:
                return Response({
                    "error": "Failed to create DNS entry",
                    "status": "failed"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Save the tenant details in your database
            # tenant = Tenant.objects.create(username=username, subdomain=subdomain)
            
            return Response({
                "service": "backend1",
                "tenant": {
                    "username": username,
                    "subdomain": f"{subdomain}.questnest.in",
                    "created": True
                }
            })
        except Exception as e:
            return Response({
                "service": "backend1",
                "error": str(e),
                "status": "failed"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)