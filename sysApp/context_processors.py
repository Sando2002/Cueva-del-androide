from .models import Carrito, Notificacion
from django.db.models import Sum

def carrito_contador(request):
    """
    Context processor que proporciona el contador del carrito a todos los templates.
    Si el usuario está autenticado, calcula la cantidad total de productos en su carrito.
    Si no está autenticado, devuelve 0.
    """
    carrito_total = 0
    notificaciones_recientes = []
    notificaciones_sin_leer = 0
    
    if request.user.is_authenticated:
        # Obtener la suma de cantidades directamente en la BD (más eficiente)
        resultado = Carrito.objects.filter(usuario=request.user).aggregate(Sum('cantidad'))
        carrito_total = resultado['cantidad__sum'] or 0
        
        # Obtener 3 notificaciones más recientes
        notificaciones_recientes = Notificacion.objects.filter(
            usuario=request.user
        ).order_by('-fecha_creacion')[:3]
        
        # Contar notificaciones sin leer
        notificaciones_sin_leer = Notificacion.objects.filter(
            usuario=request.user,
            leida=False
        ).count()
    
    return {
        'carrito_total': carrito_total,
        'notificaciones_recientes': notificaciones_recientes,
        'notificaciones_sin_leer': notificaciones_sin_leer
    }
