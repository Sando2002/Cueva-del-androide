#!/usr/bin/env python
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoCA.settings')
django.setup()

from sysApp.models import AuditoriaInventario

# Obtener todas las auditorias en_proceso
auditorias_en_proceso = AuditoriaInventario.objects.filter(estado='en_proceso')

print("=" * 60)
print("LIMPIANDO AUDITORIAS EN PROCESO ANTIGUAS")
print("=" * 60)
print(f"\nEncontradas: {auditorias_en_proceso.count()} auditorias en estado 'en_proceso'")

if auditorias_en_proceso.exists():
    print("\nCancelando auditorias...")
    for aud in auditorias_en_proceso:
        aud.estado = 'cancelada'
        aud.save()
        print(f"  ✓ {aud.numero_auditoria} -> CANCELADA")
    
    print(f"\n✓ Se cancelaron {auditorias_en_proceso.count()} auditorias")
    
    # Verificar después
    en_proceso = AuditoriaInventario.objects.filter(estado='en_proceso').count()
    print(f"\nAuditorias en proceso ahora: {en_proceso}")
    print("✓ El bloqueo DEBERÍA estar DESACTIVADO ahora")
else:
    print("✓ No hay auditorias en proceso para limpiar")

print("\n" + "=" * 60)
