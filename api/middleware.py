# backend1/api/middleware.py
from django.http import JsonResponse
from django.conf import settings

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Exclude admin paths
        if request.path.startswith('/admin/'):
            return self.get_response(request)
            
        # Check for API key in header
        api_key = request.headers.get(settings.API_KEY_HEADER)
        
        # Public endpoints that don't require API key
        if request.path == '/api/health/':
            return self.get_response(request)
            
        if not api_key:
            return JsonResponse({'error': 'API key missing'}, status=401)
            
        if api_key != settings.API_KEY:
            return JsonResponse({'error': 'Invalid API key'}, status=403)
            
        return self.get_response(request)