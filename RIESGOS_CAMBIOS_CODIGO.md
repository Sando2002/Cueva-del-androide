# Riesgos de Cambios en el Código - Ejemplos Detallados

## 1. CAMBIOS SEGUROS ✅

### 1.1 Renombrar Variables Locales
**Archivo:** `sysApp/views.py` línea 284

**CÓDIGO ORIGINAL:**
```python
def catalogo(request):
    productos = Producto.objects.filter(activo=True)
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'paginas/catalogo.html', {'page_obj': page_obj})
```

**CAMBIO SEGURO:**
```python
def catalogo(request):
    items = Producto.objects.filter(activo=True)  # ← CAMBIO: productos → items
    paginator = Paginator(items, 12)  # ← CAMBIO: productos → items
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'paginas/catalogo.html', {'page_obj': page_obj})
```

**¿QUÉ PASA?** ✅ Funciona perfecto. Es solo un nombre interno que no afecta nada.
- El HTML sigue recibiendo `page_obj` (no cambió)
- La base de datos no se ve afectada
- La lógica es idéntica
- **RIESGO:** Bajo (0%)

---

### 1.2 Cambiar Comentarios
**Archivo:** `sysApp/views.py` línea 381

**CÓDIGO ORIGINAL:**
```python
def agregar_al_carrito(request):
    # Obtener producto
    producto_id = request.POST.get('producto_id')
    cantidad = request.POST.get('cantidad', 1)
```

**CAMBIO SEGURO:**
```python
def agregar_al_carrito(request):
    # Obtenemos el ID y cantidad del formulario POST
    producto_id = request.POST.get('producto_id')
    cantidad = request.POST.get('cantidad', 1)
```

**¿QUÉ PASA?** ✅ Los comentarios solo son para humanos. El código funciona igual.
- **RIESGO:** Ninguno (0%)

---

### 1.3 Cambiar Estilos CSS
**Archivo:** `sysApp/static/css/catalogo.css`

**CÓDIGO ORIGINAL:**
```css
.producto-card {
    background-color: white;
    border-radius: 8px;
    padding: 15px;
}
```

**CAMBIO SEGURO:**
```css
.producto-card {
    background-color: #f8f9fa;  /* ← CAMBIO: color de fondo */
    border-radius: 12px;         /* ← CAMBIO: bordes más redondeados */
    padding: 20px;               /* ← CAMBIO: más espacio interno */
}
```

**¿QUÉ PASA?** ✅ Solo cambia la apariencia visual.
- Las tarjetas se ven diferentes pero funcionan igual
- No hay riesgo de ruptura de lógica
- **RIESGO:** Ninguno (0%)

---

### 1.4 Cambiar Mensajes de Alerta
**Archivo:** `sysApp/static/js/validation.js`

**CÓDIGO ORIGINAL:**
```javascript
if (cantidad < 1) {
    alert("Cantidad mínima es 1");
    return false;
}
```

**CAMBIO SEGURO:**
```javascript
if (cantidad < 1) {
    alert("Debes comprar mínimo 1 producto");  // ← CAMBIO: mensaje diferente
    return false;
}
```

**¿QUÉ PASA?** ✅ Solo cambia lo que ve el usuario.
- El validador sigue funcionando
- Se rechazarán cantidades menores a 1
- **RIESGO:** Ninguno (0%)

---

## 2. CAMBIOS PELIGROSOS ⚠️

### 2.1 Renombrar una Función SIN Actualizar Llamadas
**Archivo:** `sysApp/views.py` línea 136

**CÓDIGO ORIGINAL:**
```python
def registrar_auditoria(usuario, accion, modelo, cambios, ip):
    """Registra cambio en la tabla de auditoría"""
    auditoria = Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        modelo=modelo,
        cambios=cambios,
        ip_cliente=ip
    )
    return auditoria
```

**CAMBIO PELIGROSO:**
```python
def log_auditoria(usuario, accion, modelo, cambios, ip):  # ← RENOMBRAMOS
    # ... código igual ...
```

**¿QUÉ PASA?** 🔴 **ERROR INMEDIATO**

Cuando alguien intenta editar un producto en `editar_producto()` (línea 505):

