# Documentación Completa - Tienda Anime

## 1. Estructura del Proyecto

```
proyectoCA/
├── manage.py                          # Gestor de Django
├── requirements.txt                   # Dependencias del proyecto
├── tiendaanime.sql                    # Base de datos SQL
├── proyectoCA/                        # Configuración principal de Django
│   ├── settings.py                    # Configuración del proyecto
│   ├── urls.py                        # Rutas principales
│   ├── asgi.py                        # Configuración ASGI
│   └── wsgi.py                        # Configuración WSGI
├── sysApp/                            # Aplicación principal
│   ├── models.py                      # Modelos de BD
│   ├── views.py                       # Lógica de vistas
│   ├── urls.py                        # Rutas de la app
│   ├── forms.py                       # Formularios
│   ├── admin.py                       # Interfaz de administrador
│   ├── static/                        # Archivos estáticos
│   │   ├── css/                       # Estilos CSS
│   │   └── fondos/                    # Imágenes de fondo
│   ├── templates/                     # Plantillas HTML
│   │   ├── master.html                # Plantilla base
│   │   ├── includes/                  # Componentes reutilizables
│   │   │   ├── navbar.html
│   │   │   └── footer.html
│   │   ├── paginas/                   # Páginas principales
│   │   ├── registration/              # Páginas de autenticación
│   │   └── emails/                    # Plantillas de email
│   ├── migrations/                    # Migraciones de BD
│   └── management/commands/           # Comandos personalizados
├── media/                             # Archivos de usuario (productos)
└── env/                               # Entorno virtual Python
```

---

## 2. Base de Datos - Modelos

### Modelo: User (Django Built-in)
- **id**: Identificador único
- **username**: Nombre de usuario
- **email**: Email único
- **password**: Contraseña hasheada
- **first_name**: Nombre
- **last_name**: Apellido
- **is_active**: Usuario activo
- **date_joined**: Fecha de registro

### Modelo: Categoria
```python
id (PK)
nombre (CharField, max_length=100, unique=True)
descripcion (TextField, blank=True)
icono (CharField, default='fas fa-box')
```
**Uso**: Organizar productos en categorías (Anime, Manga, Figuras, etc.)

### Modelo: Producto
```python
id (PK)
titulo (CharField, max_length=200)
descripcion (TextField)
precio (DecimalField, max_digits=10, decimal_places=2)
stock (IntegerField, default=0)
foto (ImageField, upload_to='productos/')
categoria (ForeignKey -> Categoria)
fecha_creacion (DateTimeField, auto_now_add=True)
fecha_actualizacion (DateTimeField, auto_now=True)
destacado (BooleanField, default=False)
```
**Uso**: Almacenar información de productos vendibles

### Modelo: Carrito
```python
id (PK)
usuario (ForeignKey -> User)
producto (ForeignKey -> Producto)
cantidad (IntegerField, default=1)
fecha_agregado (DateTimeField, auto_now_add=True)

class Meta:
    unique_together = ('usuario', 'producto')
```
**Uso**: Almacenar productos seleccionados por el usuario antes de comprar

### Modelo: Pedido
```python
id (PK)
numero_pedido (CharField, unique=True, auto-generado como "PED-YYYYMMDD-XXXXX")
usuario (ForeignKey -> User)
fecha_pedido (DateTimeField, auto_now_add=True)
estado (CharField, choices=[
    'pendiente',    # Esperando pago
    'procesando',   # Pago recibido, preparando envío
    'aprobado',     # Pago completado
    'rechazado',    # Pago fallido
    'cancelado'     # Cancelado por usuario
])
total (DecimalField)
preferencia_id (CharField, null=True)  # ID de preferencia de Mercado Pago
payment_id (CharField, null=True)      # ID de pago de Mercado Pago
fecha_pago (DateTimeField, null=True)   # Cuándo se pagó
metodo_pago (CharField, default='mercado_pago')
```
**Uso**: Registrar todas las compras de los usuarios

