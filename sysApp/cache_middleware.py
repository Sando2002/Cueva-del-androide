"""
Middleware personalizado para gestionar headers de cache en archivos estáticos
"""
from django.http import HttpResponse

class CacheControlMiddleware:
    """
    Middleware para controlar el caché de archivos estáticos en navegadores.
    Esto fuerza la recarga de archivos CSS, JS e imágenes en navegadores móviles.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Archivos estáticos que queremos que NO se cacheen o se cacheen menos
        no_cache_extensions = ['.css', '.js']
        
        # Para archivos CSS y JS, establecer caché corto (1 hora)
        for ext in no_cache_extensions:
            if request.path.endswith(ext):
                # max-age: 3600 = 1 hora
                response['Cache-Control'] = 'public, max-age=3600, must-revalidate'
                response['Pragma'] = 'cache'
                response['Expires'] = 'Thu, 01 Jan 2025 00:00:00 GMT'
                break
        
        # Para imágenes y otros assets, caché de 1 mes
        static_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.woff', '.woff2']
        for ext in static_extensions:
            if request.path.endswith(ext):
                # max-age: 2592000 = 30 días
                response['Cache-Control'] = 'public, max-age=2592000, immutable'
                break
        
        return response