```python
def editar_producto(request, id):
    # ... código ...
    registrar_auditoria(  # ← FALLA AQUÍ: función no existe
        usuario=request.user,
        accion='EDITAR',
        modelo='Producto',
        cambios={'precio': 100},
        ip=obtener_ip_cliente(request)
    )
```

**RESULTADO:**
```
NameError: name 'registrar_auditoria' is not defined
⚠️ Se rompe toda la auditoría
⚠️ Los cambios se hacen pero no quedan registrados
⚠️ Panel admin pierde funcionalidad crítica
```

**RIESGO:** Crítico (100%) - Deja de funcionar completamente

---

### 2.2 Cambiar Nombre de Campo en Modelo SIN Migración
**Archivo:** `sysApp/models.py`

**CÓDIGO ORIGINAL:**
```python
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
```

**CAMBIO PELIGROSO (DIRECTO EN MODELS.PY):**
```python
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField(default=0)  # ← CAMBIAMOS 'stock'
```

**¿QUÉ PASA?** 🔴 **BASE DE DATOS ROTA**

En `views.py` línea 505, cuando editamos producto:

```python
def editar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.stock = request.POST.get('stock')  # ← FALLA: no existe este campo
    producto.save()
```

**RESULTADO:**
```
AttributeError: 'Producto' object has no attribute 'stock'
🔴 No se pueden editar productos
🔴 Se pierden datos si no hay migración
🔴 La BD tiene un campo que el código no usa
```

**RIESGO:** Crítico (100%) - Inconsistencia base de datos/código

**LO CORRECTO:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 2.3 Cambiar Nombre de Parámetro POST
**Archivo:** `sysApp/templates/paginas/detalleProducto.html` + `sysApp/views.py`

**CÓDIGO ORIGINAL EN TEMPLATE:**
```html
<form method="POST" action="/agregar-carrito/">
    <input type="hidden" name="producto_id" value="{{ producto.id }}">
    <input type="number" name="cantidad" min="1" value="1">
    <button type="submit">Agregar al Carrito</button>
</form>
```

**EN VIEWS.PY (línea 381):**
```python
def agregar_al_carrito(request):
    producto_id = request.POST.get('producto_id')  # Espera este nombre
    cantidad = request.POST.get('cantidad', 1)
```

**CAMBIO PELIGROSO - Solo cambiamos el template:**
```html
<form method="POST" action="/agregar-carrito/">
    <input type="hidden" name="id_producto" value="{{ producto.id }}">  <!-- ← CAMBIAMOS -->
    <input type="number" name="cantidad_seleccionada" min="1" value="1">  <!-- ← CAMBIAMOS -->
    <button type="submit">Agregar al Carrito</button>
</form>
```

**¿QUÉ PASA?** 🔴 **CARRITO NO FUNCIONA**

```python
# El código sigue esperando:
producto_id = request.POST.get('producto_id')  # ← Obtiene None
cantidad = request.POST.get('cantidad', 1)     # ← Obtiene None

# Si producto_id es None:
try:
    producto = Producto.objects.get(id=None)  # ← ERROR: id=None
except Producto.DoesNotExist:
    # Se lanza excepción
```

**RESULTADO:**
```
🔴 Botón "Agregar al Carrito" no funciona
🔴 No hay mensajes de error (solo falla silenciosamente)
🔴 Los usuarios ven el botón pero nada pasa al hacer click
```

**RIESGO:** Crítico (100%) - Carrito roto

---

### 2.4 Cambiar Nombre de Campo en Formulario SIN Actualizar Views
**Archivo:** `sysApp/forms.py` + `sysApp/views.py`

**CÓDIGO ORIGINAL EN FORMS.PY:**
```python
class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen']
```

**EN VIEWS.PY (línea 505):**
```python
def editar_producto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()  # Guarda usando los nombres del formulario
```

**CAMBIO PELIGROSO - Solo en forms.py:**
```python
class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_venta', 'categoria', 'imagen']
        # ← Cambiamos 'precio' por 'precio_venta'
```

**¿QUÉ PASA?** 🔴 **FORMULARIO NO VALIDA**

