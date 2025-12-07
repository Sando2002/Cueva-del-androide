from django.shortcuts import render, get_object_or_404, redirect
from .models import (Categoria, Producto, Carrito, Pedido, ItemPedido, Notificacion, Auditoria,
                     MovimientoInventario, AuditoriaInventario, DetalleAuditoria, 
                     OrdenCompra, DetalleOrdenCompra)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from .forms import ProductoForm, CustomUserForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, Count, Q, Avg
from django.db import models
from datetime import datetime, timedelta
import json

# ============ FUNCIONES HELPER PARA NOTIFICACIONES ============

def crear_notificacion(usuario, titulo, mensaje, tipo, pedido=None, producto=None):
    """
    Crear una notificación para un usuario.
    
    Parámetros:
    - usuario: Usuario que recibe la notificación
    - titulo: Título corto
    - mensaje: Descripción detallada
    - tipo: Tipo de notificación (choices en modelo)
    - pedido: Pedido relacionado (opcional)
    - producto: Producto relacionado (opcional)
    """
    notificacion = Notificacion.objects.create(
        usuario=usuario,
        titulo=titulo,
        mensaje=mensaje,
        tipo=tipo,
        pedido=pedido,
        producto=producto
    )
    return notificacion


def notificar_pedido_creado(pedido):
    """Notificar al cliente que su pedido fue creado"""
    crear_notificacion(
        usuario=pedido.usuario,
        titulo=f"Pedido #{pedido.numero_pedido} Creado",
        mensaje=f"Tu pedido ha sido creado exitosamente. Total: ${pedido.total} CLP. Por favor procede al pago.",
        tipo='pedido_creado',
        pedido=pedido
    )


def notificar_pedido_cambio_estado(pedido, estado_anterior, estado_nuevo):
    """Notificar al cliente sobre cambio de estado del pedido"""
    mensajes_estado = {
        'en_preparacion': 'Tu pago ha sido confirmado. Tu pedido ya fue pagado y está en preparación.',
        'listo': 'Tu pedido está listo para recoger en nuestras instalaciones.',
        'rechazado': 'Tu pago ha sido rechazado. Por favor intenta de nuevo o contacta con soporte.',
        'cancelado': 'Tu pedido ha sido cancelado.',
    }
    
    tipo_map = {
        'en_preparacion': 'pedido_pagado',
        'listo': 'pedido_procesando',
        'rechazado': 'pedido_rechazado',
        'cancelado': 'pedido_cancelado',
    }
    
    crear_notificacion(
        usuario=pedido.usuario,
        titulo=f"Pedido #{pedido.numero_pedido} - {pedido.get_estado_display()}",
        mensaje=mensajes_estado.get(estado_nuevo, f"El estado de tu pedido cambió a: {pedido.get_estado_display()}"),
        tipo=tipo_map.get(estado_nuevo, 'pedido_procesando'),
        pedido=pedido
    )


def actualizar_stock_pedido(pedido):
    """
    Actualizar el stock de los productos cuando el pago es exitoso.
    Descuenta la cantidad de cada item del pedido del stock del producto.
    """
    items = pedido.items.all()
    print(f"🔥 Actualizando stock para pedido {pedido.numero_pedido}")
    print(f"📦 Items a procesar: {items.count()}")
    
    for item in items:
        if item.producto:
            stock_anterior = item.producto.stock
            # Descontar el stock
            item.producto.stock -= item.cantidad
            item.producto.save()
            
            print(f"✅ Producto '{item.producto.titulo}': {stock_anterior} -> {item.producto.stock} (descuento: {item.cantidad})")
            
            # Notificar si el stock es bajo
            if item.producto.stock <= 5:
                notificar_stock_bajo_admin(item.producto, umbral=5)


def notificar_stock_bajo_admin(producto, umbral=5):
    """Notificar a los admins cuando el stock de un producto baja"""
    admins = Group.objects.get(name='Administrador').user_set.all() if Group.objects.filter(name='Administrador').exists() else []
    
    if not admins:
        admins = [u for u in Group.objects.get(name='Administrador').user_set.all()] if Group.objects.filter(name='Administrador').exists() else []
    
    # Si no hay grupo, notificar a todos los superusers
    if not admins:
        admins = [u for u in User.objects.filter(is_superuser=True)]
    
    for admin in admins:
        crear_notificacion(
            usuario=admin,
            titulo=f"Stock Bajo: {producto.titulo}",
            mensaje=f"El producto '{producto.titulo}' tiene solo {producto.stock} unidades en stock.",
            tipo='stock_bajo',
            producto=producto
        )


# ============ FUNCIONES HELPER PARA AUDITORÍA ============

