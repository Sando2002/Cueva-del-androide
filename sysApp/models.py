from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título del Producto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    precio = models.IntegerField(verbose_name="Precio")  # Cambio a IntegerField
    foto = models.ImageField(upload_to='productos/', verbose_name="Foto del Producto")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    stock_minimo = models.IntegerField(default=5, verbose_name="Stock Mínimo")
    stock_maximo = models.IntegerField(default=50, verbose_name="Stock Máximo")
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE,
        related_name='productos',
        null=True,
        blank=True,
        verbose_name="Categoría"
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.titulo

    def clean(self):
        # Verifica que 'precio' no sea menor o igual a cero
        if self.precio is not None and self.precio <= 0:
            raise ValidationError('El precio debe ser un valor positivo.')
        
        # Verifica que 'stock' no sea negativo
        if self.stock is not None and self.stock < 0:
            raise ValidationError('El stock no puede ser negativo.')
        
        # Verifica que stock_minimo sea menor que stock_maximo
        if self.stock_minimo and self.stock_maximo and self.stock_minimo >= self.stock_maximo:
            raise ValidationError('El stock mínimo debe ser menor que el stock máximo.')
    
    def necesita_reorden(self):
        """Verifica si el producto necesita reorden"""
        return self.stock <= self.stock_minimo
    
    def stock_excedido(self):
        """Verifica si el stock excede el máximo"""
        return self.stock > self.stock_maximo

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('usuario', 'producto')
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f'{self.usuario.username if self.usuario else "Anónimo"} - {self.producto.titulo} (x{self.cantidad})'

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def clean(self):
        # Validar que la cantidad no exceda el stock disponible
        if self.cantidad > self.producto.stock:
            raise ValidationError(f'La cantidad no puede exceder el stock disponible ({self.producto.stock}).')


class Pedido(models.Model):
    """
    Modelo para guardar los pedidos realizados con Mercado Pago.
    Guarda la información del pago, estado y referencia con MP.
    """
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En Preparación'),
        ('listo', 'Listo para Recoger'),
        ('recogido', 'Recogido'),
        ('rechazado', 'Rechazado'),
        ('cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    numero_pedido = models.CharField(max_length=50, unique=True, verbose_name="Número de Pedido")
    total = models.IntegerField(verbose_name="Total del Pedido")
    reembolso_parcial = models.IntegerField(default=0, verbose_name="Reembolso Parcial Realizado")
    razon_reembolso = models.TextField(blank=True, null=True, verbose_name="Razón del Reembolso")
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_PAGO,
        default='pendiente',
        verbose_name="Estado del Pago"
    )
    # Referencia a Mercado Pago
    preferencia_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID de Preferencia de MP"
    )
    payment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID de Pago de MP"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_pago = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Pago")
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'Pedido {self.numero_pedido} - {self.usuario.username} - {self.estado}'


