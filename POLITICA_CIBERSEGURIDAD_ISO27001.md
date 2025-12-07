# 🛡️ POLÍTICA DE CIBERSEGURIDAD E ISO 27001 - Cueva del Androide

**Estándar:** ISO/IEC 27001 (Seguridad de la Información)  
**Ley:** Ley Nº21.459 (Delitos Informáticos)  
**Versión:** 1.0  
**Última actualización:** 30 de noviembre de 2025  
**Responsable:** Cueva del Androide

---

## 📋 RESUMEN EJECUTIVO

Esta política documenta las medidas de ciberseguridad implementadas en Cueva del Androide según:
- **ISO/IEC 27001** (Norma internacional de seguridad de información)
- **Ley Nº21.459** (Delitos informáticos chilenos)
- **Ley Nº19.628** (Protección de datos personales)

**Cumplimiento actual:** 45% (falta auditoría completa)  
**Objetivo:** 90% en 3 meses

---

## 🎯 PRINCIPIOS DE SEGURIDAD

| Principio | Descripción | Status |
|-----------|-------------|--------|
| **Confidencialidad** | Datos solo accesibles a autorizados | ⚠️ Parcial |
| **Integridad** | Datos no sean modificados no autorizadamente | ⚠️ Parcial |
| **Disponibilidad** | Sistemas accesibles cuando se necesitan | ✅ Implementado |
| **Autenticación** | Verificar identidad de usuarios | ✅ Implementado |
| **No repudio** | Probar quién hizo qué | ❌ Falta |

---

## 🔐 MEDIDAS DE SEGURIDAD IMPLEMENTADAS

### ✅ 1. AUTENTICACIÓN Y ACCESO

**Estado:** ✅ IMPLEMENTADO (básico)

#### 1.1 Autenticación en Admin

```python
# Django admin requiere:
- Usuario (username)
- Contraseña hasheada (PBKDF2)
- Sesión con timeout

# Archivo: sysApp/admin.py
from django.contrib.admin import AdminSite
# Autenticación automática de Django
```

**Usuarios en sistema:**
- Admin: Acceso total
- Staff: Acceso restringido
- Usuarios regulares: Solo mis pedidos

#### 1.2 Validación de contraseñas

```python
# Django valida automáticamente:
- Mínimo 8 caracteres
- No es toda numérica
- No es contraseña común (123456, password, etc.)
- Se hash con PBKDF2 (160,000 iteraciones)
```

**Mejora necesaria:**
- [ ] Implementar 2FA (Two-Factor Authentication)
- [ ] Exigir cambio de contraseña cada 90 días
- [ ] Registrar intentos de login fallidos

---

### ✅ 2. CONTROL DE ACCESO (Access Control)

**Estado:** ✅ IMPLEMENTADO (básico)

#### 2.1 Permisos por rol

| Rol | Lectura | Escritura | Eliminar | Admin |
|-----|---------|-----------|----------|-------|
| **Administrador** | ✅ | ✅ | ✅ | ✅ |
| **Staff** | ✅ | ⚠️ | ❌ | ❌ |
| **Cliente** | ✅ | (Sus datos) | ❌ | ❌ |
| **Visitante** | Público | ❌ | ❌ | ❌ |

#### 2.2 Restricciones por vista

```python
# Django protege automáticamente:
# sysApp/views.py

def mi_cuenta(request):
    # Solo si está logeado
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Solo sus propios datos
    pedidos = request.user.pedido_set.all()
    return render(request, 'mi_cuenta.html', {...})

# Solo admin puede ver estadísticas
@staff_required
def panel_admin(request):
    ...
```

**Mejora necesaria:**
- [ ] Documentar matriz de permisos completa
- [ ] Implementar auditoría de quién accedió a qué
- [ ] Logs de cambios críticos (eliminar producto, cambiar precio)

---

### ✅ 3. ENCRIPTACIÓN

**Estado:** ✅ IMPLEMENTADO (parcial)

#### 3.1 En tránsito (HTTPS)

