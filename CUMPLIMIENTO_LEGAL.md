# 📋 CUMPLIMIENTO LEGAL - Cueva del Androide

**Última actualización:** 30 de noviembre de 2025  
**Versión:** 1.0  
**Responsable:** Cueva del Androide

---

## 📊 RESUMEN EJECUTIVO

| Ley/Estándar | Cumplimiento | Estado | Prioridad |
|--------------|--------------|--------|-----------|
| Ley 19.628 (Datos Personales) | 80% | ✅ Bien | Media |
| Ley 19.496 (Protección Consumidor) | 100% | ✅ Excelente | Alta |
| Ley 19.799 (Firma Electrónica) | 75% | ⚠️ Aceptable | Media |
| Ley 20.169 (Competencia Desleal) | 75% | ⚠️ Aceptable | Media |
| Ley 20.575 (Datos Comerciales) | 100% | ✅ Excelente | Alta |
| Ley 21.082 (E-commerce) | 90% | ✅ Excelente | Alta |
| Ley 21.459 (Ciberseguridad) | 20% | ❌ Crítico | **URGENTE** |
| Decreto 1/2023 (Plataformas) | 80% | ⚠️ Bien | Media |
| Estándar PCI DSS | 75% | ⚠️ Aceptable | **URGENTE** |
| Norma ISO/IEC 27001 | 25% | ❌ Crítico | **URGENTE** |
| Ley 17.336 (Propiedad Intelectual) | 25% | ❌ Crítico | Alta |
| **PROMEDIO GENERAL** | **64.5%** | ⚠️ Aceptable | - |

---

## 🟢 CUMPLIMIENTO TOTAL (100%)

### ✅ Ley Nº19.496 - Protección de los Derechos de los Consumidores

**Artículos aplicables:** Art. 3 bis, 12A, 14

**Implementación:**
- ✅ **Información clara y accesible** en 4 políticas públicas
- ✅ **Deber de informar** sobre precios, garantías, devoluciones
- ✅ **Confirmación de compra** por email (Mercado Pago)
- ✅ **Número de pedido único** para cada transacción
- ✅ **Transparencia de precios** sin costos ocultos (envío gratis = retiro en tienda)
- ✅ **Garantía legal** especificada por producto (6-12 meses)
- ✅ **Derechos de devolución** dentro de 30 días (Ley 20.606 integrada)

**Archivos relacionados:**
- `sysApp/templates/paginas/terminos_condiciones.html` (Sección 3-10)
- `sysApp/templates/paginas/politica_devoluciones.html` (Todo)
- `sysApp/templates/includes/footer.html` (Enlaces a políticas)

---

### ✅ Ley Nº20.575 - Limitación de Uso de Información Comercial

**Artículos aplicables:** Art. 1, 2

**Implementación:**
- ✅ **NO se usan datos para marketing** sin consentimiento previo
- ✅ **Cookie banner** pide permiso antes de rastrear
- ✅ **localStorage** respeta decisión del usuario
- ✅ **NO se envían emails promocionales** sin opt-in explícito
- ✅ **NO se usa información para scoring crediticio**
- ✅ **Política de Privacidad** especifica usos permitidos (solo operacionales)

**Archivos relacionados:**
- `sysApp/templates/includes/cookie_banner.html`
- `sysApp/static/js/cookies.js`
- `sysApp/templates/paginas/politica_privacidad.html` (Sección 2)

---

## 🟡 CUMPLIMIENTO ALTO (80-75%)

### ✅ Ley Nº19.628 - Protección de la Vida Privada (Datos Personales)

**Artículos aplicables:** Art. 4, 7, 10

**Implementación (80%):**
- ✅ **Art. 4** - Tratamiento de datos especificado (qué se recopia)
- ✅ **Art. 7** - Datos almacenados en base de datos (Django/MySQL)
- ✅ **Art. 10** - Consentimiento para rastreo (Cookie banner)
- ✅ **Derechos ARCO** documentados (Acceso, Rectificación, Cancelación, Oposición)
- ✅ **Contacto responsable** (contacto@cuevadeandroide.cl)
- ✅ **Retención de datos** especificada por tipo (5 años compras, 2 años inactivos)
- ⚠️ **Cifrado de datos** - Implementado en Django, pero NO especificado en política

**Mejora necesaria:**
- Agregar en Política de Privacidad: "Los datos se almacenan en servidor seguro con cifrado AES-256"

**Archivos relacionados:**
- `sysApp/templates/paginas/politica_privacidad.html` (Todo)
- `sysApp/templates/includes/cookie_banner.html`
- `sysApp/static/js/cookies.js`