### Modelo: ItemPedido
```python
id (PK)
pedido (ForeignKey -> Pedido)
producto (ForeignKey -> Producto)
cantidad (IntegerField)
precio_unitario (DecimalField)  # Precio al momento de comprar

class Meta:
    unique_together = ('pedido', 'producto')
```
**Uso**: Detalles de cada producto en un pedido (relación muchos-a-muchos con historial de precios)

---

## 3. Flujo de Autenticación

### Registro (registration/registro.html)
1. Usuario accede a `/accounts/register/`
2. Completa formulario con: email, nombre, contraseña
3. Django crea usuario y contraseña hasheada
4. Redirige a login

### Login (registration/login.html)
1. Usuario accede a `/accounts/login/`
2. Proporciona email y contraseña
3. Django verifica credenciales
4. Crea sesión de usuario
5. Redirige a página anterior o inicio

### Recuperación de Contraseña (PERSONALIZADA)
1. Usuario accede a `/recuperar-password/`
2. Ingresa su email
3. Sistema genera contraseña temporal (6 caracteres aleatorios)
4. Envía email con contraseña temporal
5. Usuario usa contraseña temporal para login
6. Es redirigido a `/cambiar-password-temporal/` automáticamente
7. Debe establecer nueva contraseña
8. Login con nueva contraseña

**Vistas personalizadas** (en views.py):
- `recuperar_password`: Genera y envía contraseña temporal
- `cambiar_password_temporal`: Permite cambiar contraseña en primer login
- `verificar_email_existente`: Valida emails durante registro

---

## 4. Catálogo y Búsqueda

### Vista: index (/)
- Muestra página principal
- Destaca productos marcados como `destacado=True`
- Contiene formulario de búsqueda y filtros

### Vista: catalogo (/catalogo/)
- Muestra todos los productos
- Filtrados por categoría si se proporciona
- Búsqueda por título con `Q(titulo__icontains=query)`
- Ordenamiento por:
  - precio_asc: Precio menor a mayor
  - precio_desc: Precio mayor a menor
  - reciente: Productos más nuevos primero
  - popular: Los más vendidos primero
- Paginación: 12 productos por página

### Vista: detalle_producto (paginas/detalleProducto.html)
- Muestra información completa de un producto
- Cantidad disponible (stock)
- Galería de imágenes
- Botón "Agregar al carrito"

**Parámetros URL**: `/producto/<id>/`

---

## 5. Carrito de Compras

### Vista: agregar_al_carrito (GET /agregar_al_carrito/<id>/)
```python
1. Obtiene producto por ID
2. Si usuario autenticado:
   - Busca si el producto ya está en su carrito
   - Si existe: incrementa cantidad
   - Si no existe: crea nuevo ItemCarrito
3. Si usuario NO autenticado:
   - Guarda en sesión (carrito_temporal)
4. Redirige a carrito con mensaje de confirmación
```

### Vista: carrito (GET /carrito/)
```python
1. Si usuario autenticado:
   - Obtiene todos sus ItemsCarrito
   - Calcula total
2. Si usuario NO autenticado:
   - Lee carrito_temporal de sesión
   - Obtiene productos desde BD
3. Renderiza template con items
```

### Vista: eliminar_del_carrito (GET /eliminar_del_carrito/<id>/)
```python
1. Obtiene ItemCarrito
2. Lo elimina de BD
3. Redirige a carrito
```

### Vista: actualizar_carrito (POST)
```python
1. Recibe JSON con cantidades
2. Valida que cantidad >= 1 y <= stock
3. Actualiza cada ItemCarrito
4. Devuelve JSON con nuevo total
```

---

## 6. Integración Mercado Pago

