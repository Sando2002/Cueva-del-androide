# 📊 MÓDULO DE REPORTES Y ANÁLISIS

## Descripción General
El módulo de reportes proporciona análisis completo del desempeño de la tienda en línea, permitiendo tomar decisiones basadas en datos reales.

## Secciones Disponibles

### 1. 📈 ESTADÍSTICAS GENERALES
Muestra KPIs principales del mes actual:
- **Ingresos Este Mes**: Total de ventas aprobadas en el mes
- **Pedidos Este Mes**: Cantidad de pedidos completados
- **Ticket Promedio**: Monto promedio por pedido
- **Tasa de Conversión**: Porcentaje de carritos convertidos a pedidos

### 2. 🏆 TOP 10 PRODUCTOS MÁS VENDIDOS
Lista los 10 productos con mayor cantidad de unidades vendidas, mostrando:
- Nombre del producto
- Cantidad total vendida
- Ingresos generados
- Clasificación por posición

**Uso**: Identificar bestsellers y optimizar promociones

---

### 3. 🔄 ROTACIÓN DE INVENTARIO (Últimos 30 días)
Analiza qué tan rápido se vende el inventario:
- **Rotación (%)**: Indicador de velocidad de venta
  - ✓ **Verde (50%+)**: Excelente rotación
  - ⚠ **Amarillo (25-50%)**: Rotación moderada
  - ✗ **Rojo (<25%)**: Baja rotación

**Fórmula**: `(Ventas / (Stock + Ventas)) × 100`

**Uso**: Identificar productos lentos de vender y considerar:
- Rebajas
- Promociones
- Discontinuación

---

### 4. ⚠️ ANÁLISIS DE RIESGO FINANCIERO
Evalúa la salud financiera de la tienda:

#### Indicadores:
- **Nivel de Riesgo**: 
  - 🟢 BAJO: Situación financiera saludable
  - 🟡 MEDIO: Requiere atención en rotación
  - 🔴 ALTO: Riesgo potencial de quiebra

- **Ingresos Totales**: Suma de todas las ventas aprobadas
- **Inversión en Inventario**: Valor total del stock
- **Relación Ingresos/Inversión**: 
  - >100%: Ingresos > Inversión ✓
  - 60-100%: Relación moderada
  - <60%: Ingresos insuficientes

- **Productos Sin Venta**: Cantidad de SKUs nunca vendidos

#### Criterios de Riesgo:
```
ALTO   → Relación < 30% O Tasa venta < 0.5
MEDIO  → Relación < 60% O Tasa venta < 1.0
BAJO   → Otros casos
```

**Uso**: Tomar decisiones sobre gestión de stock y presupuesto

---

### 5. 📈 DESEMPEÑO POR CATEGORÍA
Análisis detallado por cada categoría de productos:

Muestra:
- **Productos**: Total en la categoría
- **En Stock**: Cantidad disponible
- **Ventas**: Unidades vendidas
- **Stock Total**: Unidades en almacén
- **Ingresos**: Dinero generado

**Uso**: 
- Identificar categorías rentables
- Optimizar surtido por categoría
- Evaluar desempeño relativo

---

### 6. 📦 PRODUCTOS OBSOLETOS (Sin venta en 60 días)
Lista productos que no se han vendido en los últimos 2 meses:

Información:
- Stock actual
- Precio unitario
- **Inversión Bloqueada**: Dinero atrapado en ese inventario
- Acción recomendada:
  - ⚠ >10 unidades: Considerar promoción
  - ⚡ 1-10 unidades: Liquidar stock
  - ✓ Agotado: Monitorear

**Uso**: Liberar capital invertido en productos sin demanda

---

## Cómo Acceder

### Opción 1: Desde el Panel Principal
1. Ir a **Panel de Administración**
2. Click en botón **"Ver Reportes"**

### Opción 2: Desde el Menú Lateral
1. Panel Admin → **Reportes**

### URL Directa
```
/panel-admin/reportes/
```

---

## Interpretación de Datos

### Ejemplo 1: Bajo Rotación
**Situación**: Producto con 5% de rotación
**Interpretación**: De cada 100 unidades en stock, apenas 5 se venden
**Acción**: 
- Rebajar precio 10-20%
- Destacar en promociones
- Considerar descontinuar

### Ejemplo 2: Alto Riesgo Financiero
**Situación**: 
- Ingresos: $500,000
- Inversión: $2,000,000
- Relación: 25%

**Interpretación**: El inventario vale 4x los ingresos mensuales
**Acciones**:
- Mejorar rotación
- Reducir stock lentamente
- Revisar política de compras

### Ejemplo 3: Categoría Top
**Situación**: Categoría "Anime" con $50,000 en ingresos
**Interpretación**: Es la más rentable
**Acciones**:
- Ampliar surtido
- Dedicar presupuesto de marketing
- Mejorar stock de bestsellers

---

## Frecuencia Recomendada de Revisión

- **Diaria**: Monitorear ingresos y pedidos
- **Semanal**: Revisar rotación y stock crítico
- **Mensual**: Análisis completo y riesgo financiero
- **Trimestral**: Evaluación de categorías y estrategia

---

## Exportación de Datos

_Nota: Funcionalidad próxima_
Se planea agregar la opción de exportar reportes a:
- Excel (.xlsx)
- PDF
- CSV

---

## Preguntas Frecuentes

**P: ¿Qué significa "Rotación"?**
R: Es la velocidad con que vende un producto. Mayor rotación = vende rápido.

**P: ¿Cómo reduzco el riesgo de quiebra?**
R: Aumenta ingresos (más ventas) o reduce inversión en inventario.

**P: ¿Por qué un producto no aparece en rotación?**
R: No tuvo ventas en los últimos 30 días. Revisa en "Productos Obsoletos".

**P: ¿Puedo cambiar el período de análisis?**
R: Actualmente es fijo (30 y 60 días). Próximas versiones permitirán personalizar.

---

## Versión
v1.0 - Noviembre 2025
