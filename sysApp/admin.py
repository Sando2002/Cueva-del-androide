# Register your models here.
from django.contrib import admin
from .models import (Producto, Categoria, Pedido, ItemPedido, MovimientoInventario, 
                     AuditoriaInventario, DetalleAuditoria, OrdenCompra, DetalleOrdenCompra)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo','descripcion', 'precio', 'foto', 'stock','categoria', 'stock_minimo', 'stock_maximo')
    list_filter = ('categoria',)
    search_fields = ('titulo',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero_pedido', 'usuario', 'total', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('numero_pedido', 'usuario__username')
    readonly_fields = ('numero_pedido', 'preferencia_id', 'payment_id', 'fecha_creacion', 'fecha_pago')

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario')
    search_fields = ('pedido__numero_pedido', 'producto__titulo')

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'stock_anterior', 'stock_posterior', 'fecha')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__titulo', 'motivo')
    readonly_fields = ('fecha',)

@admin.register(AuditoriaInventario)
class AuditoriaInventarioAdmin(admin.ModelAdmin):
    list_display = ('numero_auditoria', 'tipo', 'estado', 'fecha_inicio', 'usuario_creador')
    list_filter = ('estado', 'tipo', 'fecha_inicio')
    search_fields = ('numero_auditoria',)
    readonly_fields = ('numero_auditoria', 'fecha_inicio')

@admin.register(DetalleAuditoria)
class DetalleAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('auditoria', 'producto', 'stock_sistema', 'stock_fisico', 'diferencia', 'ajustado')
    list_filter = ('ajustado', 'auditoria__fecha_inicio')
    search_fields = ('producto__titulo', 'auditoria__numero_auditoria')

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'proveedor', 'estado', 'fecha_creacion', 'fecha_entrega_esperada')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('numero_orden', 'proveedor')
    readonly_fields = ('numero_orden', 'fecha_creacion')

@admin.register(DetalleOrdenCompra)
class DetalleOrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'cantidad_solicitada', 'cantidad_recibida', 'precio_unitario')
    search_fields = ('orden__numero_orden', 'producto__titulo')
