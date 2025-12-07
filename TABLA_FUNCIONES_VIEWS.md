# Tabla de Contenidos - Views.py

## NOTIFICACIONES
| Función | Línea | Qué hace |
|---------|-------|----------|
| `crear_notificacion()` | 22 | Crea notificación para usuario |
| `notificar_pedido_creado()` | 45 | Alerta cuando se crea pedido |
| `notificar_pedido_cambio_estado()` | 56 | Alerta cuando cambia estado pedido |
| `notificar_stock_bajo_admin()` | 104 | Alerta a admin si stock es bajo |

## UTILIDADES
| Función | Línea | Qué hace |
|---------|-------|----------|
| `obtener_ip_cliente()` | 127 | Obtiene IP del usuario |
| `registrar_auditoria()` | 137 | Registra cambios en auditoría |
| `registrar_cambios()` | 160 | Detecta diferencias antes/después |
| `es_superusuario()` | 198 | Verifica si es admin |

## PÚBLICO - HOME
| Función | Línea | Qué hace |
|---------|-------|----------|
| `inicio()` | 194 | Página principal |

## AUTENTICACIÓN
| Función | Línea | Qué hace |
|---------|-------|----------|
| `registrar()` | 204 | Crear nueva cuenta |
| `login_view()` | 468 | Iniciar sesión |
| `logout_view()` | 496 | Cerrar sesión |
| `recuperar_contraseña()` | 1174 | Solicitar reset de contraseña |
| `recuperar_contraseña_confirmacion()` | 1213 | Confirmar nuevo password |
| `cambiar_contraseña_temporal()` | 1228 | Cambiar password temporal |

## CATÁLOGO
| Función | Línea | Qué hace |
|---------|-------|----------|
| `catalogo()` | 284 | Listar todos productos con paginación |
| `buscar_productos()` | 328 | Búsqueda por título |
| `productos_por_categoria()` | 350 | Filtrar por categoría |
| `detalleProducto()` | 372 | Ver detalles de 1 producto |

## CARRITO
| Función | Línea | Qué hace |
|---------|-------|----------|
| `agregar_al_carrito()` | 381 | Añadir producto al carrito |
| `detalle_carrito()` | 413 | Ver contenido del carrito |
| `eliminar_del_carrito()` | 430 | Quitar producto del carrito |
| `actualizar_cantidad()` | 439 | Cambiar cantidad de artículo |
| `get_carrito_count()` | 611 | Obtener cantidad de items (AJAX) |

## ADMIN - PRODUCTOS
| Función | Línea | Qué hace |
|---------|-------|----------|
| `editar_producto()` | 505 | Editar datos de producto |
| `eliminar_producto()` | 581 | Eliminar producto |
| `admin_productos()` | 1475 | Listar productos para admin |

## PAGO - MERCADO PAGO
| Función | Línea | Qué hace |
|---------|-------|----------|
| `checkout_mercadopago()` | 636 | Crear orden y redirigir a MP |
| `pago_exito()` | 775 | Confirmar pago exitoso |
| `pago_fallo()` | 822 | Pago fue rechazado |
| `pago_pendiente()` | 850 | Pago pendiente de confirmación |
| `verificar_pago()` | 870 | Verificar estado de pago |
| `mercadopago_webhook()` | 927 | Webhook de MP (automático) |

## PEDIDOS - USUARIO
| Función | Línea | Qué hace |
|---------|-------|----------|
| `mis_pedidos()` | 998 | Ver historial de pedidos del usuario |
| `cancelar_pedido()` | 1280 | Cancelar pedido pendiente |
| `reintentar_pago()` | 1312 | Reintenta pagar pedido rechazado |

## PERFIL
| Función | Línea | Qué hace |
|---------|-------|----------|
| `mi_cuenta()` | 1118 | Ver perfil del usuario |
| `editar_perfil()` | 1140 | Modificar datos personales |

## ADMIN - DASHBOARD
| Función | Línea | Qué hace |
|---------|-------|----------|
| `panel_admin()` | 1449 | Dashboard principal de admin |

## ADMIN - PEDIDOS
| Función | Línea | Qué hace |
|---------|-------|----------|
| `admin_pedidos()` | 1526 | Listar todos los pedidos |
| `cambiar_estado_pedido()` | 1641 | Cambiar estado pedido (admin) |

## ADMIN - NOTIFICACIONES
| Función | Línea | Qué hace |
|---------|-------|----------|
| `listar_notificaciones()` | 1549 | Ver todas las notificaciones |
| `get_notificaciones_sin_leer()` | 1569 | Obtener notificaciones no leídas (AJAX) |
| `marcar_notificacion_leida()` | 1590 | Marcar notificación como leída |

## ADMIN - INVENTARIO
| Función | Línea | Qué hace |
|---------|-------|----------|
| `actualizar_stock()` | 1604 | Cambiar stock manualmente |

## ADMIN - AUDITORÍA
| Función | Línea | Qué hace |
|---------|-------|----------|
| `admin_auditoria()` | 1702 | Ver historial de cambios |

## ADMIN - REPORTES
| Función | Línea | Qué hace |
|---------|-------|----------|
| `admin_reportes()` | 1750 | Dashboard de reportes/ventas |

---

## RESUMEN
| Categoría | Cantidad |
|-----------|----------|
| Total funciones | 48 |
| Autenticación | 6 funciones |
| Catálogo | 4 funciones |
| Carrito | 5 funciones |
| Pago | 6 funciones |
| Pedidos | 3 funciones |
| Admin | 9 funciones |
| Notificaciones | 4 funciones |
| Utilidades | 4 funciones |
| Páginas estáticas | 1 función |
| Otros | 6 funciones |

---

**Archivo:** `sysApp/views.py`  
**Total de líneas:** 2183  
**Última actualización:** 29 de noviembre de 2025