def obtener_ip_cliente(request):
    """Obtener la dirección IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def registrar_auditoria(request, accion, modelo, objeto_id, descripcion, cambios=None):
    """
    Registrar una acción de auditoría.
    
    Parámetros:
    - request: Request HTTP para obtener usuario e IP
    - accion: Tipo de acción (crear_producto, editar_producto, etc.)
    - modelo: Tipo de modelo (Producto, Pedido, etc.)
    - objeto_id: ID del objeto modificado
    - descripcion: Descripción legible de la acción
    - cambios: Dict con cambios antes/después (opcional)
    """
    Auditoria.objects.create(
        usuario=request.user,
        accion=accion,
        modelo=modelo,
        objeto_id=objeto_id,
        descripcion=descripcion,
        cambios=cambios or {},
        ip_address=obtener_ip_cliente(request)
    )


def registrar_cambios(antes, despues, campos_ignorar=None):
    """
    Comparar dos diccionarios y devolver un dict con los cambios.
    
    Parámetros:
    - antes: Dict con valores anteriores
    - despues: Dict con valores nuevos
    - campos_ignorar: Lista de campos a no incluir
    
    Retorna: Dict con cambios en formato {'campo': {'antes': X, 'despues': Y}}
    """
    campos_ignorar = campos_ignorar or []
    cambios = {}
    
    for campo in despues:
        if campo in campos_ignorar:
            continue
        
        valor_antes = antes.get(campo, 'N/A')
        valor_despues = despues.get(campo, 'N/A')
        
        if valor_antes != valor_despues:
            cambios[campo] = {
                'antes': str(valor_antes),
                'despues': str(valor_despues)
            }
    
    return cambios



# ============ VISTAS PRINCIPALES ============

# Vista para inicio
def inicio(request):
    categorias = Categoria.objects.all()
    return render(request, 'paginas/index.html', {'categorias': categorias})

def es_superusuario(user):
    return user.is_superuser

# Vista para catalogo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def registrar(request):
    from django.contrib.auth.models import User, Group
    storage = messages.get_messages(request)
    storage.used = True
    
    data = {'titulo': 'Registrar Usuario'}
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        
        # Validar que no estén vacíos
        if not username:
            messages.error(request, 'El nombre de usuario es requerido.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        if not email:
            messages.error(request, 'El correo electrónico es requerido.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        if not password1:
            messages.error(request, 'La contraseña es requerida.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        if not password2:
            messages.error(request, 'Debes confirmar la contraseña.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        # Validar que el username no exista
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe. Por favor, intenta con otro.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        # Validar que el email no exista
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado. Por favor, intenta con otro.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        # Validar formato de email
        if '@' not in email or '.' not in email:
            messages.error(request, 'Por favor, ingresa un correo electrónico válido.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        # Validar que las contraseñas coincidan
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        # Validar longitud de contraseña
        if len(password1) < 8:
            messages.error(request, 'Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        # Validar que no sea completamente numérica
        if password1.isdigit():
            messages.error(request, 'Esta contraseña es completamente numérica.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        # Validar que no sea una contraseña común
        contraseñas_comunes = ['123456', 'password', 'qwerty', 'abc123', 'letmein', 'welcome', 'monkey', 'dragon']
        if password1.lower() in contraseñas_comunes:
            messages.error(request, 'Esta contraseña es demasiado común.', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
        
        # Crear el usuario
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            # Agregar al grupo de clientes
            grupo = Group.objects.get(name='clientes')
            user.groups.add(grupo)
            messages.success(request, '¡Usuario creado con éxito! Ahora puedes iniciar sesión.', extra_tags='auth')
            return redirect(to='login')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al crear la cuenta: {str(e)}', extra_tags='auth')
            return render(request, 'registration/registro.html', data)
    
    return render(request, 'registration/registro.html', data)

def catalogo(request):
    productos_list = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos_list = productos_list.filter(categoria_id=categoria_id)
    
    # Filtro por precio
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    
    if precio_min:
        try:
            productos_list = productos_list.filter(precio__gte=int(precio_min))
        except ValueError:
            pass
    
    if precio_max:
        try:
            productos_list = productos_list.filter(precio__lte=int(precio_max))
        except ValueError:
            pass

    paginator = Paginator(productos_list, 12)  # 12 productos por página
    page_number = request.GET.get("page")

    try:
        productos = paginator.page(page_number)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    return render(request, 'paginas/catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'precio_min': precio_min,
        'precio_max': precio_max
    })

# Vista para buscar productos
def buscar_productos(request):
    query = request.GET.get('search', '')
    productos_list = Producto.objects.filter(titulo__icontains=query)
    categorias = Categoria.objects.all()
    
    paginator = Paginator(productos_list, 12)  # 12 productos por página
    page_number = request.GET.get("page")

    try:
        productos = paginator.page(page_number)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    
    return render(request, 'paginas/catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'search_query': query
    })

# Vista para filtrar productos por categoria
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos_list = Producto.objects.filter(categoria=categoria)
    categorias = Categoria.objects.all()
    
    paginator = Paginator(productos_list, 12)  # 12 productos por página
    page_number = request.GET.get("page")

    try:
        productos = paginator.page(page_number)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
    
    return render(request, 'paginas/catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria
    })

# Vista para detalle de producto
def detalleProducto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    # Verificar si hay auditoria en progreso
    auditoria_abierta = AuditoriaInventario.objects.filter(estado='en_proceso').exists()
    
    return render(request, 'paginas/detalleProducto.html', {
        'producto': producto,
        'auditoria_abierta': auditoria_abierta
    })


# Vista para agregar al carrito
@login_required
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    usuario = request.user
    
    # Verificar si hay auditoria en progreso
    auditoria_abierta = AuditoriaInventario.objects.filter(estado='en_proceso').exists()
    if auditoria_abierta:
        messages.error(request, '⚠️ No se pueden agregar productos al carrito durante una auditoría de inventario.', extra_tags='carrito')
        return redirect("detalleProducto", pk=producto_id)
    
    if producto.stock > 0:
        # Buscar si el producto ya está en el carrito del usuario
        carrito_item, creado = Carrito.objects.get_or_create(
            usuario=usuario,
            producto=producto,
            defaults={'cantidad': 1}
        )
        
        if not creado:
            # Si ya existe, aumentar cantidad
            if carrito_item.cantidad < producto.stock:
                carrito_item.cantidad += 1
                carrito_item.save()
                messages.success(request, "Cantidad actualizada en el carrito.", extra_tags='carrito')
            else:
                messages.error(request, "No hay suficiente stock del producto.", extra_tags='carrito')
                return redirect("detalle_carrito")
        else:
            messages.success(request, "Producto agregado al carrito.", extra_tags='carrito')
        
        return redirect("detalle_carrito")
    
    messages.error(request, "No hay suficiente stock del producto.", extra_tags='carrito')
    return redirect("catalogo")


# Vista para ver el detalle del carrito
@login_required
@login_required
def detalle_carrito(request):
    usuario = request.user
    items_carrito = Carrito.objects.filter(usuario=usuario)
    
    # Verificar si hay auditoria en progreso
    auditoria_abierta = AuditoriaInventario.objects.filter(estado='en_proceso').exists()
    if auditoria_abierta:
        messages.error(request, '⚠️ Hay una auditoría de inventario en proceso. No se pueden realizar compras en este momento.', extra_tags='carrito')
    
    # Calcular total de forma eficiente sumando (precio * cantidad) en la BD
    total_carrito = 0
    for item in items_carrito:
        total_carrito += item.subtotal()

    return render(
        request,
        "paginas/detalle_carrito.html",
        {
            "items_carrito": items_carrito, 
            "total_carrito": total_carrito,
            "auditoria_abierta": auditoria_abierta
        },
    )

# Vista para eliminar un producto del carrito
@login_required
def eliminar_del_carrito(request, item_id):
    usuario = request.user
    carrito_item = get_object_or_404(Carrito, id=item_id, usuario=usuario)
    carrito_item.delete()
    messages.success(request, "Producto eliminado del carrito.", extra_tags='carrito')
    return redirect("detalle_carrito")

# Vista para actualizar la cantidad de un producto en el carrito
@login_required
def actualizar_cantidad(request, item_id):
    if request.method == 'POST':
        usuario = request.user
        carrito_item = get_object_or_404(Carrito, id=item_id, usuario=usuario)
        producto = carrito_item.producto
        accion = request.POST.get('accion')
        
        if accion == 'incrementar':
            if carrito_item.cantidad < producto.stock:
                carrito_item.cantidad += 1
                carrito_item.save()
                messages.success(request, "Cantidad incrementada.", extra_tags='carrito')
            else:
                messages.error(request, "No hay suficiente stock.", extra_tags='carrito')
                
        elif accion == 'decrementar':
            if carrito_item.cantidad > 1:
                carrito_item.cantidad -= 1
                carrito_item.save()
                messages.success(request, "Cantidad decrementada.", extra_tags='carrito')
            else:
                messages.error(request, "La cantidad mínima es 1.", extra_tags='carrito')
        
    return redirect('detalle_carrito')

# Vista para login
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login 
def login_view(request):
    from django.contrib.auth.models import User
    storage = messages.get_messages(request)
    storage.used = True
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Verificar si el usuario existe
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario no existe. Por favor, verifica o regístrate.', extra_tags='auth')
            return render(request, 'registration/login.html')
        
        # Intentar autenticar
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {username}!', extra_tags='auth')
            return redirect('inicio')
        else:
            messages.error(request, 'La contraseña es incorrecta. Por favor, intenta de nuevo.', extra_tags='auth')
            return render(request, 'registration/login.html')
    
    return render(request, 'registration/login.html')

# Vista para logout
def logout_view(request):
    logout(request)
    return redirect('inicio')

# Vista para modificar producto
@user_passes_test(es_superusuario)
@login_required
# Vista para editar producto
@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    # Capturar parámetros de filtro para mantenerlos después de guardar
    categoria_id = request.GET.get('categoria', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            # Guardar datos anteriores para auditoría
            datos_anteriores = {
                'titulo': producto.titulo,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'categoria': str(producto.categoria) if producto.categoria else None,
            }
            
            # Guardar el stock ANTES de cualquier cambio
            stock_original = producto.stock
            
            # Guardar el formulario
            form.save()
            
            # FORZAR restaurar el stock original para asegurar que NO se modifique
            producto.stock = stock_original
            producto.save(update_fields=['stock'])
            
            # Registrar cambios en auditoría
            datos_nuevos = {
                'titulo': producto.titulo,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'categoria': str(producto.categoria) if producto.categoria else None,
            }
            
            cambios = registrar_cambios(datos_anteriores, datos_nuevos)
            registrar_auditoria(
                request,
                accion='editar_producto',
                modelo='Producto',
                objeto_id=producto.id,
                descripcion=f'Editó el producto "{producto.titulo}"',
                cambios=cambios
            )
            
            messages.success(request, f'Producto {producto.titulo} actualizado exitosamente. El stock se gestiona desde el módulo de Inventario.')
            
            # Redirigir con los parámetros de filtro
            redirect_url = reverse('admin_productos')
            query_params = []
            if categoria_id:
                query_params.append(f'categoria={categoria_id}')
            if precio_min:
                query_params.append(f'precio_min={precio_min}')
            if precio_max:
                query_params.append(f'precio_max={precio_max}')
            
            if query_params:
                redirect_url += '?' + '&'.join(query_params)
            
            return redirect(redirect_url)
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'paginas/editar_producto.html', {
        'form': form,
        'producto': producto,
        'categoria_id': categoria_id,
        'precio_min': precio_min,
        'precio_max': precio_max,
    })

# Vista para eliminar producto
@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        # Registrar la eliminación en auditoría ANTES de eliminar
        registrar_auditoria(
            request,
            accion='eliminar_producto',
            modelo='Producto',
            objeto_id=producto.id,
            descripcion=f'Eliminó el producto "{producto.titulo}" (Precio: ${producto.precio}, Stock: {producto.stock})'
        )
        
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('admin_productos')
    return render(request, 'paginas/eliminar_producto.html', {'producto': producto})

    
# Página estática: Política de Privacidad
def politica_privacidad(request):
    return render(request, 'paginas/politica_privacidad.html')



# Página estática: Términos y Condiciones
def terminos_condiciones(request):
    return render(request, 'paginas/terminos_condiciones.html')


# Página estática: Política de Devoluciones
def politica_devoluciones(request):
    return render(request, 'paginas/politica_devoluciones.html')


# Página estática: Política de Envíos
def politica_envios(request):
    return render(request, 'paginas/politica_envios.html')

# Vista para obtener el contador del carrito en JSON
@login_required
def get_carrito_count(request):
    """
    Devuelve la cantidad total de productos en el carrito del usuario autenticado.
    Responde en formato JSON para ser usado por JavaScript.
    """
    usuario = request.user
    resultado = Carrito.objects.filter(usuario=usuario).aggregate(Sum('cantidad'))
    total = resultado['cantidad__sum'] or 0
    
    return JsonResponse({
        'total': total,
        'success': True
    })


# ==================== VISTAS DE PAGO CON MERCADO PAGO ====================

import mercadopago
from django.conf import settings
import uuid
from datetime import datetime
from django.views.decorators.http import require_http_methods
import json

@login_required
def checkout_mercadopago(request):
    """
    Crea una preferencia de pago en Mercado Pago y redirige al usuario.
    """
    print("=== INICIANDO CHECKOUT MERCADOPAGO ===")
    usuario = request.user
    print(f"Usuario: {usuario}")
    
    # ✅ Verificar que no haya auditoria abierta
    auditoria_abierta = AuditoriaInventario.objects.filter(estado='en_proceso').exists()
    if auditoria_abierta:
        messages.error(request, '⚠️ No se pueden realizar compras mientras hay una auditoría de inventario en proceso. Por favor intenta más tarde.', extra_tags='carrito')
        return redirect('detalle_carrito')
    
    items_carrito = Carrito.objects.filter(usuario=usuario)
    print(f"Items en carrito: {items_carrito.count()}")
    
    if not items_carrito.exists():
        print("Carrito vacío")
        messages.error(request, 'Tu carrito está vacío.', extra_tags='carrito')
        return redirect('detalle_carrito')
    
    # Calcular total
    resultado = items_carrito.aggregate(total=Sum(F('cantidad') * F('producto__precio')))
    total = resultado['total'] or 0
    print(f"Total calculado: {total}")
    
    if total <= 0:
        print("Total inválido")
        messages.error(request, 'Total inválido.', extra_tags='carrito')
        return redirect('detalle_carrito')
    
    # Crear número de pedido único
    numero_pedido = f"PED-{uuid.uuid4().hex[:8].upper()}"
    
    try:
        # Crear pedido en base de datos
        pedido = Pedido.objects.create(
            usuario=usuario,
            numero_pedido=numero_pedido,
            total=total,
            estado='pendiente'
        )
        
        # Crear items del pedido (copia de carrito para histórico)
        for item in items_carrito:
            ItemPedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio
            )
        
        # ✅ Crear notificación de pedido creado
        notificar_pedido_creado(pedido)
        
        # Configurar SDK de Mercado Pago
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        # Construir URLs de retorno (usar ngrok en desarrollo)
        # Si estamos en ngrok, usar esa URL; si no, usar la URL del request
        if 'ngrok' in request.get_host():
            base_url = f"https://{request.get_host()}"
        else:
            base_url = request.build_absolute_uri('/').rstrip('/')
        
        print(f"Base URL para back_urls: {base_url}")
        
        # Construir preference
        preference_data = {
            "items": [
                {
                    "title": item.producto.titulo,
                    "quantity": item.cantidad,
                    "unit_price": float(item.producto.precio),
                    "currency_id": "CLP"  # Cambiar según tu país
                }
                for item in items_carrito
            ],
            "payer": {
                "email": usuario.email or f"{usuario.username}@tienda.local"
            },
            "back_urls": {
                "success": f"{base_url}/mis-pedidos/",
                "failure": f"{base_url}/pago/fallo/",
                "pending": f"{base_url}/pago/pendiente/"
            },
        #   "notification_url": request.build_absolute_uri('/api/mercadopago/webhook/'),
            "external_reference": numero_pedido
        }
        
        # Crear preferencia
        response = sdk.preference().create(preference_data)
        
        print(f"Response status: {response.get('status')}")
        print(f"Response: {response}")
        
        # Validar respuesta (a veces es 'status' a veces es 'code')
        status = response.get("status") or response.get("code")
        
        if status == 201 or (response.get("response") and response["response"].get("id")):
            init_point = None
            preferencia_id = None
            
            if response.get("response"):
                init_point = response["response"].get("init_point")
                preferencia_id = response["response"].get("id")
            
            if init_point and preferencia_id:
                pedido.preferencia_id = preferencia_id
                pedido.save()
                
                # Limpiar carrito después de crear el pedido
                items_carrito.delete()
                
                messages.success(request, 'Redirigiendo a Mercado Pago...', extra_tags='carrito')
                # Redirigir a Mercado Pago
                return redirect(init_point)
            else:
                error_msg = "No se pudo obtener el init_point de Mercado Pago"
                print(f"Error: {error_msg}")
                messages.error(request, f'Error: {error_msg}', extra_tags='carrito')
                pedido.delete()
                return redirect('detalle_carrito')
        else:
            # Si la respuesta no es válida, mostrar error
            error_msg = response.get("response", {}).get("message", "Error desconocido al crear la preferencia")
            print(f"Error: {error_msg}")
            messages.error(request, f'Error: {error_msg}', extra_tags='carrito')
            pedido.delete()
            return redirect('detalle_carrito')
    
    except Exception as e:
        print(f"Exception en checkout_mercadopago: {str(e)}")
        import traceback
        traceback.print_exc()
        messages.error(request, f'Error al procesar el pago: {str(e)}', extra_tags='carrito')
        # Eliminar el pedido si ocurrió un error
        try:
            Pedido.objects.filter(numero_pedido=numero_pedido).delete()
        except:
            pass
        return redirect('detalle_carrito')


@login_required
def pago_exito(request):
    """
    Página de éxito del pago. Se muestra cuando el usuario retorna desde MP.
    Aquí se actualiza el estado del pedido a en_preparacion y se descuenta el stock.
    """
    payment_id = request.GET.get('payment_id')
    external_reference = request.GET.get('external_reference')
    
    # Debug
    print(f"=== PAGO EXITO ===")
    print(f"Payment ID: {payment_id}")
    print(f"External Reference: {external_reference}")
    print(f"GET params: {request.GET}")
    
    # Buscar el pedido
    pedido = None
    if external_reference:
        pedido = Pedido.objects.filter(numero_pedido=external_reference).first()
        print(f"Pedido encontrado: {pedido}")
        if pedido:
            print(f"Estado anterior: {pedido.estado}")
        
        # Si el pedido existe y aún está en estado pendiente, cambiar a en_preparacion
        if pedido and pedido.estado == 'pendiente':
            pedido.estado = 'en_preparacion'
            pedido.save()
            
            # 🔥 Actualizar stock de los productos comprados
            actualizar_stock_pedido(pedido)
            
            # ✅ Notificar cambio de estado a en_preparacion
            notificar_pedido_cambio_estado(pedido, 'pendiente', 'en_preparacion')
            print(f"Estado actualizado a: {pedido.estado}")
        else:
            print(f"Pedido no actualizado. Estado actual: {pedido.estado if pedido else 'Sin pedido'}")
    else:
        print(f"No se encontró external_reference en los parámetros")
    
    context = {
        'pedido': pedido,
        'payment_id': payment_id
    }
    
    return render(request, 'paginas/pago_exito.html', context)


@login_required
def pago_fallo(request):
    """
    Página de fallo del pago.
    Se muestra cuando el usuario cancela el pago o es rechazado.
    El pedido se mantiene en estado 'pendiente' para poder reintentar.
    """
    external_reference = request.GET.get('external_reference')
    
    # Buscar el pedido
    pedido = None
    if external_reference:
        pedido = Pedido.objects.filter(numero_pedido=external_reference).first()
        
        # El pedido se mantiene en 'pendiente' para poder reintentar
        # No lo cambiamos a 'rechazado' porque el usuario puede reintentar
        print(f"Pago fallo/cancelado para pedido {pedido.numero_pedido} - Estado: {pedido.estado if pedido else 'Sin pedido'}")
    
    context = {
        'pedido': pedido
    }
    
    return render(request, 'paginas/pago_fallo.html', context)


@login_required
def reintentar_pago(request, pedido_id):
    """
    Reintentar el pago de un pedido.
    Redirige directamente a Mercado Pago sin pasar por el carrito.
    Funciona con pedidos en estado 'pendiente' (cancelados o rechazados).
    """
    usuario = request.user
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=usuario, estado='pendiente')
    
    print(f"=== REINTENTANDO PAGO PARA PEDIDO {pedido.numero_pedido} ===")
    
    try:
        # Configurar SDK de Mercado Pago
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        # Construir URLs de retorno
        if 'ngrok' in request.get_host():
            base_url = f"https://{request.get_host()}"
        else:
            base_url = request.build_absolute_uri('/').rstrip('/')
        
        # Obtener items del pedido
        items = pedido.items.all()
        if not items.exists():
            messages.error(request, 'El pedido no tiene items.', extra_tags='carrito')
            return redirect('mis_pedidos')
        
        # Construir preference
        preference_data = {
            "items": [
                {
                    "title": item.producto.titulo,
                    "quantity": item.cantidad,
                    "unit_price": float(item.precio_unitario),
                    "currency_id": "CLP"
                }
                for item in items
            ],
            "payer": {
                "email": usuario.email or f"{usuario.username}@tienda.local"
            },
            "back_urls": {
                "success": f"{base_url}/mis-pedidos/",
                "failure": f"{base_url}/pago/fallo/",
                "pending": f"{base_url}/pago/pendiente/"
            },
            "external_reference": pedido.numero_pedido
        }
        
        # Crear preferencia
        response = sdk.preference().create(preference_data)
        status = response.get("status") or response.get("code")
        
        if status == 201 or (response.get("response") and response["response"].get("id")):
            init_point = None
            preferencia_id = None
            
            if response.get("response"):
                init_point = response["response"].get("init_point")
                preferencia_id = response["response"].get("id")
            
            if init_point and preferencia_id:
                # Actualizar el pedido con la nueva preferencia
                pedido.preferencia_id = preferencia_id
                pedido.save()
                
                print(f"Reintentando pago para {pedido.numero_pedido}, nuevo preferencia_id: {preferencia_id}")
                messages.success(request, 'Redirigiendo a Mercado Pago...', extra_tags='carrito')
                return redirect(init_point)
            else:
                error_msg = "No se pudo obtener el init_point de Mercado Pago"
                messages.error(request, f'Error: {error_msg}', extra_tags='carrito')
                return redirect('mis_pedidos')
        else:
            error_msg = response.get("response", {}).get("message", "Error desconocido")
            messages.error(request, f'Error: {error_msg}', extra_tags='carrito')
            return redirect('mis_pedidos')
    
    except Exception as e:
        print(f"Error en reintentar_pago: {str(e)}")
        messages.error(request, f'Error al procesar el pago: {str(e)}', extra_tags='carrito')
        return redirect('mis_pedidos')


@login_required


@login_required
def pago_pendiente(request):
    """
    Página de pago pendiente.
    El stock NO se descuenta cuando el pago está pendiente.
    """
    external_reference = request.GET.get('external_reference')
    
    # Buscar el pedido
    pedido = None
    if external_reference:
        pedido = Pedido.objects.filter(numero_pedido=external_reference).first()
    
    context = {
        'pedido': pedido
    }
    
    return render(request, 'paginas/pago_pendiente.html', context)


@login_required
def verificar_pago(request, preferencia_id):
    """
    Verifica el estado del pago usando el preferencia_id.
    Útil cuando el usuario está en la página de éxito de MP pero no ha sido redirigido.
    """
    try:
        # Buscar el pedido por preferencia_id
        pedido = Pedido.objects.filter(preferencia_id=preferencia_id, usuario=request.user).first()
        
        if not pedido:
            return JsonResponse({'status': 'error', 'message': 'Pedido no encontrado'}, status=404)
        
        # Si ya está en preparación, no hacer nada
        if pedido.estado == 'en_preparacion':
            return JsonResponse({'status': 'success', 'estado': 'en_preparacion', 'message': 'Pedido ya en preparación'})
        
        # Consultar MP para obtener el estado del pago
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        # Obtener los pagos de esta preferencia
        filters = {
            'preference_id': preferencia_id
        }
        search_result = sdk.payment().search(filters)
        
        if search_result['status'] == 200 and search_result['response']['results']:
            # Obtener el pago más reciente
            payment = search_result['response']['results'][0]
            payment_status = payment.get('status')
            
            # Si el pago está aprobado, actualizar el pedido
            if payment_status == 'approved':
                pedido.estado = 'en_preparacion'
                pedido.payment_id = payment.get('id')
                pedido.fecha_pago = datetime.now()
                pedido.save()
                
                # 🔥 Actualizar stock de los productos comprados
                actualizar_stock_pedido(pedido)
                
                # ✅ Notificar cambio de estado a en_preparacion
                notificar_pedido_cambio_estado(pedido, 'pendiente', 'en_preparacion')
                
                return JsonResponse({'status': 'success', 'estado': 'en_preparacion', 'message': 'Pago confirmado'})
            elif payment_status == 'pending':
                return JsonResponse({'status': 'pending', 'estado': 'pendiente', 'message': 'Pago en proceso'})
            else:
                return JsonResponse({'status': 'failed', 'estado': payment_status, 'message': f'Estado: {payment_status}'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No se pudo obtener el estado del pago'}, status=400)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def mercadopago_webhook(request):
    """
    Webhook para recibir notificaciones de Mercado Pago.
    Actualiza el estado del pedido según el resultado del pago.
    """
    print("=== WEBHOOK RECIBIDO ===")
    print(f"Método: {request.method}")
    print(f"Body: {request.body}")
    
    try:
        # Obtener data del webhook
        data = json.loads(request.body) if request.body else {}
        print(f"Data parseada: {data}")
        
        # Tipos de notificación que nos interesan
        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')
            print(f"Payment ID: {payment_id}")
            
            if payment_id:
                # Obtener info del pago de MP
                sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
                response = sdk.payment().get(payment_id)
                print(f"Response de MP: {response}")
                
                if response["status"] == 200:
                    payment_info = response["response"]
                    external_reference = payment_info.get('external_reference')
                    print(f"External Reference: {external_reference}")
                    
                    # Buscar el pedido
                    pedido = Pedido.objects.filter(numero_pedido=external_reference).first()
                    print(f"Pedido encontrado: {pedido}")
                    
                    if pedido:
                        pedido.payment_id = payment_id
                        
                        # Actualizar estado según el status del pago
                        status = payment_info.get('status')
                        print(f"Status de pago: {status}")
                        
                        if status == 'approved':
                            pedido.estado = 'en_preparacion'
                            pedido.fecha_pago = datetime.now()
                            print(f"Pedido actualizado a en_preparacion")
                            # ✅ Notificar cambio de estado a en_preparacion
                            notificar_pedido_cambio_estado(pedido, 'pendiente', 'en_preparacion')
                            
                            # 🔥 Actualizar stock de los productos comprados
                            actualizar_stock_pedido(pedido)
                        
                        elif status == 'pending':
                            pedido.estado = 'listo'
                        
                        elif status in ['rejected', 'cancelled']:
                            pedido.estado = 'rechazado'
                        
                        pedido.save()
        
        return JsonResponse({'status': 'ok'}, status=200)
    
    except Exception as e:
        print(f"Error en webhook: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# ==================== VISTA DE MIS PEDIDOS ====================

@login_required
def mis_pedidos(request):
    """
    Muestra todos los pedidos del usuario actual, filtrados por estado.
    Verifica automáticamente los pedidos pendientes con Mercado Pago.
    """
    usuario = request.user
    
    # Si viene desde Mercado Pago con parámetros, procesar directamente
    payment_id = request.GET.get('payment_id')
    external_reference = request.GET.get('external_reference')
    collection_status = request.GET.get('collection_status')
    
    print(f"\n=== MIS_PEDIDOS - Parámetros de MP ===")
    print(f"payment_id: {payment_id}")
    print(f"external_reference: {external_reference}")
    print(f"collection_status: {collection_status}")
    
    if payment_id and external_reference and collection_status == 'approved':
        print(f"✅ Pago aprobado detectado - Cambiando estado a en_preparacion")
        try:
            # Buscar el pedido
            pedido = Pedido.objects.filter(numero_pedido=external_reference, usuario=usuario).first()
            print(f"Pedido encontrado: {pedido}")
            
            if pedido and pedido.estado == 'pendiente':
                print(f"Actualizando pedido {pedido.numero_pedido}...")
                # Actualizar inmediatamente
                pedido.estado = 'en_preparacion'
                pedido.payment_id = payment_id
                pedido.fecha_pago = datetime.now()
                pedido.save()
                
                print(f"Pedido guardado, ahora actualizando stock...")
                # 🔥 Actualizar stock de los productos comprados
                actualizar_stock_pedido(pedido)
                
                # ✅ Notificar cambio de estado a en_preparacion
                notificar_pedido_cambio_estado(pedido, 'pendiente', 'en_preparacion')
                print(f"✅ Pedido {external_reference} actualizado a en_preparacion desde URL con stock actualizado")
            else:
                print(f"Pedido no actualizado. Estado: {pedido.estado if pedido else 'NO ENCONTRADO'}")
        except Exception as e:
            print(f"❌ Error al actualizar pedido desde URL: {e}")
            import traceback
            traceback.print_exc()
    
    # Verificar otros pedidos pendientes con Mercado Pago
    pedidos_pendientes = Pedido.objects.filter(usuario=usuario, estado='pendiente', preferencia_id__isnull=False)
    
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    for pedido in pedidos_pendientes:
        try:
            # Buscar pagos con esta preferencia
            filters = {'preference_id': pedido.preferencia_id}
            search_result = sdk.payment().search(filters)
            
            if search_result['status'] == 200 and search_result['response']['results']:
                # Obtener el pago más reciente
                payment = search_result['response']['results'][0]
                payment_status = payment.get('status')
                
                # Si el pago está aprobado, actualizar
                if payment_status == 'approved':
                    pedido.estado = 'en_preparacion'
                    pedido.payment_id = payment.get('id')
                    pedido.fecha_pago = datetime.now()
                    pedido.save()
                    
                    # 🔥 Actualizar stock de los productos comprados
                    actualizar_stock_pedido(pedido)
                    
                    # ✅ Notificar cambio de estado a en_preparacion
                    notificar_pedido_cambio_estado(pedido, 'pendiente', 'en_preparacion')
                    print(f"✅ Pedido {pedido.numero_pedido} actualizado a en_preparacion vía SDK")
        except Exception as e:
            # Si hay error, continuar sin actualizar
            print(f"⚠️ Error verificando pedido {pedido.numero_pedido}: {e}")
    
    # Obtener estado desde parámetro GET (por defecto 'todos')
    estado_filtro = request.GET.get('estado', 'todos')
    
    # Obtener todos los pedidos del usuario
    if estado_filtro == 'todos':
        pedidos = Pedido.objects.filter(usuario=usuario).order_by('-fecha_creacion')
    else:
        pedidos = Pedido.objects.filter(usuario=usuario, estado=estado_filtro).order_by('-fecha_creacion')
    
    # Agrupar por estado para mostrar contadores
    contadores = {
        'en_preparacion': Pedido.objects.filter(usuario=usuario, estado='en_preparacion').count(),
        'listo': Pedido.objects.filter(usuario=usuario, estado='listo').count(),
        'recogido': Pedido.objects.filter(usuario=usuario, estado='recogido').count(),
        'pendiente': Pedido.objects.filter(usuario=usuario, estado='pendiente').count(),
        'rechazado': Pedido.objects.filter(usuario=usuario, estado='rechazado').count(),
        'cancelado': Pedido.objects.filter(usuario=usuario, estado='cancelado').count(),
        'total': Pedido.objects.filter(usuario=usuario).count(),
    }
    
    context = {
        'pedidos': pedidos,
        'contadores': contadores,
        'estado_filtro': estado_filtro,
        'estados_disponibles': [
            ('todos', 'Todos'),
            ('en_preparacion', 'En Preparación'),
            ('listo', 'Listo para Recoger'),
            ('recogido', 'Recogidos'),
            ('pendiente', 'Pendientes'),
            ('rechazado', 'Rechazados'),
            ('cancelado', 'Cancelados'),
        ]
    }
    
    return render(request, 'paginas/mis_pedidos.html', context)


# ==================== VISTA DE MI CUENTA ====================

@login_required
def mi_cuenta(request):
    """
    Página de inicio de Mi Cuenta con menú de opciones.
    """
    usuario = request.user
    
    # Contar pedidos por estado
    contadores = {
        'en_preparacion': Pedido.objects.filter(usuario=usuario, estado='en_preparacion').count(),
        'listo': Pedido.objects.filter(usuario=usuario, estado='listo').count(),
        'total': Pedido.objects.filter(usuario=usuario).count(),
    }
    
    context = {
        'usuario': usuario,
        'contadores': contadores,
    }
    
    return render(request, 'paginas/mi_cuenta.html', context)


@login_required
def editar_perfil(request):
    """
    Permite editar los datos del perfil del usuario.
    """
    usuario = request.user
    
    if request.method == 'POST':
        # Obtener datos del formulario
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Validar email único (excepto el actual)
        from django.contrib.auth.models import User
        if User.objects.filter(email=email).exclude(id=usuario.id).exists():
            messages.error(request, 'Este correo electrónico ya está en uso.', extra_tags='perfil')
        else:
            # Actualizar usuario
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email
            usuario.save()
            
            messages.success(request, '¡Perfil actualizado correctamente!', extra_tags='perfil')
            return redirect('mi_cuenta')
    
    context = {
        'usuario': usuario,
    }
    
    return render(request, 'paginas/editar_perfil.html', context)


# Vista para recuperar contraseña (sin requerir autenticación)
def recuperar_contraseña(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        try:
            from django.contrib.auth.models import User
            usuario = User.objects.get(username=username, email=email)
            
            # Generar contraseña temporal
            from django.utils.crypto import get_random_string
            nueva_contraseña = get_random_string(12)
            usuario.set_password(nueva_contraseña)
            usuario.save()
            
            # Guardar contraseña temporal en sesión para mostrarla (desarrollo)
            request.session['nueva_contraseña'] = nueva_contraseña
            request.session['usuario_recuperado'] = username
            
            # Intentar enviar email
            from django.core.mail import send_mail
            try:
                send_mail(
                    'Tu nueva contraseña - Cueva del Androide',
                    f'Tu nueva contraseña es: {nueva_contraseña}\n\nPor favor cámbiala después de iniciar sesión.',
                    'noreply@cuevaandroides.com',
                    [email],
                    fail_silently=False,
                )
            except:
                pass  # Si el email falla, continuamos de todas formas
            
            return redirect('recuperar_contraseña_confirmacion')
        except User.DoesNotExist:
            messages.error(request, 'El usuario y email no coinciden')
    
    return render(request, 'registration/recuperar_contraseña.html')


def recuperar_contraseña_confirmacion(request):
    nueva_contraseña = request.session.get('nueva_contraseña')
    usuario_recuperado = request.session.get('usuario_recuperado')
    
    if not nueva_contraseña:
        return redirect('recuperar_contraseña')
    
    context = {
        'nueva_contraseña': nueva_contraseña,
        'usuario_recuperado': usuario_recuperado,
    }
    
    return render(request, 'registration/recuperar_contraseña_confirmacion.html', context)


def cambiar_contraseña_temporal(request):
    """Cambiar contraseña temporal por una permanente sin requerir autenticación"""
    usuario_recuperado = request.session.get('usuario_recuperado')
    nueva_contraseña_temporal = request.session.get('nueva_contraseña')
    
    if not usuario_recuperado or not nueva_contraseña_temporal:
        messages.error(request, 'Sesión expirada. Por favor, recupera tu contraseña nuevamente.')
        return redirect('recuperar_contraseña')
    
    if request.method == 'POST':
        contraseña_nueva = request.POST.get('nueva_contraseña')
        confirmar_contraseña = request.POST.get('confirmar_contraseña')
        
        # Validaciones
        if not contraseña_nueva or not confirmar_contraseña:
            messages.error(request, 'Por favor, completa todos los campos.')
            return render(request, 'registration/cambiar_contraseña_temporal.html')
        
        if contraseña_nueva != confirmar_contraseña:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registration/cambiar_contraseña_temporal.html')
        
        if len(contraseña_nueva) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return render(request, 'registration/cambiar_contraseña_temporal.html')
        
        try:
            from django.contrib.auth.models import User
            usuario = User.objects.get(username=usuario_recuperado)
            usuario.set_password(contraseña_nueva)
            usuario.save()
            
            # Limpiar sesión
            if 'nueva_contraseña' in request.session:
                del request.session['nueva_contraseña']
            if 'usuario_recuperado' in request.session:
                del request.session['usuario_recuperado']
            
            messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Error al actualizar la contraseña. Por favor, intenta nuevamente.')
    
    context = {
        'usuario_recuperado': usuario_recuperado,
    }
    
    return render(request, 'registration/cambiar_contraseña_temporal.html', context)


# Cancelar pedido
@login_required
def cancelar_pedido(request, pedido_id):
    """Cancelar un pedido (cliente solo puede cancelar pendiente o en_preparacion)"""
    # Aceptar GET o POST, pero solo procesar si es POST
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('mis_pedidos')
    
    try:
        pedido = Pedido.objects.get(id=pedido_id, usuario=request.user)
        
        # Solo se puede cancelar si está en estado pendiente o en_preparacion
        if pedido.estado not in ['pendiente', 'en_preparacion']:
            messages.error(request, 'Solo puedes cancelar pedidos pendientes de pago o en preparación.')
            return redirect('mis_pedidos')
        
        # Cambiar estado a cancelado
        estado_anterior = pedido.estado
        pedido.estado = 'cancelado'
        pedido.save()
        
        # ✅ Notificar cambio de estado
        notificar_pedido_cambio_estado(pedido, estado_anterior, 'cancelado')
        
        messages.success(request, 'Pedido cancelado correctamente.')
        return redirect('mis_pedidos')
    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido no encontrado o no puedes cancelarlo.')
        return redirect('mis_pedidos')


# Reintentar pago
@login_required
def reintentar_pago(request, pedido_id):
    """Reintentar el pago de un pedido pendiente"""
    try:
        pedido = Pedido.objects.get(id=pedido_id, usuario=request.user, estado='pendiente')
        
        # Obtener items del pedido
        items_pedido = ItemPedido.objects.filter(pedido=pedido)
        
        if not items_pedido.exists():
            messages.error(request, 'El pedido no tiene items.')
            return redirect('mis_pedidos')
        
        # Configurar SDK de Mercado Pago
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        # Construir URLs de retorno (usar ngrok en desarrollo)
        if 'ngrok' in request.get_host():
            base_url = f"https://{request.get_host()}"
        else:
            base_url = request.build_absolute_uri('/').rstrip('/')
        
        # Construir nueva preferencia
        preference_data = {
            "items": [
                {
                    "title": item.producto.titulo,
                    "quantity": item.cantidad,
                    "unit_price": float(item.producto.precio),
                    "currency_id": "CLP"
                }
                for item in items_pedido
            ],
            "payer": {
                "email": request.user.email or f"{request.user.username}@tienda.local"
            },
            "back_urls": {
                "success": f"{base_url}/mis-pedidos/",
                "failure": f"{base_url}/pago/fallo/",
                "pending": f"{base_url}/pago/pendiente/"
            },
            "external_reference": pedido.numero_pedido
        }
        
        # Crear preferencia
        response = sdk.preference().create(preference_data)
        
        # Validar respuesta
        status = response.get("status") or response.get("code")
        
        if status == 201 or (response.get("response") and response["response"].get("id")):
            init_point = None
            preferencia_id = None
            
            if response.get("response"):
                init_point = response["response"].get("init_point")
                preferencia_id = response["response"].get("id")
            
            if init_point and preferencia_id:
                # Actualizar el pedido con la nueva preferencia
                pedido.preferencia_id = preferencia_id
                pedido.save()
                
                messages.success(request, 'Redirigiendo a Mercado Pago...', extra_tags='carrito')
                # Redirigir a Mercado Pago
                return redirect(init_point)
            else:
                error_msg = "No se pudo obtener el init_point de Mercado Pago"
                messages.error(request, f'Error: {error_msg}', extra_tags='carrito')
                return redirect('mis_pedidos')
        else:
            error_msg = response.get("response", {}).get("message", "Error desconocido al crear la preferencia")
            messages.error(request, f'Error: {error_msg}', extra_tags='carrito')
            return redirect('mis_pedidos')
    
    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido no encontrado.')
        return redirect('mis_pedidos')
    except Exception as e:
        messages.error(request, f'Error al procesar el pago: {str(e)}', extra_tags='carrito')
        return redirect('mis_pedidos')


@login_required
def marcar_pedido_recogido(request, pedido_id):
    """Marca un pedido como recogido por el cliente (solo si está en estado 'listo')"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=400)
    
    try:
        pedido = Pedido.objects.get(id=pedido_id, usuario=request.user)
        
        # Solo se puede marcar como recogido si está en estado 'listo'
        if pedido.estado != 'listo':
            return JsonResponse({
                'status': 'error',
                'message': f'No puedes marcar este pedido como recogido. Debe estar en estado "Listo para Recoger".'
            }, status=400)
        
        # Cambiar estado a recogido
        estado_anterior = pedido.estado
        pedido.estado = 'recogido'
        pedido.save()
        
        # ✅ Registrar en auditoría
        registrar_auditoria(
            request,
            accion='marcar_pedido_recogido',
            modelo='Pedido',
            objeto_id=pedido.id,
            descripcion=f'Cliente marcó el pedido #{pedido.numero_pedido} como recogido',
            cambios={'estado': {'antes': estado_anterior, 'despues': 'recogido'}}
        )
        
        # ✅ Notificar cambio de estado
        notificar_pedido_cambio_estado(pedido, estado_anterior, 'recogido')
        
        return JsonResponse({
            'status': 'success',
            'message': 'Pedido marcado como recogido correctamente',
            'nuevo_estado': 'recogido'
        })
    
    except Pedido.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Pedido no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error al marcar pedido como recogido: {str(e)}'
        }, status=500)