### Configuración (settings.py)
```python
# Credenciales de prueba (sandbox)
MERCADOPAGO_ACCESS_TOKEN = 'APP_USR_...'
MERCADOPAGO_PUBLIC_KEY = 'APP_...'

# Configuración para ngrok (desarrollo)
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'postexilian-allene-unfragrantly.ngrok-free.dev'  # Cambiar si ngrok reinicia
]

CSRF_TRUSTED_ORIGINS = [
    'https://postexilian-allene-unfragrantly.ngrok-free.dev',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

### Vista: checkout_mercadopago (GET /checkout/mercadopago/)

**Función**: Crear preferencia de pago en Mercado Pago

```python
def checkout_mercadopago(request):
    usuario = request.user
    carrito_items = Carrito.objects.filter(usuario=usuario)
    
    if not carrito_items.exists():
        return redirect('carrito')
    
    # 1. Crear Pedido en BD
    numero_pedido = generar_numero_pedido()
    total = sum(item.producto.precio * item.cantidad for item in carrito_items)
    
    pedido = Pedido.objects.create(
        numero_pedido=numero_pedido,
        usuario=usuario,
        total=total,
        estado='pendiente'
    )
    
    # 2. Crear ItemPedidos
    for item in carrito_items:
        ItemPedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
    
    # 3. IMPORTANTE: Detectar si estamos en ngrok o localhost
    if 'ngrok' in request.get_host():
        base_url = f"https://{request.get_host()}"
    else:
        base_url = "http://localhost:8000"
    
    # 4. Crear preferencia de Mercado Pago
    preference = {
        "items": [
            {
                "title": item.producto.titulo,
                "quantity": item.cantidad,
                "unit_price": float(item.producto.precio),
            }
            for item in carrito_items
        ],
        "payer": {
            "email": usuario.email
        },
        "back_urls": {
            "success": f"{base_url}/mis-pedidos/?payment_id={{payment_id}}&external_reference={{external_reference}}&collection_status={{collection_status}}",
            "failure": f"{base_url}/pago/fallo/",
            "pending": f"{base_url}/pago/pendiente/"
        },
        "external_reference": numero_pedido,
        "notification_url": None,  # No usar webhook para localhost
    }
    
    # 5. Enviar a Mercado Pago
    mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    result = mp.preference().create(preference)
    
    if result["status"] == 201:
        pedido.preferencia_id = result["response"]["id"]
        pedido.save()
        
        # 6. Limpiar carrito
        carrito_items.delete()
        
        # 7. Redirigir a checkout de MP
        return redirect(result["response"]["init_point"])
    else:
        return render(request, 'error.html', {'mensaje': 'Error al crear preferencia'})
```

**Puntos clave**:
- ✅ Detecta ngrok con `if 'ngrok' in request.get_host()`
- ✅ Usa ngrok URL para success_url (MP rechaza localhost)
- ✅ external_reference = número_pedido (vincula pago con pedido)
- ✅ Limpia carrito después de crear pedido
- ✅ No usa notification_url (webhook) para evitar errores

---

## 7. Flujo Post-Pago y Verificación

### Vista: mis_pedidos (GET /mis-pedidos/)

**Función**: Mostrar pedidos del usuario Y procesar retorno de Mercado Pago

```python
def mis_pedidos(request):
    usuario = request.user
    
    # PASO 1: Procesar parámetros retornados por Mercado Pago
    payment_id = request.GET.get('payment_id')
    external_reference = request.GET.get('external_reference')
    collection_status = request.GET.get('collection_status')
    
    if payment_id and external_reference and collection_status == 'approved':
        # Buscar el pedido correspondiente
        pedido = Pedido.objects.filter(
            numero_pedido=external_reference,
            usuario=usuario
        ).first()
        
        if pedido and pedido.estado == 'pendiente':
            # Actualizar estado a aprobado inmediatamente
            pedido.estado = 'aprobado'
            pedido.payment_id = payment_id
            pedido.fecha_pago = datetime.now()
            pedido.save()
            print(f"✅ Pedido {numero_pedido} actualizado a APROBADO")
    
    # PASO 2: Obtener todos los pedidos del usuario
    pedidos = Pedido.objects.filter(usuario=usuario).order_by('-fecha_pedido')
    
    context = {
        'pedidos': pedidos
    }
    
    return render(request, 'paginas/mis_pedidos.html', context)
