# Generated migration to fix obsolete pedido states

from django.db import migrations

def fix_pedido_states(apps, schema_editor):
    """Convert 'aprobado' to 'en_preparacion' and 'procesando' to 'listo'"""
    Pedido = apps.get_model('sysApp', 'Pedido')
    
    # Fix 'aprobado' -> 'en_preparacion'
    aprobados = Pedido.objects.filter(estado='aprobado')
    count_aprobados = aprobados.count()
    aprobados.update(estado='en_preparacion')
    print(f"✅ Convertidos {count_aprobados} pedidos de 'aprobado' a 'en_preparacion'")
    
    # Fix 'procesando' -> 'listo'
    procesando = Pedido.objects.filter(estado='procesando')
    count_procesando = procesando.count()
    procesando.update(estado='listo')
    print(f"✅ Convertidos {count_procesando} pedidos de 'procesando' a 'listo'")

def reverse_fix(apps, schema_editor):
    """Reverse migration (not recommended in production)"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('sysApp', '0015_pedido_razon_reembolso_pedido_reembolso_parcial'),
    ]

    operations = [
        migrations.RunPython(fix_pedido_states, reverse_fix),
    ]