# ===== PANEL DE ADMINISTRACIÓN =====

@login_required
def panel_admin(request):
    """Panel principal de administración"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para acceder al panel de administración.')
        return redirect('inicio')
    
    # Estadísticas
    total_productos = Producto.objects.count()
    total_pedidos = Pedido.objects.count()
    total_categorias = Categoria.objects.count()
    productos_bajo_stock = Producto.objects.filter(stock__lte=F('stock_minimo')).count()
    
    # Pedidos recientes
    pedidos_recientes = Pedido.objects.all().order_by('-fecha_creacion')[:10]
    
    contexto = {
        'total_productos': total_productos,
        'total_pedidos': total_pedidos,
        'total_categorias': total_categorias,
        'productos_bajo_stock': productos_bajo_stock,
        'pedidos_recientes': pedidos_recientes,
    }
    return render(request, 'admin/panel_admin.html', contexto)


@login_required
def admin_productos(request):
    """Gestión de productos con filtros y creación"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permiso.')
        return redirect('inicio')
    
    # Manejar POST para crear producto
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # El ProductoForm NO incluye stock, así que se creará con default=0
            producto = form.save()
            registrar_auditoria(
                request,
                accion='crear_producto',
                modelo='Producto',
                objeto_id=producto.id,
                descripcion=f'Creó el producto "{producto.titulo}" (Stock inicial: 0)'
            )
            messages.success(request, f'Producto {producto.titulo} creado exitosamente con stock inicial 0. Configura el stock desde el módulo de Inventario.')
            return redirect('admin_productos')
    
    # Manejar filtros GET
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    categoria_id = request.GET.get('categoria', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    
    contexto = {
        'productos': productos,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'form': ProductoForm(),
    }
    return render(request, 'admin/admin_productos.html', contexto)


@login_required
def admin_pedidos(request):
    """Gestión de pedidos"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permiso.')
        return redirect('inicio')
    
    estado_filter = request.GET.get('estado', '')
    
    if estado_filter:
        pedidos = Pedido.objects.filter(estado=estado_filter).order_by('-fecha_creacion')
    else:
        pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    
    contexto = {
        'pedidos': pedidos,
        'estado_filter': estado_filter,
    }
    return render(request, 'admin/admin_pedidos.html', contexto)


# ============ VISTAS DE NOTIFICACIONES ============

@login_required
def listar_notificaciones(request):
    """Página de todas las notificaciones del usuario"""
    notificaciones = request.user.notificaciones.all().order_by('-fecha_creacion')
    
    # Marcar como leídas
    notificaciones.filter(leida=False).update(leida=True)
    
    # Paginación
    paginator = Paginator(notificaciones, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contexto = {
        'page_obj': page_obj,
        'notificaciones': page_obj.object_list,
    }
    return render(request, 'paginas/notificaciones.html', contexto)


@login_required
def get_notificaciones_sin_leer(request):
    """API: Obtener notificaciones sin leer (para navbar)"""
    notificaciones = request.user.notificaciones.filter(leida=False).order_by('-fecha_creacion')[:5]
    
    datos = {
        'total_sin_leer': request.user.notificaciones.filter(leida=False).count(),
        'notificaciones': [
            {
                'id': n.id,
                'titulo': n.titulo,
                'mensaje': n.mensaje,
                'tipo': n.get_tipo_display(),
                'fecha': n.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
            }
            for n in notificaciones
        ]
    }
    return JsonResponse(datos)


@login_required
def marcar_notificacion_leida(request, notificacion_id):
    """Marcar una notificación como leída"""
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'estado': 'ok'})
    
    return redirect('notificaciones')


@login_required
@login_required
def actualizar_stock(request, producto_id):
    """Actualizar stock de un producto"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    try:
        producto = Producto.objects.get(id=producto_id)
        
        if request.method == 'POST':
            stock_anterior = producto.stock
            nuevo_stock = int(request.POST.get('stock', 0))
            producto.stock = nuevo_stock
            producto.save()
            
            # ✅ Registrar en auditoría
            registrar_auditoria(
                request,
                accion='actualizar_stock',
                modelo='Producto',
                objeto_id=producto.id,
                descripcion=f'Actualizó el stock de "{producto.titulo}" de {stock_anterior} a {nuevo_stock} unidades',
                cambios={'stock': {'antes': str(stock_anterior), 'despues': str(nuevo_stock)}}
            )
            
            # ✅ Notificar si el stock está bajo
            if producto.stock <= 5 and producto.stock > 0:
                notificar_stock_bajo_admin(producto, umbral=5)
            
            messages.success(request, f'Stock actualizado para {producto.titulo}')
            return redirect('gestionar_inventario')
    except Producto.DoesNotExist:
        messages.error(request, 'Producto no encontrado.')
    
    return redirect('gestionar_inventario')


@login_required
def cambiar_estado_pedido(request, pedido_id):
    """Cambiar estado de un pedido con reglas de transición"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    # Reglas de transición de estados permitidas (ADMIN)
    TRANSICIONES_PERMITIDAS = {
        'pendiente': [],                                              # Pago pendiente: solo cliente puede cancelar
        'en_preparacion': ['listo', 'rechazado'],                     # En preparación: admin lo marca listo o rechaza
        'listo': ['recogido', 'rechazado', 'cancelado'],              # Listo para recoger: puede marcarse como recogido o rechazarse/cancelarse
        'recogido': ['cancelado'],                                    # Recogido: estado final (puede cancelarse en casos especiales)
        'rechazado': [],                                              # Rechazado: estado final
        'cancelado': [],                                              # Cancelado: estado final
    }
    
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        
        # Si el pedido está en estado final, no se puede cambiar
        if pedido.estado in ['rechazado', 'cancelado', 'recogido']:
            messages.error(request, f'No se puede modificar un pedido {pedido.estado}. Este estado es final.')
            return redirect('admin_pedidos')
        
        if request.method == 'POST':
            nuevo_estado = request.POST.get('estado')
            estado_actual = pedido.estado
            
            # Validar que la transición sea permitida
            if nuevo_estado not in TRANSICIONES_PERMITIDAS.get(estado_actual, []):
                estados_validos = ', '.join(TRANSICIONES_PERMITIDAS.get(estado_actual, []))
                messages.error(request, f'No se puede cambiar de "{estado_actual}" a "{nuevo_estado}". Estados válidos: {estados_validos}')
                return redirect('admin_pedidos')
            
            pedido.estado = nuevo_estado
            pedido.save()
            
            # ✅ Registrar en auditoría
            registrar_auditoria(
                request,
                accion='cambiar_estado_pedido',
                modelo='Pedido',
                objeto_id=pedido.id,
                descripcion=f'Cambió el estado del pedido #{pedido.numero_pedido} de "{estado_actual}" a "{nuevo_estado}"',
                cambios={'estado': {'antes': estado_actual, 'despues': nuevo_estado}}
            )
            
            # ✅ Crear notificación de cambio de estado
            notificar_pedido_cambio_estado(pedido, estado_actual, nuevo_estado)
            
            messages.success(request, f'Estado del pedido actualizado a {nuevo_estado}')
            return redirect('admin_pedidos')
            
    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido no encontrado.')
    
    return redirect('admin_pedidos')


# ============ VISTA DE AUDITORÍA ============

@login_required
def admin_auditoria(request):
    """Panel de auditoría - Historial de acciones de admins"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permiso.')
        return redirect('inicio')
    
    # Filtros
    filtro_usuario = request.GET.get('usuario', '')
    filtro_accion = request.GET.get('accion', '')
    filtro_modelo = request.GET.get('modelo', '')
    
    auditorias = Auditoria.objects.all().order_by('-fecha_creacion')
    
    # Aplicar filtros
    if filtro_usuario:
        auditorias = auditorias.filter(usuario__username__icontains=filtro_usuario)
    
    if filtro_accion:
        auditorias = auditorias.filter(accion=filtro_accion)
    
    if filtro_modelo:
        auditorias = auditorias.filter(modelo=filtro_modelo)
    
    # Paginación
    paginator = Paginator(auditorias, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Opciones para filtros
    usuarios_auditorias = User.objects.filter(auditorias__isnull=False).distinct()
    acciones_disponibles = Auditoria.TIPOS_ACCION
    modelos_disponibles = Auditoria.MODELOS
    
    contexto = {
        'page_obj': page_obj,
        'auditorias': page_obj.object_list,
        'usuarios_auditorias': usuarios_auditorias,
        'acciones_disponibles': acciones_disponibles,
        'modelos_disponibles': modelos_disponibles,
        'filtro_usuario': filtro_usuario,
        'filtro_accion': filtro_accion,
        'filtro_modelo': filtro_modelo,
    }
    
    return render(request, 'admin/admin_auditoria.html', contexto)


@login_required
def admin_reportes(request):
    """
    Panel de reportes y análisis de la tienda.
    Incluye:
    - Productos más vendidos
    - Productos obsoletos
    - Rotación de inventario
    - Riesgo de quiebra
    - Desempeño por categoría
    """
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permiso.')
        return redirect('inicio')
    
    # ========== PRODUCTOS MÁS VENDIDOS ==========
    productos_vendidos = ItemPedido.objects.values('producto__id', 'producto__titulo', 'producto__precio').annotate(
        cantidad_vendida=Sum('cantidad'),
        ingresos=Sum(F('cantidad') * F('precio_unitario'), output_field=models.IntegerField())
    ).order_by('-cantidad_vendida')[:10]
    
    # ========== PRODUCTOS OBSOLETOS ==========
    # Productos sin vender en los últimos 60 días
    hace_60_dias = datetime.now() - timedelta(days=60)
    productos_vendidos_60d = ItemPedido.objects.filter(
        pedido__fecha_creacion__gte=hace_60_dias
    ).values_list('producto_id', flat=True).distinct()
    
    productos_obsoletos = Producto.objects.exclude(
        id__in=productos_vendidos_60d
    ).order_by('-stock')
    
    # ========== ROTACIÓN DE INVENTARIO ==========
    # Calcular rotación: (Ventas totales / Stock promedio) en últimos 30 días
    hace_30_dias = datetime.now() - timedelta(days=30)
    ventas_30d = ItemPedido.objects.filter(
        pedido__fecha_creacion__gte=hace_30_dias
    ).values('producto__id', 'producto__titulo').annotate(
        ventas=Sum('cantidad'),
        stock_actual=F('producto__stock')
    ).order_by('-ventas')
    
    rotacion_datos = []
    for venta in ventas_30d:
        stock_actual = venta['stock_actual']
        ventas = venta['ventas'] or 0
        rotacion = ventas / (stock_actual + ventas) if (stock_actual + ventas) > 0 else 0
        rotacion_datos.append({
            'producto_id': venta['producto__id'],
            'titulo': venta['producto__titulo'],
            'ventas_30d': ventas,
            'rotacion': round(rotacion * 100, 2)
        })
    
    rotacion_datos = sorted(rotacion_datos, key=lambda x: x['rotacion'], reverse=True)[:10]
    
    # ========== RIESGO DE QUIEBRA ==========
    ingresos_totales = Pedido.objects.filter(
        estado='aprobado'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Calcular inversión en inventario (stock total * precio promedio)
    inversion_inventario = 0
    for producto in Producto.objects.all():
        inversion_inventario += producto.stock * producto.precio
    
    # Indicadores de riesgo
    tasa_venta_promedio = ItemPedido.objects.filter(
        pedido__estado='aprobado'
    ).count() / max(Producto.objects.count(), 1)
    
    productos_con_venta = ItemPedido.objects.values_list('producto_id', flat=True).distinct()
    productos_sin_venta = Producto.objects.exclude(
        id__in=productos_con_venta
    ).count()
    
    riesgo_quiebra = {
        'ingresos_totales': ingresos_totales,
        'inversion_inventario': inversion_inventario,
        'relacion_activos': round((ingresos_totales / max(inversion_inventario, 1)) * 100, 2),
        'tasa_venta_promedio': round(tasa_venta_promedio, 2),
        'productos_sin_venta': productos_sin_venta,
        'riesgo_nivel': calcular_nivel_riesgo(ingresos_totales, inversion_inventario, tasa_venta_promedio)
    }
    
    # ========== DESEMPEÑO POR CATEGORÍA ==========
    desempeno_categoria = Categoria.objects.annotate(
        total_productos=Count('productos'),
        productos_en_stock=Count('productos', filter=Q(productos__stock__gt=0)),
        ventas_totales=Sum('productos__itempedido__cantidad'),
        ingresos_totales=Sum(
            F('productos__itempedido__cantidad') * F('productos__itempedido__precio_unitario'),
            output_field=models.IntegerField()
        ),
        stock_total=Sum('productos__stock')
    ).order_by('-ingresos_totales')
    
    # ========== ESTADÍSTICAS GENERALES ==========
    stats = {
        'ingresos_mes': Pedido.objects.filter(
            estado='aprobado',
            fecha_creacion__month=datetime.now().month,
            fecha_creacion__year=datetime.now().year
        ).aggregate(total=Sum('total'))['total'] or 0,
        
        'pedidos_mes': Pedido.objects.filter(
            estado='aprobado',
            fecha_creacion__month=datetime.now().month,
            fecha_creacion__year=datetime.now().year
        ).count(),
        
        'ticket_promedio': round(
            Pedido.objects.filter(estado='aprobado').aggregate(avg=Avg('total'))['avg'] or 0, 2
        ),
        
        'productos_stock_critico': Producto.objects.filter(stock__lte=0).count(),
        'tasa_conversion': round(
            (ItemPedido.objects.count() / max(Carrito.objects.count(), 1)) * 100, 2
        ) if Carrito.objects.exists() else 0
    }
    
    contexto = {
        'productos_vendidos': productos_vendidos,
        'productos_obsoletos': productos_obsoletos[:15],
        'rotacion_datos': rotacion_datos,
        'riesgo_quiebra': riesgo_quiebra,
        'desempeno_categoria': desempeno_categoria,
        'stats': stats,
    }
    
    return render(request, 'admin/admin_reportes.html', contexto)


def calcular_nivel_riesgo(ingresos, inversion, tasa_venta):
    """
    Calcular el nivel de riesgo de quiebra basado en indicadores financieros.
    Retorna: 'bajo', 'medio' o 'alto'
    """
    if inversion == 0:
        return 'bajo'
    
    relacion = ingresos / inversion if inversion > 0 else 0
    
    # Criterios de riesgo
    if relacion < 0.3 or tasa_venta < 0.5:
        return 'alto'
    elif relacion < 0.6 or tasa_venta < 1.0:
        return 'medio'
    else:
        return 'bajo'


# ============ GESTIÓN DE INVENTARIO ============

@login_required
def gestionar_inventario(request):
    """Panel principal de gestión de inventario"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permiso.')
        return redirect('inicio')
    
    # Productos que necesitan reorden
    productos_reorden = Producto.objects.filter(stock__lte=F('stock_minimo')).order_by('stock')
    
    # Productos con stock excedido
    productos_exceso = Producto.objects.filter(stock__gt=F('stock_maximo')).order_by('-stock')
    
    # Últimos movimientos
    movimientos_recientes = MovimientoInventario.objects.all()[:20]
    
    # Auditorias completadas recientes
    auditorias_completadas = AuditoriaInventario.objects.filter(estado='completada').order_by('-fecha_finalizacion')[:10]
    
    # Órdenes pendientes
    ordenes_pendientes = OrdenCompra.objects.filter(
        estado__in=['pendiente', 'confirmada', 'enviada']
    ).order_by('fecha_entrega_esperada')
    
    # Todos los productos con filtros
    todos_productos = Producto.objects.all().order_by('titulo')
    
    # Aplicar filtros GET
    categoria_id = request.GET.get('categoria')
    stock_min = request.GET.get('stock_min')
    stock_max = request.GET.get('stock_max')
    
    if categoria_id:
        todos_productos = todos_productos.filter(categoria_id=categoria_id)
    
    if stock_min:
        todos_productos = todos_productos.filter(stock__gte=stock_min)
    
    if stock_max:
        todos_productos = todos_productos.filter(stock__lte=stock_max)
    
    # Obtener categorías para el filtro
    categorias = Categoria.objects.all()
    
    contexto = {
        'productos_reorden': productos_reorden,
        'productos_exceso': productos_exceso,
        'movimientos_recientes': movimientos_recientes,
        'auditorias_completadas': auditorias_completadas,
        'ordenes_pendientes': ordenes_pendientes,
        'todos_productos': todos_productos,
        'categorias': categorias,
        'total_reorden': productos_reorden.count(),
        'total_exceso': productos_exceso.count(),
        'total': AuditoriaInventario.objects.filter(estado='en_proceso').count(),
    }
    
    return render(request, 'admin/gestionar_inventario.html', contexto)


@login_required
def registrar_movimiento(request, producto_id):
    """Registrar movimiento de inventario (entrada/salida)"""
    if not request.user.is_superuser:
        return redirect('inicio')
    
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        cantidad = int(request.POST.get('cantidad', 0))
        motivo = request.POST.get('motivo', '')
        
        stock_anterior = producto.stock
        
        # Calcular nuevo stock según tipo
        if tipo == 'entrada':
            producto.stock += cantidad
        elif tipo in ['salida_venta', 'salida_devolucion', 'salida_daño']:
            if producto.stock < cantidad:
                messages.error(request, 'No hay stock suficiente')
                return redirect('gestionar_inventario')
            producto.stock -= cantidad
        elif tipo == 'ajuste':
            # Reemplazar stock
            producto.stock = cantidad
        
        producto.save()
        
        # Registrar movimiento
        MovimientoInventario.objects.create(
            producto=producto,
            tipo=tipo,
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            stock_posterior=producto.stock,
            motivo=motivo,
            usuario=request.user
        )
        
        # Registrar auditoría
        registrar_auditoria(
            request,
            accion='movimiento_inventario',
            modelo='Producto',
            objeto_id=producto.id,
            descripcion=f'Movimiento: {tipo} ({cantidad} unidades) - Stock: {stock_anterior} → {producto.stock}'
        )
        
        messages.success(request, f'Movimiento registrado: {stock_anterior} → {producto.stock}')
        return redirect('gestionar_inventario')
    
    contexto = {
        'producto': producto,
        'tipos_movimiento': MovimientoInventario.TIPO_MOVIMIENTO,
    }
    return render(request, 'admin/registrar_movimiento.html', contexto)


@login_required
def crear_orden_compra(request):
    """Crear nueva orden de compra"""
    if not request.user.is_superuser:
        return redirect('inicio')
    
    if request.method == 'POST':
        from django.utils import timezone
        import uuid
        
        numero_orden = f"OC-{uuid.uuid4().hex[:8].upper()}"
        proveedor = request.POST.get('proveedor')
        fecha_entrega = request.POST.get('fecha_entrega')
        
        # Crear orden SIN total (se calculará después)
        orden = OrdenCompra.objects.create(
            numero_orden=numero_orden,
            proveedor=proveedor,
            fecha_entrega_esperada=fecha_entrega,
            total_estimado=0,  # Placeholder, se recalculará
            usuario=request.user
        )
        
        # Agregar productos
        productos_json = request.POST.get('productos_json')
        if productos_json:
            import json
            productos = json.loads(productos_json)
            for prod in productos:
                DetalleOrdenCompra.objects.create(
                    orden=orden,
                    producto_id=prod['producto_id'],
                    cantidad_solicitada=prod['cantidad'],
                    precio_unitario=int(prod['precio_unitario'])
                )
        
        # Recalcular y guardar el total estimado
        orden.total_estimado = orden.calcular_total_estimado()
        orden.save()
        
        messages.success(request, f'Orden {numero_orden} creada exitosamente')
        return redirect('gestionar_inventario')
    
    contexto = {
        'productos': Producto.objects.all(),
    }
    return render(request, 'admin/crear_orden_compra.html', contexto)


@login_required
def ver_orden_compra(request, orden_id):
    """Ver detalles de una orden de compra"""
    if not request.user.is_superuser:
        return redirect('inicio')
    
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'aceptar_parcial':
            # Procesar aceptación parcial de productos
            detalles_json = request.POST.get('detalles_json')
            if detalles_json:
                import json
                detalles_aceptados = json.loads(detalles_json)
                
                for detalle_id, cantidad in detalles_aceptados.items():
                    detalle = DetalleOrdenCompra.objects.get(id=detalle_id)
                    cantidad_int = int(cantidad)
                    detalle.cantidad_recibida = cantidad_int
                    detalle.save()
                    
                    # Actualizar stock del producto
                    producto = detalle.producto
                    producto.stock += cantidad_int
                    producto.save()
                
                # Registrar movimiento de inventario
                registrar_auditoria(
                    usuario=request.user,
                    accion='Orden de compra parcialmente recibida',
                    tabla='OrdenCompra',
                    registro_id=orden.id,
                    descripcion=f'Productos recibidos: {len(detalles_aceptados)}'
                )
                
                # Cambiar estado a recibida si todo está recibido
                todas_recibidas = all(
                    d.cantidad_recibida >= d.cantidad_solicitada 
                    for d in orden.detalles.all()
                )
                
                if todas_recibidas:
                    orden.estado = 'recibida'
                    orden.fecha_recepcion = datetime.now()
                else:
                    orden.estado = 'enviada'  # Parcialmente recibida
                
                orden.save()
                messages.success(request, '✅ Productos recibidos y stock actualizado')
                return redirect('ver_orden_compra', orden_id=orden.id)
        
        elif accion == 'rechazar_completo':
            # Rechazar la orden completa
            razon = request.POST.get('razon_rechazo', 'No especificada')
            
            orden.estado = 'cancelada'
            orden.observaciones = f"[RECHAZADA] Razón: {razon}\nObservaciones anteriores: {orden.observaciones or 'Ninguna'}"
            orden.save()
            
            registrar_auditoria(
                usuario=request.user,
                accion='Orden de compra rechazada',
                tabla='OrdenCompra',
                registro_id=orden.id,
                descripcion=f'Razón: {razon}'
            )
            
            messages.success(request, f'❌ Orden {orden.numero_orden} rechazada')
            return redirect('gestionar_inventario')
    
    detalles = orden.detalles.all()
    
    contexto = {
        'orden': orden,
        'detalles': detalles,
        'total_estimado': orden.calcular_total_estimado(),
        'total_recibido': orden.calcular_total_recibido(),
    }
    return render(request, 'admin/ver_orden_compra.html', contexto)


@login_required
def crear_auditoria_inventario(request):
    """Crear nueva auditoría de inventario"""
    if not request.user.is_superuser:
        return redirect('inicio')
    
    if request.method == 'POST':
        import uuid
        
        numero_auditoria = f"AUD-{uuid.uuid4().hex[:8].upper()}"
        tipo = request.POST.get('tipo', 'ciclico')
        categoria_id = request.POST.get('categoria_id')
        
        auditoria = AuditoriaInventario.objects.create(
            numero_auditoria=numero_auditoria,
            tipo=tipo,
            usuario_creador=request.user,
            estado='en_proceso'
        )
        
        if categoria_id:
            auditoria.categoria_id = categoria_id
            auditoria.save()
        
        # Crear detalles según tipo
        if tipo == 'total':
            productos = Producto.objects.all()
        elif tipo == 'categoria' and categoria_id:
            productos = Producto.objects.filter(categoria_id=categoria_id)
        else:
            productos = Producto.objects.all()  # Todos para cíclico
        
        for producto in productos:
            DetalleAuditoria.objects.create(
                auditoria=auditoria,
                producto=producto,
                stock_sistema=producto.stock,
                stock_fisico=producto.stock
            )
        
        messages.success(request, f'Auditoría {numero_auditoria} creada. Ingresa los datos de conteo físico.')
        return redirect('revisar_auditoria', auditoria_id=auditoria.id)
    
    # Obtener categorías con conteo de productos
    categorias = Categoria.objects.annotate(
        productos_count=models.Count('productos')
    )
    
    # Total de productos para cíclico
    total_productos = Producto.objects.count()
    
    contexto = {
        'categorias': categorias,
        'total_productos': total_productos,
    }
    return render(request, 'admin/crear_auditoria.html', contexto)


@login_required
def revisar_auditoria(request, auditoria_id):
    """Revisar y completar auditoría de inventario"""
    if not request.user.is_superuser:
        return redirect('inicio')
    
    auditoria = get_object_or_404(AuditoriaInventario, id=auditoria_id)
    detalles = auditoria.detalles.all()
    
    if request.method == 'POST':
        # Actualizar detalles
        observaciones = request.POST.get('observaciones', '')
        
        for detalle in detalles:
            stock_fisico = request.POST.get(f'stock_fisico_{detalle.id}')
            observacion = request.POST.get(f'observacion_{detalle.id}', '')
            
            if stock_fisico:
                detalle.stock_fisico = int(stock_fisico)
                detalle.observacion = observacion
                detalle.save()
        
        # Finalizar auditoría
        auditoria.estado = 'completada'
        auditoria.fecha_finalizacion = datetime.now()
        auditoria.usuario_revisor = request.user
        auditoria.observaciones = observaciones
        auditoria.save()
        
        # Aplicar ajustes
        for detalle in detalles:
            if detalle.diferencia != 0:
                producto = detalle.producto
                stock_anterior = producto.stock
                producto.stock = detalle.stock_fisico
                producto.save()
                
                MovimientoInventario.objects.create(
                    producto=producto,
                    tipo='ajuste',
                    cantidad=abs(detalle.diferencia),
                    stock_anterior=stock_anterior,
                    stock_posterior=producto.stock,
                    motivo=f'Auditoría {auditoria.numero_auditoria} - {detalle.observacion}',
                    usuario=request.user
                )
                
                detalle.ajustado = True
                detalle.save()
        
        messages.success(request, f'Auditoría {auditoria.numero_auditoria} completada')
        return redirect('gestionar_inventario')
    
    # Calcular discrepancias
    discrepancias_count = sum(1 for d in detalles if d.diferencia != 0)
    
    contexto = {
        'auditoria': auditoria,
        'detalles': detalles,
        'discrepancias_count': discrepancias_count,
    }
    return render(request, 'admin/revisar_auditoria.html', contexto)


@login_required
def cancelar_auditoria(request, auditoria_id):
    """Cancelar una auditoria en proceso"""
    if not request.user.is_superuser:
        return redirect('inicio')
    
    auditoria = get_object_or_404(AuditoriaInventario, id=auditoria_id)
    
    if auditoria.estado == 'en_proceso':
        auditoria.estado = 'cancelada'
        auditoria.save()
        messages.success(request, f'✓ Auditoría {auditoria.numero_auditoria} cancelada')
    else:
        messages.warning(request, f'⚠️ No se puede cancelar una auditoría en estado "{auditoria.get_estado_display()}"')
    
    return redirect('gestionar_inventario')


@login_required
def auditorias_abiertas(request):
    """Panel para ver y gestionar auditorias en proceso"""
    if not request.user.is_superuser:
        return redirect('inicio')
    
    auditorias_abiertas = AuditoriaInventario.objects.filter(estado='en_proceso').order_by('-fecha_creacion')
    
    contexto = {
        'auditorias': auditorias_abiertas,
        'total': auditorias_abiertas.count(),
    }
    
    return render(request, 'admin/auditorias_abiertas.html', contexto)


@login_required
def editar_pedido(request, pedido_id):
    """
    Permite al admin editar un pedido solo cuando está en preparación.
    Puede eliminar items sin stock y procesar reembolso.
    """
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('inicio')
    
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Solo permitir editar pedidos en preparación (estado después de pago confirmado)
    if pedido.estado != 'en_preparacion':
        messages.error(request, 'Solo puedes editar pedidos que están en preparación.')
        return redirect('admin_pedidos')
    
    items = pedido.items.all()
    
    if request.method == 'POST':
        # Obtener items a eliminar
        items_a_eliminar = request.POST.getlist('items_eliminar')
        razon = request.POST.get('razon', '')
        
        if not items_a_eliminar:
            messages.warning(request, 'Debes seleccionar al menos un item para eliminar.')
            return redirect('editar_pedido', pedido_id=pedido_id)
        
        # Calcular reembolso
        reembolso_total = 0
        items_eliminados = []
        
        for item_id in items_a_eliminar:
            try:
                item = ItemPedido.objects.get(id=item_id, pedido=pedido)
                subtotal_item = item.cantidad * item.precio_unitario
                reembolso_total += subtotal_item
                items_eliminados.append(f"{item.producto.titulo} (x{item.cantidad})")
                item.delete()
            except ItemPedido.DoesNotExist:
                continue
        
        if reembolso_total > 0:
            # Procesar reembolso en Mercado Pago
            try:
                sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
                refund_body = {"amount": reembolso_total}
                refund_response = sdk.refund().create(pedido.payment_id, refund_body)
                
                if refund_response['status'] == 200 or refund_response['status'] == 201:
                    # Guardar información del reembolso
                    pedido.reembolso_parcial = reembolso_total
                    pedido.razon_reembolso = razon
                    pedido.total -= reembolso_total
                    pedido.save()
                    
                    # Notificar al cliente
                    crear_notificacion(
                        usuario=pedido.usuario,
                        titulo=f"Pedido #{pedido.numero_pedido} - Reembolso Parcial Realizado",
                        mensaje=f"Se ha procesado un reembolso de ${reembolso_total} por los siguientes items: {', '.join(items_eliminados)}. Razón: {razon}",
                        tipo='pedido_reembolso',
                        pedido=pedido
                    )
                    
                    # Registrar en auditoría
                    registrar_auditoria(
                        usuario=request.user,
                        accion='reembolso_pedido',
                        descripcion=f'Reembolso de ${reembolso_total} en pedido {pedido.numero_pedido}. Items: {", ".join(items_eliminados)}. Razón: {razon}',
                        tabla='Pedido',
                        id_registro=pedido.id
                    )
                    
                    messages.success(request, f'✅ Reembolso de ${reembolso_total} procesado correctamente.')
                else:
                    messages.error(request, f'Error al procesar reembolso: {refund_response.get("message", "Error desconocido")}')
            except Exception as e:
                messages.error(request, f'Error al procesar reembolso: {str(e)}')
        
        return redirect('admin_pedidos')
    
    context = {
        'pedido': pedido,
        'items': items,
    }
    return render(request, 'admin/editar_pedido.html', context)