```

**¿Por qué funciona ahora?**

Cuando MP redirige desde su sitio de checkout, lo hace así:
```
https://postexilian-allene-unfragrantly.ngrok-free.dev/mis-pedidos/
?payment_id=XXXXXXXXXXXX
&external_reference=PED-YYYYMMDD-XXXXX
&collection_status=approved
```

La vista captura estos parámetros y ANTES de mostrar la página:
1. ✅ Busca el Pedido por número (`external_reference`)
2. ✅ Si está pendiente, lo marca como 'aprobado'
3. ✅ Guarda el payment_id y fecha_pago

Resultado: El usuario ve inmediatamente su pedido como "PAGADO"

### Vista: verificar_pago (GET /verificar-pago/ - JSON)

**Función**: Verificación alternativa mediante polling (respaldo)

```python
def verificar_pago(request):
    preference_id = request.GET.get('preference_id')
    
    if not preference_id:
        return JsonResponse({'error': 'Sin preference_id'}, status=400)
    
    mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    # Buscar pagos asociados a esta preferencia
    search_result = mp.payment().search({
        "external_reference": preference_id
    })
    
    if search_result and search_result["response"]["results"]:
        payment = search_result["response"]["results"][0]
        
        if payment["status"] == "approved":
            # Pago confirmado
            pedido = Pedido.objects.filter(
                numero_pedido=preference_id
            ).first()
            
            if pedido:
                pedido.estado = 'aprobado'
                pedido.payment_id = payment["id"]
                pedido.save()
                
                return JsonResponse({
                    'estado': 'aprobado',
                    'mensaje': 'Pago confirmado'
                })
    
    return JsonResponse({'estado': 'pendiente'})
```

### Vista: mercadopago_webhook (POST /mp-webhook/)

**Función**: Recibir notificaciones de Mercado Pago en tiempo real

```python
@csrf_exempt
@require_http_methods(["POST"])
def mercadopago_webhook(request):
    """
    MP envía:
    {
        "id": "NOTIFICATION_ID",
        "type": "payment",
        "data": {
            "id": "PAYMENT_ID"
        }
    }
    """
    try:
        data = json.loads(request.body)
        
        if data.get("type") == "payment":
            payment_id = data.get("data", {}).get("id")
            
            # Consultar estado del pago a MP
            mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            payment_info = mp.payment().get(payment_id)
            
            if payment_info["status"] == 200:
                payment = payment_info["response"]
                
                if payment["status"] == "approved":
                    external_reference = payment.get("external_reference")
                    
                    pedido = Pedido.objects.filter(
                        numero_pedido=external_reference
                    ).first()
                    
                    if pedido:
                        pedido.estado = 'aprobado'
                        pedido.payment_id = payment_id
                        pedido.save()
                        print(f"✅ Webhook: Pedido {external_reference} aprobado")
        
        return JsonResponse({"status": "ok"}, status=200)
    
    except Exception as e:
        # Retornar 200 siempre para que MP no reintente
        print(f"❌ Error en webhook: {e}")
        return JsonResponse({"status": "ok"}, status=200)
```

**Importante**: Retorna HTTP 200 incluso en errores, porque si retorna error, MP reintentará indefinidamente.

---

## 8. Gestión de Pedidos

### Vista: cancelar_pedido (POST /cancelar-pedido/<id>/)

**Función**: Cancelar un pedido pendiente

```python
def cancelar_pedido(request, pedido_id):
    if request.method != 'POST':
        return redirect('mis_pedidos')
    
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    if pedido.estado == 'pendiente':
        pedido.estado = 'cancelado'
        pedido.save()
        messages.success(request, f'Pedido {pedido.numero_pedido} cancelado')
    else:
        messages.error(request, 'Solo se pueden cancelar pedidos pendientes')
    
    return redirect('mis_pedidos')