```
1. Usuario carga formulario de editar producto
2. El formulario espera un campo llamado 'precio_venta' 
3. Pero el HTML original espera 'precio'
4. Campo no aparece en la forma visual
5. Al guardar, falta el precio
6. Producto queda sin precio (NULL o 0)
```

**RESULTADO:**
```
🔴 El campo precio desaparece del formulario
🔴 Se pueden guardar productos sin precio
🔴 El catálogo muestra productos con precio 0
🔴 Los pedidos fallan (no hay precio para calcular total)
```

**RIESGO:** Crítico (100%) - Datos inconsistentes

---

## 3. CAMBIOS MUY PELIGROSOS 🔴

### 3.1 Eliminar Función Completa
**Archivo:** `sysApp/views.py` línea 636

**CÓDIGO ORIGINAL:**
```python
def checkout_mercadopago(request):
    """Crea preferencia de pago en Mercado Pago"""
    carrito = request.session.get('carrito', {})
    
    preference_data = {
        "items": [
            {
                "title": producto['nombre'],
                "quantity": producto['cantidad'],
                "unit_price": float(producto['precio'])
            }
            for producto in carrito.values()
        ]
    }
    
    preference = sdk.preference().create(preference_data)
    return redirect(preference['response']['init_point'])
```

**CAMBIO PELIGROSO:**
```python
# Simplemente eliminamos esta función
# (no hacemos nada)
```

**¿QUÉ PASA?** 🔴 **SISTEMA DE PAGO MUERTO**

En `urls.py`:
```python
urlpatterns = [
    path('checkout/', checkout_mercadopago, name='checkout'),  # ← FALLA: no existe
]
```

**RESULTADO:**
```
🔴 Los usuarios no pueden hacer checkout
🔴 Error 404 o NameError
🔴 Cero ventas
🔴 Dinero perdido
```

**RIESGO:** CATASTRÓFICO (100%) - Sistema no funciona

---

### 3.2 Cambiar Autenticación
**Archivo:** `sysApp/views.py` línea 1395

**CÓDIGO ORIGINAL:**
```python
def panel_admin(request):
    if not request.user.is_superuser:  # ← Verifica que sea admin
        return redirect('inicio')
    
    bajo_stock = Producto.objects.filter(stock__lte=F('stock_minimo'))
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente')
    
    return render(request, 'admin/panel_admin.html', {
        'bajo_stock': bajo_stock,
        'pedidos_pendientes': pedidos_pendientes
    })
```

**CAMBIO PELIGROSO:**
```python
def panel_admin(request):
    # Eliminamos la verificación de superuser
    # if not request.user.is_superuser:
    #     return redirect('inicio')
    
    bajo_stock = Producto.objects.filter(stock__lte=F('stock_minimo'))
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente')
    
    return render(request, 'admin/panel_admin.html', {
        'bajo_stock': bajo_stock,
        'pedidos_pendientes': pedidos_pendientes
    })
```

**¿QUÉ PASA?** 🔴 **SEGURIDAD ROTA**

```
1. Cualquier usuario registrado puede acceder a /admin/
2. Un cliente normal ve: inventario, todas las órdenes, auditoría
3. Alguien malintensionado puede:
   - Ver precios costales
   - Ver datos de otros clientes (direcciones, teléfonos)
   - Cambiar estados de órdenes
   - Manipular inventario
```

**RESULTADO:**
```
🔴 Pérdida de datos privados
🔴 Fraude posible
🔴 Incumplimiento legal (GDPR, CCPA)
🔴 Reputación destruida
```

**RIESGO:** CATASTRÓFICO (100%) - Violación de seguridad

---

### 3.3 Cambiar Lógica de Pago
**Archivo:** `sysApp/views.py` línea 775

**CÓDIGO ORIGINAL:**
```python
def pago_exito(request):
    """Confirma pago exitoso"""
    payment_id = request.GET.get('payment_id')
    
    # Verifica con Mercado Pago
    payment = sdk.payment().get(payment_id)
    
    if payment['response']['status'] == 'approved':  # ← Verifica estado real
        pedido = Pedido.objects.get(mercadopago_id=payment_id)
        pedido.estado = 'confirmado'
        pedido.save()
        return render(request, 'pago_exito.html')
    else:
        return redirect('pago_fallo')
```

