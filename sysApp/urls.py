from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', redirect_to_login),
    path('registro/', views.registrar, name='registro'),

    path('admin/login/', redirect_to_login),
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('accounts/login/', views.login_view, name='login'), 
    path('catalogo/categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('detalle/<int:pk>/', views.detalleProducto, name='detalleProducto'),
    path('catalogo/buscar/', views.buscar_productos, name='buscar_productos'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('detalle_carrito/', views.detalle_carrito, name='detalle_carrito'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar_cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('logout/', views.logout_view, name='logout'),
    path('editar_producto/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    # Páginas estáticas: políticas
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
    path('politica-devoluciones/', views.politica_devoluciones, name='politica_devoluciones'),
    path('politica-envios/', views.politica_envios, name='politica_envios'),
    # API: obtener contador del carrito
    path('api/carrito/count/', views.get_carrito_count, name='get_carrito_count'),
    
    # Pago con Mercado Pago
    path('checkout/mercadopago/', views.checkout_mercadopago, name='checkout_mercadopago'),
    path('pago/exito/', views.pago_exito, name='pago_exito'),
    path('pago/fallo/', views.pago_fallo, name='pago_fallo'),
    path('pago/pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('verificar-pago/<str:preferencia_id>/', views.verificar_pago, name='verificar_pago'),
    path('api/mercadopago/webhook/', views.mercadopago_webhook, name='mercadopago_webhook'),
    
    # Mis Pedidos
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    
    # Acciones en pedidos
    path('pedido/<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
    path('pedido/<int:pedido_id>/reintentar-pago/', views.reintentar_pago, name='reintentar_pago'),
    path('pedido/<int:pedido_id>/marcar-recogido/', views.marcar_pedido_recogido, name='marcar_pedido_recogido'),
    
    # Mi Cuenta
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    
    # Notificaciones
    path('notificaciones/', views.listar_notificaciones, name='notificaciones'),
    path('notificaciones/marcar-leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('api/notificaciones/sin-leer/', views.get_notificaciones_sin_leer, name='get_notificaciones_sin_leer'),
    
    # Recuperación de contraseña personalizada
    path('recuperar-contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),
    path('recuperar-contraseña/confirmacion/', views.recuperar_contraseña_confirmacion, name='recuperar_contraseña_confirmacion'),
    path('cambiar-contraseña-temporal/', views.cambiar_contraseña_temporal, name='cambiar_contraseña_temporal'),
    
    # Panel de Administración
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('panel-admin/productos/', views.admin_productos, name='admin_productos'),
    path('panel-admin/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('panel-admin/pedidos/<int:pedido_id>/editar/', views.editar_pedido, name='editar_pedido'),
    path('panel-admin/auditoria/', views.admin_auditoria, name='admin_auditoria'),
    path('panel-admin/reportes/', views.admin_reportes, name='admin_reportes'),
    path('panel-admin/actualizar-stock/<int:producto_id>/', views.actualizar_stock, name='actualizar_stock'),
    path('panel-admin/cambiar-estado-pedido/<int:pedido_id>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    
    # Gestión de Inventario
    path('panel-admin/inventario/', views.gestionar_inventario, name='gestionar_inventario'),
    path('panel-admin/inventario/movimiento/<int:producto_id>/', views.registrar_movimiento, name='registrar_movimiento'),
    path('panel-admin/inventario/orden-compra/crear/', views.crear_orden_compra, name='crear_orden_compra'),
    path('panel-admin/inventario/orden-compra/<int:orden_id>/', views.ver_orden_compra, name='ver_orden_compra'),
    path('panel-admin/inventario/auditoria/crear/', views.crear_auditoria_inventario, name='crear_auditoria_inventario'),
    path('panel-admin/inventario/auditoria/<int:auditoria_id>/revisar/', views.revisar_auditoria, name='revisar_auditoria'),
    path('panel-admin/inventario/auditoria/<int:auditoria_id>/cancelar/', views.cancelar_auditoria, name='cancelar_auditoria'),
    path('panel-admin/inventario/auditorias-abiertas/', views.auditorias_abiertas, name='auditorias_abiertas'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