```

**Importante**: Cambia estado a 'cancelado', NO lo elimina. Mantiene historial de compras.

### Vista: reintentar_pago (GET /reintentar-pago/<pedido_id>/)

**Función**: Crear nueva preferencia para pago de pedido pendiente

```python
def reintentar_pago(request, pedido_id):
    usuario = request.user
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=usuario)
    
    if pedido.estado != 'pendiente':
        messages.error(request, 'Solo se pueden reintentar pedidos pendientes')
        return redirect('mis_pedidos')
    
    # Obtener items del pedido
    items = ItemPedido.objects.filter(pedido=pedido)
    
    # Construir preferencia
    if 'ngrok' in request.get_host():
        base_url = f"https://{request.get_host()}"
    else:
        base_url = "http://localhost:8000"
    
    preference = {
        "items": [
            {
                "title": item.producto.titulo,
                "quantity": item.cantidad,
                "unit_price": float(item.precio_unitario),
            }
            for item in items
        ],
        "payer": {
            "email": usuario.email
        },
        "back_urls": {
            "success": f"{base_url}/mis-pedidos/?payment_id={{payment_id}}&external_reference={{external_reference}}&collection_status={{collection_status}}",
            "failure": f"{base_url}/pago/fallo/",
            "pending": f"{base_url}/pago/pendiente/"
        },
        "external_reference": pedido.numero_pedido,
    }
    
    mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    result = mp.preference().create(preference)
    
    if result["status"] == 201:
        pedido.preferencia_id = result["response"]["id"]
        pedido.save()
        return redirect(result["response"]["init_point"])
    else:
        messages.error(request, 'Error al crear preferencia de pago')
        return redirect('mis_pedidos')
```

---

## 9. Funcionalidad de Administrador

### Vista: productos_admin (GET /productos-admin/)
- Muestra tabla de todos los productos
- Permite editar cada producto
- Permite eliminar productos

### Vista: agregar_producto_admin (GET/POST /agregar-producto/)
- Formulario para agregar nuevo producto
- Sube imagen a `media/productos/`
- Valida que no exista ya

### Vista: eliminar_producto_admin (POST)
- Elimina producto y su imagen
- Redirige a lista de productos

### Vista: modificar_producto_admin (GET/POST /modificar-producto/<id>/)
- Formulario para editar producto existente
- Puede cambiar imagen, precio, stock, etc.

---

## 10. Generación de PDF

### Vista: descargar_comprobante (GET /descargar-comprobante/<pedido_id>/)

```python
def descargar_comprobante(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    # Crear PDF con ReportLab
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Contenido
    content = []
    
    # Título
    styles = getSampleStyleSheet()
    title = Paragraph(f"Comprobante de Pedido", styles['Heading1'])
    content.append(title)
    
    # Datos del pedido
    data = [
        ['Número de Pedido:', pedido.numero_pedido],
        ['Fecha:', pedido.fecha_pedido.strftime('%d/%m/%Y')],
        ['Estado:', pedido.estado.upper()],
        ['Total:', f"${pedido.total}"]
    ]
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 3), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 3), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    content.append(table)
    
    # Construir PDF
    doc.build(content)
    buffer.seek(0)
    
    # Retornar como descarga
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pedido_{pedido.numero_pedido}.pdf"'
    
    return response
```

---

## 11. Temas y Estilo CSS

### Tema Claro (#f8f9fa)
```css
:root {
    --color-primario: #667eea;
    --color-secundario: #764ba2;
    --color-fondo: #f8f9fa;
    --color-texto: #2d3748;
    --color-borde: #e2e8f0;
    --color-exito: #48bb78;
    --color-error: #f56565;
    --color-alerta: #ed8936;
}