class ItemPedido(models.Model):
    """
    Modelo para guardar los items de cada pedido.
    Copia los detalles del producto para histórico.
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.IntegerField(verbose_name="Precio Unitario")
    
    class Meta:
        verbose_name = 'Item del Pedido'
        verbose_name_plural = 'Items del Pedido'
    
    def __str__(self):
        return f'{self.pedido.numero_pedido} - {self.producto.titulo if self.producto else "Producto eliminado"}'
    
    def subtotal(self):
        return self.precio_unitario * self.cantidad


class Notificacion(models.Model):
    """
    Modelo para notificaciones en la plataforma.
    Se crean automáticamente cuando ocurren eventos importantes.
    """
    TIPOS_NOTIFICACION = [
        ('pedido_creado', 'Pedido Creado'),
        ('pedido_pagado', 'Pedido Pagado'),
        ('pedido_procesando', 'Pedido en Procesamiento'),
        ('pedido_listo', 'Pedido Listo para Recoger'),
        ('pedido_rechazado', 'Pedido Rechazado'),
        ('pedido_cancelado', 'Pedido Cancelado'),
        ('stock_bajo', 'Stock Bajo'),
        ('pago_fallido', 'Pago Fallido'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=255, verbose_name="Título")
    mensaje = models.TextField(verbose_name="Mensaje")
    tipo = models.CharField(
        max_length=50,
        choices=TIPOS_NOTIFICACION,
        verbose_name="Tipo de Notificación"
    )
    leida = models.BooleanField(default=False, verbose_name="Leída")
    
    # Para relacionar con el objeto que generó la notificación
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notificaciones',
        verbose_name="Pedido Relacionado"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notificaciones',
        verbose_name="Producto Relacionado"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'{self.usuario.username} - {self.titulo} ({self.get_tipo_display()})'


class Auditoria(models.Model):
    """
    Modelo para registrar todas las acciones de administración.
    Proporciona un historial completo de quién hizo qué, cuándo y en qué objeto.
    """
    TIPOS_ACCION = [
        ('crear_producto', 'Crear Producto'),
        ('editar_producto', 'Editar Producto'),
        ('eliminar_producto', 'Eliminar Producto'),
        ('actualizar_stock', 'Actualizar Stock'),
        ('cambiar_estado_pedido', 'Cambiar Estado de Pedido'),
        ('crear_categoria', 'Crear Categoría'),
        ('editar_categoria', 'Editar Categoría'),
        ('eliminar_categoria', 'Eliminar Categoría'),
        ('otro', 'Otra Acción'),
    ]
    
    MODELOS = [
        ('Producto', 'Producto'),
        ('Pedido', 'Pedido'),
        ('Categoria', 'Categoría'),
        ('ItemPedido', 'Item de Pedido'),
        ('otro', 'Otro'),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='auditorias',
        verbose_name="Usuario Admin"
    )
    
    accion = models.CharField(
        max_length=50,
        choices=TIPOS_ACCION,
        verbose_name="Tipo de Acción"
    )
    
    modelo = models.CharField(
        max_length=50,
        choices=MODELOS,
        verbose_name="Modelo Afectado"
    )
    
    objeto_id = models.IntegerField(
        verbose_name="ID del Objeto",
        help_text="ID del objeto que fue modificado"
    )
    
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada de la acción"
    )
    
    cambios = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Cambios",
        help_text="Diferencias antes/después en formato JSON"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Dirección IP"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Acción"
    )
    
    class Meta:
        verbose_name = 'Auditoría'
        verbose_name_plural = 'Auditorías'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['usuario', '-fecha_creacion']),
            models.Index(fields=['modelo', 'objeto_id']),
        ]
    
    def __str__(self):
        return f'{self.usuario.username} - {self.get_accion_display()} ({self.modelo}) - {self.fecha_creacion.strftime("%d/%m/%Y %H:%M")}'


# ============ MODELOS DE GESTIÓN DE INVENTARIO ============

class MovimientoInventario(models.Model):
    """
    Registra todas las entradas y salidas de inventario.
    Permite auditoria completa del movimiento de stock.
    """
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada (Compra)'),
        ('salida_venta', 'Salida (Venta)'),
        ('salida_devolucion', 'Salida (Devolución)'),
        ('salida_daño', 'Salida (Producto Dañado)'),
        ('ajuste', 'Ajuste de Inventario'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO, verbose_name="Tipo de Movimiento")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    stock_anterior = models.IntegerField(verbose_name="Stock Anterior")
    stock_posterior = models.IntegerField(verbose_name="Stock Posterior")
    motivo = models.TextField(blank=True, null=True, verbose_name="Motivo")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Movimiento")
    
    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-fecha']
    
    def __str__(self):
        return f'{self.producto.titulo} - {self.get_tipo_display()} ({self.cantidad} unidades) - {self.fecha.strftime("%d/%m/%Y")}'


class AuditoriaInventario(models.Model):
    """
    Registra auditorías físicas de inventario (inventario cíclico).
    Compara el stock del sistema con el conteo físico.
    """
    ESTADO_AUDITORIA = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    TIPO_AUDITORIA = [
        ('total', 'Auditoría Total'),
        ('categoria', 'Por Categoría'),
        ('producto', 'Productos Específicos'),
        ('ciclico', 'Inventario Cíclico'),
    ]
    
    numero_auditoria = models.CharField(max_length=50, unique=True, verbose_name="Número de Auditoría")
    tipo = models.CharField(max_length=20, choices=TIPO_AUDITORIA, default='ciclico', verbose_name="Tipo")
    estado = models.CharField(max_length=20, choices=ESTADO_AUDITORIA, default='pendiente', verbose_name="Estado")
    usuario_creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='auditorias_creadas')
    usuario_revisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='auditorias_revisadas')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoría (si aplica)")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_inicio = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Inicio")
    fecha_finalizacion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Finalización")
    
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = 'Auditoría de Inventario'
        verbose_name_plural = 'Auditorías de Inventario'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'Auditoría {self.numero_auditoria} - {self.get_estado_display()}'


class DetalleAuditoria(models.Model):
    """
    Detalle de cada producto auditado en una auditoría.
    Registra la diferencia entre sistema y conteo físico.
    """
    auditoria = models.ForeignKey(AuditoriaInventario, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    stock_sistema = models.IntegerField(verbose_name="Stock en Sistema")
    stock_fisico = models.IntegerField(verbose_name="Stock Físico Contado")
    diferencia = models.IntegerField(verbose_name="Diferencia")  # stock_fisico - stock_sistema
    
    observacion = models.TextField(blank=True, null=True, verbose_name="Observación")
    ajustado = models.BooleanField(default=False, verbose_name="¿Se Ajustó?")
    
    class Meta:
        verbose_name = 'Detalle de Auditoría'
        verbose_name_plural = 'Detalles de Auditoría'
    
    def save(self, *args, **kwargs):
        self.diferencia = self.stock_fisico - self.stock_sistema
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.producto.titulo} - Diferencia: {self.diferencia:+d}'


class OrdenCompra(models.Model):
    """
    Registro de órdenes de compra a proveedores.
    Controla entradas de inventario planificadas.
    """
    ESTADO_ORDEN = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('enviada', 'Enviada'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero_orden = models.CharField(max_length=50, unique=True, verbose_name="Número de Orden")
    proveedor = models.CharField(max_length=100, verbose_name="Proveedor")
    estado = models.CharField(max_length=20, choices=ESTADO_ORDEN, default='pendiente', verbose_name="Estado")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_entrega_esperada = models.DateField(verbose_name="Fecha de Entrega Esperada")
    fecha_recepcion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Recepción Real")
    
    total_estimado = models.IntegerField(verbose_name="Total Estimado (CLP)")
    total_real = models.IntegerField(blank=True, null=True, verbose_name="Total Real (CLP)")
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'
        ordering = ['-fecha_creacion']
    
    def calcular_total_estimado(self):
        """Calcula el total estimado basado en los detalles"""
        total = sum(
            detalle.subtotal_solicitado() 
            for detalle in self.detalles.all()
        )
        return total
    
    def calcular_total_recibido(self):
        """Calcula el total recibido basado en los detalles"""
        total = sum(
            detalle.subtotal_recibido() 
            for detalle in self.detalles.all()
        )
        return total

    def __str__(self):
        return f'Orden {self.numero_orden} - {self.get_estado_display()}'


class DetalleOrdenCompra(models.Model):
    """
    Detalle de productos en una orden de compra.
    """
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_solicitada = models.IntegerField(verbose_name="Cantidad Solicitada")
    cantidad_recibida = models.IntegerField(default=0, verbose_name="Cantidad Recibida")
    precio_unitario = models.IntegerField(verbose_name="Precio Unitario")
    
    class Meta:
        verbose_name = 'Detalle de Orden de Compra'
        verbose_name_plural = 'Detalles de Órdenes de Compra'
    
    def subtotal_solicitado(self):
        return self.cantidad_solicitada * self.precio_unitario
    
    def subtotal_recibido(self):
        return self.cantidad_recibida * self.precio_unitario
    
    def __str__(self):
        return f'{self.producto.titulo} - {self.cantidad_solicitada} unidades'