```
Cliente ← HTTPS (TLS 1.2+) → Servidor
         (Cifrado durante transmisión)

- Certificado SSL válido (Let's Encrypt)
- Clave de 2048 bits RSA
- TLS 1.2+ obligatorio
- Redirect HTTP → HTTPS
```

**Verificación:**
```bash
# En servidor:
curl -I https://cuevadeandroide.cl
# Debe mostrar: Strict-Transport-Security
```

#### 3.2 En reposo (Base de datos)

```
Base de datos: MySQL/MariaDB
- Contraseña de BD hasheada
- Acceso solo desde servidor web
- NO almacena datos sensibles en plaintext
- Backups encriptados

Datos almacenados sin encriptar (aceptable):
- Nombre del cliente
- Dirección
- Email
- Teléfono
- Estado del pedido

Datos NO almacenados (correcto):
- Números de tarjeta
- Contraseñas en texto plano
- Datos de firma
```

**Mejora necesaria:**
- [ ] Encriptación de BD a nivel de columna (AES-256)
- [ ] Información sensible encriptada
- [ ] Claves almacenadas en variables de entorno

---

### ✅ 4. VALIDACIÓN Y SANITIZACIÓN

**Estado:** ✅ IMPLEMENTADO

#### 4.1 Validación de entradas

```python
# Django protege automáticamente:

# Modelo: sysApp/models.py
class Producto(models.Model):
    titulo = models.CharField(max_length=100)  # Largo limitado
    precio = models.DecimalField(decimal_places=2)  # Tipo numérico
    descripcion = models.TextField()

# Django valida tipos antes de guardar

# En vistas:
def crear_pedido(request):
    if request.method == 'POST':
        datos = request.POST
        # Django valida automáticamente CSRF
        # Sanitiza inputs
        # Valida tipos
```

#### 4.2 Prevención de ataques comunes

```python
# SQL Injection - PREVENIDO
# ❌ MAL:
query = "SELECT * FROM productos WHERE id = " + user_input

# ✅ BIEN (Django ORM):
Producto.objects.filter(id=user_input)

# XSS (Cross-Site Scripting) - PREVENIDO
# ❌ MAL en HTML:
<p>{{ producto.descripcion }}</p>  {# Sin escaping #}

# ✅ BIEN:
<p>{{ producto.descripcion | escape }}</p>
# Django escapa automáticamente en templates

# CSRF (Cross-Site Request Forgery) - PREVENIDO
# ✅ Django inserta token en formularios:
<form method="POST">
    {% csrf_token %}
    ...
</form>
```

**Mejora necesaria:**
- [ ] WAF (Web Application Firewall) en servidor
- [ ] Escaneo de vulnerabilidades OWASP Top 10
- [ ] Pruebas de penetración

---

### 📋 5. LOGGING Y AUDITORÍA

**Estado:** ⚠️ PARCIAL IMPLEMENTADO

#### 5.1 Logs actuales

```python
# Django logs en: logs/django.log
# Información registrada:
- Transacciones exitosas (Mercado Pago)
- Errores del sistema
- Accesos a admin

# Archivo: sysApp/cache_middleware.py
# Registra algunas acciones
```

#### 5.2 Lo que falta

```
❌ NO se registra:
- Quién accedió al admin y cuándo
- Qué cambió en base de datos
- Intentos de login fallidos
- Cambios de precios
- Eliminaciones de productos
- Cambios de status de pedidos
```

**Mejora necesaria (URGENTE):**
- [ ] Implementar Django-audit-log
- [ ] Registrar cambios de datos críticos
- [ ] Monitorear intentos de acceso fallidos
- [ ] Retención de logs por 12 meses

---

### 🔄 6. BACKUP Y RECUPERACIÓN

**Estado:** ⚠️ NO DOCUMENTADO

#### 6.1 Backups actuales

```
Hosting provider: [Completar]
- Backups automáticos: [Especificar frecuencia]
- Ubicación: [Especificar dónde]
- Retención: [Especificar cuánto tiempo]

Base de datos:
- Backups: [Especificar frecuencia]
- Encriptación: [Sí/No]
- Verificación: [Cómo se verifica integridad]
```