**CAMBIO PELIGROSO:**
```python
def pago_exito(request):
    """Confirma pago exitoso"""
    payment_id = request.GET.get('payment_id')
    
    # Simplemente confiamos en lo que dice el cliente
    # (SIN verificar con Mercado Pago)
    
    pedido = Pedido.objects.get(mercadopago_id=payment_id)
    pedido.estado = 'confirmado'  # ← Lo marcamos como pagado SIN verificar
    pedido.save()
    return render(request, 'pago_exito.html')
```

**¿QUÉ PASA?** 🔴 **ESTAFA MASIVA**

```
1. Usuario A va a pagar
2. En URL dice: ?payment_id=12345&status=approved
3. El código NO verifica con Mercado Pago
4. Solo copia lo que el cliente envía
5. Usuario A pone status=rejected pero su pedido se marca como pagado
6. Recibe producto GRATIS
```

**O PEOR:**
```
1. Un atacante crea una URL fake: /pago_exito/?payment_id=99999
2. Accede a esa URL
3. Se crea una orden falsa como "pagada"
4. Recibe producto sin pagar
5. Puedes perder MILES de euros
```

**RESULTADO:**
```
🔴 Pérdida económica total
🔴 Fraude sin control
🔴 Quiebra
```

**RIESGO:** CATASTRÓFICO (100%) - Ruina financiera

---

## 4. TABLA RESUMEN

| Cambio | Dónde | Riesgo | Consecuencia |
|--------|-------|--------|--------------|
| Renombrar variable local | Dentro función | 0% ✅ | Ninguna |
| Cambiar comentarios | Cualquier lugar | 0% ✅ | Ninguna |
| Cambiar CSS/colores | CSS files | 0% ✅ | Solo visual |
| Cambiar mensajes textos | HTML/JS | 0% ✅ | Solo apariencia |
| Renombrar función SIN actualizar llamadas | views.py | 100% 🔴 | NameError - Sistema roto |
| Cambiar campo modelo SIN migración | models.py | 100% 🔴 | BD inconsistente |
| Cambiar parámetro POST SIN actualizar views | Template + views | 100% 🔴 | Formulario no funciona |
| Cambiar campo formulario SIN actualizar modelo | forms.py | 100% 🔴 | Datos incompletos |
| Eliminar función completamente | views.py | 100% 🔴 | Feature muere |
| Eliminar autenticación | views.py | 100% 🔴 | Seguridad rota |
| Cambiar lógica de validación de pago | views.py | 100% 🔴 | Fraude masivo |

---

## 5. REGLA DE ORO

Cuando hagas un cambio, pregúntate:

1. **¿Este cambio toca la lógica de negocio?** (Carrito, pago, órdenes, stock)
   - SÍ → Peligroso ⚠️ → Necesita prueba
   - NO → Continúa a 2

2. **¿Afecta a más de una función?**
   - SÍ → Muy peligroso 🔴 → Necesita actualizar TODOS los lugares
   - NO → Continúa a 3

3. **¿Toca autenticación, seguridad o pagos?**
   - SÍ → CRÍTICO 🔴 → NO LO HAGAS SIN BACKUP
   - NO → Probablemente sea seguro ✅

4. **¿Es solo apariencia o comentarios?**
   - SÍ → Completamente seguro ✅
   - NO → Necesita prueba

---

## 6. CÓMO HACER CAMBIOS SEGURAMENTE

### Paso 1: Identifica DÓNDE se usa
```bash
# En terminal:
grep -r "nombre_funcion" ./
# Muestra TODAS las líneas donde aparece
```

### Paso 2: Actualiza TODOS los lugares
Si cambias:
- Nombre función → actualiza todas las llamadas
- Nombre parámetro POST → actualiza template + views
- Campo modelo → crea migración con `makemigrations`

### Paso 3: Prueba localmente
```bash
python manage.py runserver
# Prueba manualmente cada feature afectada
```

### Paso 4: Haz backup
```bash
# Antes de cambios grandes:
cp -r . backup_$(date +%Y%m%d)
```

---

**Recuerda:** Un pequeño cambio olvidado en un lugar lejano puede romper TODO el sistema.