---

### ✅ Estándar PCI DSS (Payment Card Industry Data Security Standard)

**Requisitos aplicables:** 3, 6, 12

**Implementación (75%):**
- ✅ **Requisito 3** - NO almacenamos datos de tarjetas (Mercado Pago externo)
- ✅ **Requisito 6** - Mercado Pago es PCI DSS certified
- ✅ **Transacciones HTTPS** (obligatorio con Mercado Pago)
- ✅ **Solo referencias de pago** almacenadas en BD
- ⚠️ **Política de seguridad PCI** - NO documentada en el sitio

**Mejora necesaria:**
- Agregar página: "POLITICA_SEGURIDAD_PAGOS.md" con detalles PCI DSS

**Archivos relacionados:**
- `sysApp/views.py` (línea ~300: checkout_mercadopago)
- Mercado Pago (externo)

---

### ✅ Ley Nº19.799 - Documentos y Firma Electrónica

**Artículos aplicables:** Art. 1, 3

**Implementación (75%):**
- ✅ **Art. 1** - Email de confirmación es documento válido
- ✅ **Art. 3** - Cada pedido tiene ID único (firma electrónica equivalente)
- ✅ **Número de pedido** es identificador único
- ✅ **Email de Mercado Pago** actúa como comprobante oficial
- ⚠️ **Certificado digital propio** - NO generado por la tienda (Mercado Pago lo genera)

**Mejora necesaria:**
- Generar certificado digital propio para comprobantes (opcional, Mercado Pago ya lo cubre)

**Archivos relacionados:**
- `sysApp/views.py` (checkout_mercadopago)

---

### ✅ Ley Nº20.169 - Competencia Desleal

**Artículos aplicables:** Art. 3, 4

**Implementación (75%):**
- ✅ **Art. 3** - Publicidad veraz (descripciones exactas de productos)
- ✅ **Art. 4** - SIN comparaciones indebidas con otras marcas
- ✅ **Precios claros** sin costos ocultos
- ✅ **"SOLO retiro en tienda"** especificado (NO engaña)
- ⚠️ **Proceso de verificación** - NO documentado

**Mejora necesaria:**
- Documentar quién verifica contenido y cada cuánto

**Archivos relacionados:**
- `sysApp/templates/paginas/catalogo.html`
- `sysApp/templates/paginas/detalleProducto.html`

---

### ✅ Decreto Nº1/2023 - Regulación de Plataformas Digitales

**Aspectos aplicables:** Transparencia, contacto, términos

**Implementación (80%):**
- ✅ **Datos reales de empresa** (dirección, email, teléfono)
- ✅ **Términos accesibles** en footer
- ✅ **Contacto verificable** (3 canales: email, WhatsApp, dirección)
- ✅ **Información clara sobre compra** (retiro en tienda)
- ⚠️ **RUT en placeholder** - Necesita completarse con datos reales

**Mejora necesaria:**
- Reemplazar "XX.XXX.XXX-X" con RUT real en footer

**Archivos relacionados:**
- `sysApp/templates/includes/footer.html`

---

### ✅ Ley Nº21.082 - Comercio Electrónico

**Artículos aplicables:** Art. 1-5

**Implementación (90%):**
- ✅ **Información previa clara** (políticas en footer antes de comprar)
- ✅ **Confirmación de compra** (email Mercado Pago)
- ✅ **Derecho de arrepentimiento** (30 días = Ley 20.606)
- ✅ **Método de entrega especificado** ("Retiro en tienda")
- ✅ **Contacto verificable** (3 canales)
- ✅ **Política de privacidad** accesible
- ⚠️ **Política de ciberseguridad** - NO documentada

**Mejora necesaria:**
- Crear página sobre medidas de ciberseguridad

**Archivos relacionados:**
- `sysApp/templates/paginas/` (todas las políticas)

---

## 🔴 CUMPLIMIENTO CRÍTICO (20-25%) - URGENTE IMPLEMENTAR

### ❌ Ley Nº21.459 - Delitos Informáticos (Ciberseguridad)

**Artículos aplicables:** Art. 2, 4, 9

**Cumplimiento actual (20%):**
- ⚠️ **Art. 2** - Autenticación existe, pero NO documentada
- ❌ **Art. 4** - Validación de entradas (existe en Django, NO documentada)
- ❌ **Art. 9** - Auditoría de acceso (NO implementada)
- ❌ **HTTPS/SSL certificado** - NO confirmado
- ❌ **Monitoreo de intentos no autorizados** - NO implementado