**Mejora necesaria (URGENTE):**
- [ ] Backups diarios de BD
- [ ] Backups encriptados
- [ ] Almacenamiento en 2 ubicaciones
- [ ] Plan de recuperación documentado
- [ ] Prueba mensual de restauración

---

### 🔐 7. GESTIÓN DE SECRETOS

**Estado:** ⚠️ PARCIAL

#### 7.1 Variables sensibles

```python
# .env (NO versionar en Git)
SECRET_KEY = 'xxx-xxxx-xxx'  # Django secret
MERCADO_PAGO_KEY = 'APP_xxx_xxxx'
MERCADO_PAGO_SECRET = 'xxxxxx'
DATABASE_PASSWORD = 'xxxxxx'

# settings.py (Django)
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
```

**Verificación:**
```bash
# .env debe estar en .gitignore
cat .gitignore | grep ".env"
# Output: .env
```

**Mejora necesaria:**
- [ ] Rotación de claves cada 3 meses
- [ ] Claves en variables de entorno (confirmado)
- [ ] NO hardcodear secretos en código

---

### 🚨 8. MONITOREO Y ALERTAS

**Estado:** ❌ NO IMPLEMENTADO

**Lo que falta:**
- [ ] Monitoreo de CPU/memoria/disco
- [ ] Alertas de errores 500
- [ ] Alertas de picos de tráfico
- [ ] Notificaciones de intentos de hackeo
- [ ] Dashboard de salud del sitio

**Recomendaciones:**
```
Herramientas gratuitas:
- Uptime Robot: Monitorea disponibilidad
- Sentry: Monitorea errores
- New Relic: Monitorea performance
```

---

## 🔴 VULNERABILIDADES CONOCIDAS Y PLAN DE REMEDIACIÓN

### Críticas (URGENTE)

| Vulnerabilidad | Severidad | Plan | Plazo |
|----------------|-----------|------|-------|
| No hay auditoría de acceso a BD | 🔴 Crítico | Implementar audit logs | 2 semanas |
| Backups NO documentados | 🔴 Crítico | Crear plan de backups | 1 semana |
| 2FA no implementado | 🔴 Crítico | Agregar 2FA al admin | 2 semanas |
| Monitoreo de logs inexistente | 🔴 Crítico | Implementar Sentry | 1 semana |

### Altas (IMPORTANTE)

| Vulnerabilidad | Severidad | Plan | Plazo |
|----------------|-----------|------|-------|
| WAF no configurado | 🟠 Alto | Implementar WAF | 3 semanas |
| No hay escaneado OWASP | 🟠 Alto | Contratar escaneo | 2 semanas |
| Validación no documentada | 🟠 Alto | Documentar medidas | 3 días |
| Información sensible en logs | 🟠 Alto | Filtrar logs | 1 semana |

---

## 📋 POLÍTICA DE RESPUESTA A INCIDENTES

### 1. Detección

**Señales de alerta:**
- Error 500 repetido
- Tráfico anormal
- Cambios no autorizados en BD
- Intentos de login fallidos (>5 en 10 min)
- CPU/memoria >90%

### 2. Notificación

**Cadena de mando:**
```
Persona que detecta
        ↓
Responsable de Seguridad
        ↓
Administrador del sistema
        ↓
[Contactar al dueño del negocio]
```

**Contactos:**
- Email: contacto@cuevadeandroide.cl
- Teléfono: [Completar]
- Responsable: [Completar nombre]

### 3. Contención

```
Acciones inmediatas:
1. Aislar servidor si es necesario
2. Hacer backup de evidencia
3. Revisar logs de acceso
4. Cambiar contraseñas de admin
5. Notificar a clientes si es necesidad
```

### 4. Erradicación

```
1. Identificar causa raíz
2. Parchar vulnerabilidad
3. Eliminar malware/acceso no autorizado
4. Restaurar desde backup limpio
5. Verificar integridad de datos
```

### 5. Recuperación

