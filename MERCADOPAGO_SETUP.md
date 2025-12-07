# Integración de Mercado Pago - Guía de Configuración

## ¿Qué se implementó?

Se ha integrado una pasarela de pago completa con **Mercado Pago** en tu tienda. El flujo permite que los usuarios compren sus productos de forma segura.

## Requisitos Previos

1. **Cuenta de Mercado Pago**
   - Regístrate en https://www.mercadopago.com/developers/panel
   - Crea una aplicación
   - Obtén tus credenciales:
     - `PUBLIC_KEY` (clave pública)
     - `ACCESS_TOKEN` (token de acceso)

## Configuración

### 1. Agregar Credenciales

Edita el archivo `proyectoCA/settings.py` y reemplaza los valores placeholder:

```python
# Configuración de Mercado Pago
MERCADOPAGO_PUBLIC_KEY = 'APP_USR-xxxxxxxxxxxxxxxx'  # Tu clave pública
MERCADOPAGO_ACCESS_TOKEN = 'APP_USR-xxxxxxxxxxxxxxxx'  # Tu token de acceso
```

⚠️ **IMPORTANTE**: Nunca hagas commit de tus credenciales a Git. Usa variables de entorno en producción:

```python
import os
MERCADOPAGO_PUBLIC_KEY = os.environ.get('MERCADOPAGO_PUBLIC_KEY', 'APP_USR-...')
MERCADOPAGO_ACCESS_TOKEN = os.environ.get('MERCADOPAGO_ACCESS_TOKEN', 'APP_USR-...')
```

### 2. Base de Datos

Las migraciones ya se han aplicado. Los modelos creados son:

- **Pedido**: Guarda la información del pedido (total, estado, referencia MP)
- **ItemPedido**: Guarda los items de cada pedido

## Flujo de Pago

```
1. Usuario agrega productos al carrito
   ↓
2. Hace clic en "Pagar con Mercado Pago"
   ↓
3. Se crea un Pedido en base de datos
   ↓
4. Se redirige a Mercado Pago para que complete el pago
   ↓
5. Después del pago, MP redirige al usuario a:
   - /pago/exito/ (si fue aprobado)
   - /pago/fallo/ (si fue rechazado)
   - /pago/pendiente/ (si está procesando)
   ↓
6. El webhook (/api/mercadopago/webhook/) actualiza el estado del pedido
```

## Nuevas URLs

- `/checkout/mercadopago/` - Inicia el proceso de pago
- `/pago/exito/` - Página de pago exitoso
- `/pago/fallo/` - Página de pago rechazado
- `/pago/pendiente/` - Página de pago pendiente
- `/api/mercadopago/webhook/` - Webhook para recibir notificaciones de MP

## Cambios en el Carrito

El botón "Iniciar compra" en `detalle_carrito.html` ahora redirige a:
```
Pagar con Mercado Pago → /checkout/mercadopago/
```

Cuando el usuario hace clic:
1. Se crea un Pedido con el total actual
2. Se crean ItemPedido para cada producto
3. Se vacía el carrito
4. Se redirecciona a Mercado Pago

## Estados de Pago

Los pedidos pueden tener los siguientes estados:

| Estado | Descripción |
|--------|-------------|
| `pendiente` | Pago no iniciado o esperando confirmación |
| `procesando` | Pago en proceso |
| `aprobado` | Pago confirmado ✓ Se decrementa el stock |
| `rechazado` | Pago rechazado ✗ |
| `cancelado` | Usuario canceló el pago |

## Webhook de Mercado Pago

El webhook escucha notificaciones de MP y actualiza automáticamente:
1. El estado del pedido
2. El ID de pago de MP
3. **Decrementa el stock** cuando el pago es aprobado

### Configurar Webhook en MP

1. Ve a https://www.mercadopago.com/developers/panel
2. En tu aplicación, ve a "Configuración"
3. En "Webhooks", agrega:
   ```
   https://tudominio.com/api/mercadopago/webhook/
   ```

## Pruebas en Modo Sandbox

Mercado Pago ofrece un modo sandbox para testing:

1. En tu panel, cambia a **Modo Sandbox**
2. Usa tarjetas de prueba:
   - Éxito: `4509 9535 6623 3704`
   - Fallo: `4000 0000 0000 0002`
   - Pendiente: `4000 0000 0000 0010`

3. Fecha: cualquier fecha futura (ej: 12/25)
4. CVV: cualquier número de 3 dígitos

## Panel Admin

Puedes ver todos los pedidos en:
```
/admin/ → Pedidos
```

Aquí puedes:
- Ver el estado de cada pedido
- Ver los items del pedido
- Buscar por número de pedido o usuario
- Filtrar por estado y fecha

## Personalización

### Cambiar Moneda

En `views.py`, función `checkout_mercadopago()`, busca:
```python
"currency_id": "CLP"  # Cambiar según tu país
```

Valores comunes:
- `ARS` - Peso Argentino
- `BRL` - Real Brasileño
- `CLP` - Peso Chileno
- `MXN` - Peso Mexicano
- `UYU` - Peso Uruguayo

### Personalizar URLs de Retorno

En `checkout_mercadopago()`, puedes personalizar:
```python
"back_urls": {
    "success": request.build_absolute_uri('/pago/exito/'),
    "failure": request.build_absolute_uri('/pago/fallo/'),
    "pending": request.build_absolute_uri('/pago/pendiente/')
}
```

## Problemas Comunes

### "Error al crear la preferencia de pago"
- Verifica que tus credenciales sean correctas
- Comprueba que tengas conexión a internet
- Revisa los logs de Django

### El webhook no se actualiza
- Asegúrate de estar en modo Producción (no Sandbox) en tu código
- Verifica que la URL del webhook sea accesible desde MP
- Revisa los logs en el panel de MP

### El stock no se decrementa
- Verifica que el pago tenga estado `approved`
- Comprueba que el webhook se esté ejecutando correctamente
- Revisa en el admin que el pedido tenga estado "Aprobado"

## Seguridad

✓ Se valida que el usuario esté autenticado
✓ Se valida el carrito antes de crear el pedido
✓ Se valida la respuesta de Mercado Pago en el webhook
✓ Se usa `select_for_update()` para evitar race conditions (opcional, ver: https://docs.djangoproject.com/en/5.2/ref/models/querysets/#select-for-update)

## Próximos Pasos (Opcional)

1. **Notificaciones por email**: Envía confirmación de pago al usuario
2. **Comprobante PDF**: Genera factura al aprobar pago
3. **Integración con envío**: Calcula costo de envío automáticamente
4. **Descuentos/Cupones**: Agrega códigos de descuento
5. **Devoluciones**: Implementa sistema de reembolsos

---

**Documentación oficial**: https://www.mercadopago.com/developers/es/reference