body {
    background-color: var(--color-fondo);
    color: var(--color-texto);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
```

### Archivos CSS Organizados
- `index.css` - Página principal
- `catalogo.css` - Página de catálogo
- `detalleProducto.css` - Detalles del producto
- `detalle_carrito.css` - Carrito de compras
- `mis_pedidos.css` - Historial de pedidos
- `pago_exito.css` - Confirmación de pago
- `pago_fallo.css` - Pago fallido
- `pago_pendiente.css` - Pago pendiente
- `navbar.css` - Barra de navegación
- `footer.css` - Pie de página
- `editar_perfil.css` - Perfil de usuario
- `login.css` - Página de login
- `registro.css` - Página de registro

---

## 12. Dependencias del Proyecto

```
Django==5.1.4              # Framework web
mysqlclient==2.2.6         # Conector MySQL
pillow==11.0.0             # Procesamiento de imágenes
reportlab==4.2.5           # Generación de PDFs
PyPDF2==3.0.1              # Manipulación de PDFs
mercado-pago==2.2.10       # SDK de Mercado Pago
sqlparse==0.5.3            # Parsing de SQL
asgiref==3.8.1             # ASGI utilities
chardet==5.2.0             # Detección de codificación
```

---

## 13. Flujo Completo de Compra

```
1. INICIO: Usuario accede a /
   ↓
2. EXPLORACIÓN: Navega por catálogo (/catalogo/)
   ↓
3. SELECCIÓN: Hace click en producto (/producto/<id>/)
   ↓
4. AGREGAR AL CARRITO: POST /agregar_al_carrito/<id>/
   - Agrega a BD si autenticado
   - Agrega a sesión si NO autenticado
   ↓
5. REVISAR CARRITO: GET /carrito/
   - Ve productos, cantidades, total
   - Puede cambiar cantidades (AJAX)
   - Puede eliminar items
   ↓
6. CHECKOUT: GET /checkout/mercadopago/
   - Crea Pedido(estado='pendiente')
   - Crea ItemPedidos
   - Crea preferencia en MP
   - Redirige a checkout de MP
   ↓
7. PAGO: Usuario completa pago en Mercado Pago
   - Ingresa datos de tarjeta
   - MP procesa pago
   ↓
8. RETORNO: MP redirige a /mis-pedidos/?payment_id=X&...
   - mis_pedidos captura parámetros
   - Actualiza Pedido.estado='aprobado'
   - Muestra página con pedido ya "PAGADO"
   ↓
9. CONFIRMACIÓN: Usuario ve su pedido en "Mis Pedidos"
   - Estado: PAGADO
   - Puede descargar comprobante PDF
   - Puede cancelar (si aún pendiente)
   - Puede reintentar pago (si falló)
   ↓
10. OPCIONES:
    - Continuar comprando → vuelve a paso 2
    - Cancelar pedido → estado='cancelado'
    - Reintentar pago → crea nueva preferencia (paso 6)
```

---

## 14. Solución de Problemas

### ❌ Error: "Invalid HTTP_HOST header"
**Problema**: `postexilian-allene-unfragrantly.ngrok-free.dev not in ALLOWED_HOSTS`

**Solución**:
```python
# settings.py
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'postexilian-allene-unfragrantly.ngrok-free.dev'  # Agregar ngrok URL
]
```

---

### ❌ Error: "Origin checking failed"
**Problema**: CSRF validation error con ngrok

**Solución**:
```python
# settings.py
CSRF_TRUSTED_ORIGINS = [
    'https://postexilian-allene-unfragrantly.ngrok-free.dev',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

---

### ❌ Error: "notificaction_url attribute must be a valid url"
**Problema**: Intentar usar localhost:8000 como webhook

**Solución**: No usar `notification_url` para localhost. MP rechaza URLs locales:
```python
preference = {
    # ... otros campos ...
    "notification_url": None,  # ❌ No usar para localhost
}
```

---

### ❌ Pedido no aparece como "PAGADO"
**Problema**: Pedido permanece en estado 'pendiente' después de pagar

**Solución**: La vista `mis_pedidos` debe capturar parámetros de MP:
```python
def mis_pedidos(request):
    payment_id = request.GET.get('payment_id')
    external_reference = request.GET.get('external_reference')
    collection_status = request.GET.get('collection_status')
    
    if payment_id and collection_status == 'approved':
        pedido = Pedido.objects.filter(numero_pedido=external_reference).first()
        if pedido:
            pedido.estado = 'aprobado'
            pedido.payment_id = payment_id
            pedido.save()
```

---

### ❌ back_urls vacías desde Mercado Pago
**Problema**: MP retorna preferencia con back_urls vacías

**Solución**: Detectar ngrok y construir URLs correctas:
```python
if 'ngrok' in request.get_host():
    base_url = f"https://{request.get_host()}"
else:
    base_url = "http://localhost:8000"

# Usar base_url para construir URLs
success_url = f"{base_url}/mis-pedidos/?payment_id={{payment_id}}&..."
```

---

### ⚠️ ngrok cambia URL después de reiniciar
**Problema**: La URL de ngrok cambia cada vez que reinicia

**Solución**: 
1. Ejecutar ngrok nuevamente: `.\ngrok http 8000`
2. Copiar nueva URL
3. Actualizar en:
   - `settings.py` → ALLOWED_HOSTS
   - `settings.py` → CSRF_TRUSTED_ORIGINS
   - Mercado Pago Dashboard → URLs autorizadas

---

## 15. Información de Prueba

### Tarjeta de Prueba
```
Número: 4111 1111 1111 1111
CVV: Cualquiera (ej: 123)
Fecha: Cualquier fecha futura
```

### Acceso al Admin
```
URL: http://localhost:8000/admin/
Username: admin
Password: (ver Usuarios(LEER IMPORTANTE).txt)
```

### Base de Datos
```
Host: localhost
Usuario: (en tiendaanime.sql)
Base de datos: tiendaanime
```

---

## 16. Instalación y Configuración Inicial

### 1. Entorno Virtual
```bash
# Crear entorno virtual
python -m venv env

# Activar
# Windows:
.\env\Scripts\activate
# Linux/Mac:
source env/bin/activate
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Base de Datos
```bash
# Importar tiendaanime.sql
mysql -u usuario -p < tiendaanime.sql

# Ejecutar migraciones
python manage.py migrate
```

### 4. Usuario Admin
```bash
python manage.py createsuperuser
```

### 5. Mercado Pago
1. Ir a https://www.mercadopago.com.ar
2. Crear cuenta de desarrollador
3. Obtener credenciales de sandbox
4. Actualizar en `settings.py`:
   ```python
   MERCADOPAGO_ACCESS_TOKEN = 'APP_USR_...'
   ```

### 6. ngrok (Para desarrollo)
```bash
# Descargar de https://ngrok.com/download
# Ejecutar:
.\ngrok http 8000

# Copiar URL como: https://postexilian-allene-unfragrantly.ngrok-free.dev
# Actualizar en settings.py
```

### 7. Ejecutar Servidor
```bash
python manage.py runserver
# Acceder a: http://localhost:8000
# O con ngrok: https://postexilian-allene-unfragrantly.ngrok-free.dev
```

---

## 17. Deployment a Producción

### Cambios Necesarios

```python
# settings.py

# 1. DEBUG = False
DEBUG = False

# 2. ALLOWED_HOSTS con dominio real
ALLOWED_HOSTS = ['tunominio.com', 'www.tunominio.com']

# 3. CSRF_TRUSTED_ORIGINS con dominio real
CSRF_TRUSTED_ORIGINS = [
    'https://tunominio.com',
    'https://www.tunominio.com',
]

# 4. Credenciales de producción de Mercado Pago
MERCADOPAGO_ACCESS_TOKEN = 'APP_USR_...'  # Producción

# 5. Eliminar detección de ngrok (solo desarrollo)
# Cambiar checkout_mercadopago y reintentar_pago para usar directamente:
base_url = 'https://tunominio.com'  # Sin detección
```

### Remover Detección de ngrok

**Antes (Desarrollo)**:
```python
if 'ngrok' in request.get_host():
    base_url = f"https://{request.get_host()}"
else:
    base_url = "http://localhost:8000"
```

**Después (Producción)**:
```python
base_url = 'https://tunominio.com'
```

### Base de Datos Producción
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tiendaanime',
        'USER': 'usuario',
        'PASSWORD': 'contraseña_segura',
        'HOST': 'servidor.com',
        'PORT': '3306',
    }
}
```

### Webhook URL en Mercado Pago
```
https://tunominio.com/mp-webhook/
```

---

## Conclusión

Esta aplicación es un e-commerce funcional de anime con integración completa a Mercado Pago. El flujo de pago es confiable y permite:

✅ Crear preferencias de pago con URLs correctas  
✅ Retornar del pago y actualizar estado inmediatamente  
✅ Cancelar pedidos pendientes  
✅ Reintentar pago de pedidos fallidos  
✅ Generar comprobantes en PDF  
✅ Administrar productos con panel admin  
✅ Mantener historial completo de compras  

Para cualquier duda, revisar los comentarios en `views.py` o esta documentación.