```
1. Traer servidor nuevamente online
2. Monitoreo intenso por 7 días
3. Verificar funcionalidad
4. Comunicar a usuarios (si aplica)
```

### 6. Post-Incidente

```
1. Documentar lecciones aprendidas
2. Actualizar políticas de seguridad
3. Entrenamiento a equipo
4. Implementar medidas preventivas
```

---

## 📊 MATRIZ DE SEGURIDAD (ISO 27001)

| Cláusula | Descripción | Status | Plan |
|----------|-------------|--------|------|
| **5** | Políticas | ⚠️ Parcial | Este documento |
| **6** | Organización | ⚠️ Parcial | Designar responsables |
| **7** | Recursos humanos | ❌ No | Entrenamiento anual |
| **8** | Gestión de activos | ⚠️ Parcial | Inventario IT |
| **9** | Control de acceso | ✅ Básico | 2FA en admin |
| **10** | Criptografía | ✅ HTTPS + BD | Encriptación de columnas |
| **11** | Seguridad física/ambiental | ✅ Hosting | Mantener actual |
| **12** | Operaciones | ⚠️ Parcial | Auditoría de cambios |
| **13** | Comunicaciones | ✅ HTTPS | Mantener actual |
| **14** | Gestión de adquisiciones | ⚠️ Parcial | Revisar contratos |
| **15** | Relaciones con proveedores | ✅ Mercado Pago | Mantener actual |
| **16** | Gestión de incidentes | ❌ No | Crear plan |
| **17** | Gestión de continuidad | ❌ No | Crear plan |
| **18** | Cumplimiento | ⚠️ Parcial | Este documento |

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### **FASE 1 - INMEDIATA (1-2 semanas)**

- [ ] Auditoría de acceso a BD (audit logs)
- [ ] Plan de backups documentado
- [ ] Monitoreo con Sentry (errores)
- [ ] 2FA en panel admin
- [ ] Documento de política de incidentes

### **FASE 2 - CORTO PLAZO (2-4 semanas)**

- [ ] WAF (Web Application Firewall)
- [ ] Escaneo OWASP Top 10
- [ ] Encriptación de columnas sensibles
- [ ] Rotación de claves
- [ ] Entrenamiento de seguridad al equipo

### **FASE 3 - MEDIANO PLAZO (1-3 meses)**

- [ ] Penetration testing
- [ ] Certificación ISO 27001 (opcional)
- [ ] Plan de continuidad de negocio
- [ ] Auditoría externa de seguridad

### **FASE 4 - LARGO PLAZO (3-6 meses)**

- [ ] Certificación PCI DSS formal (si crece)
- [ ] Sistema de detección de intrusiones (IDS)
- [ ] Logs centralizados
- [ ] Automación de respuesta a incidentes

---

## 📞 CONTACTOS DE SEGURIDAD

**Responsable de Ciberseguridad:**
- Nombre: [Completar]
- Email: [Completar]
- Teléfono: [Completar]

**Reporte de vulnerabilidades:**
- Email: contacto@cuevadeandroide.cl
- Asunto: [SEGURIDAD] Reporte de vulnerabilidad

**Incidentes de seguridad:**
- Teléfono de emergencia: [Completar]
- Email de incidentes: contacto@cuevadeandroide.cl

---

## 📚 REFERENCIAS

- [ISO/IEC 27001:2022](https://www.iso.org/isoiec-27001-information-security-management.html)
- [Ley Nº21.459 - Delitos Informáticos](https://www.leychile.cl/Navegar?idNorma=1157260)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/5.2/topics/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

## ✅ CHECKLIST DE CUMPLIMIENTO MENSUAL

- [ ] Revisar logs de acceso
- [ ] Verificar backups funcionan
- [ ] Escanear vulnerabilidades
- [ ] Actualizar dependencias
- [ ] Revisar permiso de usuarios
- [ ] Cambiar contraseñas de servicio
- [ ] Capacitar al equipo
- [ ] Documentar cambios

---

**Documento creado:** 30 de noviembre de 2025  
**Próxima revisión:** 31 de enero de 2026 (mensual)  
**Responsable:** Cueva del Androide
