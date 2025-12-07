#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoCA.settings')
django.setup()

from sysApp.models import AuditoriaInventario

# Ver todas las auditorias y sus estados
print("=" * 60)
print("ESTADO DE AUDITORIAS EN LA BASE DE DATOS")
print("=" * 60)

auditorias = AuditoriaInventario.objects.all().values('id', 'numero_auditoria', 'estado', 'fecha_finalizacion')
print("\nTodas las auditorias:")
for aud in auditorias:
    print(f"  ID: {aud['id']}")
    print(f"    Número: {aud['numero_auditoria']}")
    print(f"    Estado: {aud['estado']}")
    print(f"    Finalizada: {aud['fecha_finalizacion']}")
    print()

# Contar auditorias en proceso
en_proceso = AuditoriaInventario.objects.filter(estado='en_proceso').count()
print(f"✓ Auditorias EN PROCESO: {en_proceso}")

# Contar completadas
completadas = AuditoriaInventario.objects.filter(estado='completada').count()
print(f"✓ Auditorias COMPLETADAS: {completadas}")

# Contar otras
pendientes = AuditoriaInventario.objects.filter(estado='pendiente').count()
canceladas = AuditoriaInventario.objects.filter(estado='cancelada').count()
print(f"✓ Auditorias PENDIENTES: {pendientes}")
print(f"✓ Auditorias CANCELADAS: {canceladas}")

print("\n" + "=" * 60)
if en_proceso == 0:
    print("✓ NO HAY AUDITORIAS EN PROCESO - El bloqueo DEBERÍA estar DESACTIVADO")
else:
    print("⚠️ HAY AUDITORIAS EN PROCESO - El bloqueo DEBERÍA estar ACTIVO")
print("=" * 60)