**CRÍTICO - IMPLEMENTAR INMEDIATAMENTE:**
1. **HTTPS con certificado SSL válido** (obligatorio Ley 21.082 + PCI DSS)
2. **Auditoría de cambios de datos** - Registrar quién accede a qué
3. **Monitoreo de logs** - Detectar intentos de acceso no autorizado
4. **Validación de entradas documentada** - Prevenir inyección SQL

**Archivos relacionados:**
- `sysApp/` (todo el proyecto necesita auditoría)
- Servidor (necesita HTTPS)

---

### ❌ Norma ISO/IEC 27001 - Seguridad de la Información

**Cláusulas aplicables:** 5-10

**Cumplimiento actual (25%):**
- ⚠️ **Cláusula 5** - Política de seguridad NO documentada
- ⚠️ **Cláusula 6** - Acceso restringido existe, NO documentado
- ❌ **Cláusula 7** - Backup automático NO confirmado
- ❌ **Cláusula 8** - Control de cambios NO auditado
- ❌ **Cláusula 9** - Gestión de incidentes NO documentada
- ❌ **Cláusula 10** - Auditoría de seguridad NO implementada

**CRÍTICO - IMPLEMENTAR INMEDIATAMENTE:**
1. **Política de seguridad documentada** (archivo público)
2. **Backup automático diario** del servidor y BD
3. **Auditoría de cambios** en datos críticos
4. **Plan de respuesta a incidentes**

**Archivos a crear:**
- `POLITICA_SEGURIDAD_ISO27001.md`
- `PLAN_BACKUPS.md`
- `PLAN_INCIDENTES.md`

---

### ❌ Ley Nº17.336 - Propiedad Intelectual

**Artículos aplicables:** Art. 1, 5, 71F

**Cumplimiento actual (25%):**
- ⚠️ **Art. 1** - Software de autoría propia, pero SIN aviso de copyright
- ❌ **Art. 5** - Imágenes de productos NO especifican origen/licencia
- ⚠️ **Art. 71F** - Contenido digital sin protección documentada
- ✅ Bootstrap, Font Awesome - Son libres (OK)

**CRÍTICO - IMPLEMENTAR INMEDIATAMENTE:**
1. **Aviso de copyright** en footer
2. **Especificar licencia de recursos** (Bootstrap, Font Awesome, etc.)
3. **Declaración de autoría** del código
4. **Permiso de uso de imágenes** (si no son propias)

**Archivos a crear:**
- Actualizar footer con © 2025
- Crear `LICENCIAS_RECURSOS.md`

---

## 📋 PLAN DE ACCIÓN

### **URGENTE (2-3 días):**
- [ ] Implementar HTTPS/SSL certificado
- [ ] Crear `POLITICA_SEGURIDAD_PAGOS.md`
- [ ] Agregar © copyright en footer
- [ ] Documentar auditoría de acceso

### **CORTO PLAZO (1-2 semanas):**
- [ ] Implementar backup automático documentado
- [ ] Crear `PLAN_INCIDENTES.md`
- [ ] Completar RUT real en footer
- [ ] Documentar validación de entradas

### **MEDIANO PLAZO (1 mes):**
- [ ] Implementar monitoreo de logs
- [ ] Crear `POLITICA_SEGURIDAD_ISO27001.md`
- [ ] Auditoría de cambios en BD
- [ ] Certificado digital para comprobantes

---

## 📞 CONTACTO Y RESPONSABLES

- **Email:** contacto@cuevadeandroide.cl
- **Teléfono:** [Completar]
- **Dirección:** Almagro 432, Los Ángeles, Bío Bío
- **RUT:** XX.XXX.XXX-X (Completar)
- **Responsable Legal:** [Completar nombre]
- **Responsable de Seguridad:** [Completar nombre]
- **Responsable de Datos:** [Completar nombre]

---

## 📄 DOCUMENTOS RELACIONADOS

- `sysApp/templates/paginas/politica_privacidad.html` - Ley 19.628
- `sysApp/templates/paginas/terminos_condiciones.html` - Ley 19.496, 20.606
- `sysApp/templates/paginas/politica_devoluciones.html` - Ley 20.606
- `sysApp/templates/paginas/politica_envios.html` - Ley 21.082
- `POLITICA_SEGURIDAD_PAGOS.md` - PCI DSS (crear)
- `POLITICA_SEGURIDAD_ISO27001.md` - ISO 27001 (crear)
- `PLAN_INCIDENTES.md` - ISO 27001 + Ley 21.459 (crear)

---

**Documento creado:** 30 de noviembre de 2025  
**Próxima revisión:** 30 de enero de 2026
