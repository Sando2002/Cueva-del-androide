## Solución de Problemas de Caché en Navegadores

Si los estilos CSS, imágenes o JavaScript no se actualizan en dispositivos móviles, sigue estos pasos:

### ¿Por qué sucede esto?

Los navegadores cachean archivos estáticos (CSS, JS, imágenes) para cargar páginas más rápido. Esto puede causar que no veas cambios recientes.

### Soluciones

#### 1. **Limpiar caché del navegador (Recomendado)**

**En Chrome (PC o Móvil):**
- Presiona `Ctrl+Shift+Supr` (Windows) o `Cmd+Shift+Supr` (Mac)
- Selecciona "Cookies y otros datos del sitio"
- Selecciona "Archivos almacenados en caché"
- Presiona "Borrar datos"

**En Safari (iPhone/iPad):**
1. Abre Configuración
2. Safari → Historial
3. Toca "Borrar historial, datos del sitio web"

**En navegador móvil:**
- Busca Configuración → Privacidad/Historial → Borrar datos

#### 2. **Recargar página forzadamente**

**PC:**
- `Ctrl+F5` (Windows) o `Cmd+Shift+R` (Mac)

**Móvil:**
- Mantén presionado el botón de recargar hasta que aparezca "Recargar sin caché" (en algunos navegadores)

#### 3. **Solución técnica implementada**

Se ha actualizado el código con:
- ✅ Versiones de archivos CSS y JS (`?v=1.0`)
- ✅ Headers de Cache-Control en el servidor
- ✅ Cache de 1 hora para CSS/JS (fuerza recarga cada hora)
- ✅ Cache de 30 días para imágenes

Esto significa que después de 1 hora, tu navegador recargará automáticamente los archivos CSS y JS.

#### 4. **Para desarrollo local (desactivar caché)**

Si estás desarrollando, puedes desactivar el caché:

**Chrome DevTools:**
1. Abre Chrome DevTools (`F12`)
2. Ve a Settings (⚙️)
3. Marca "Disable cache (while DevTools is open)"

**Firefox DevTools:**
1. Abre Firefox DevTools (`F12`)
2. Ve a Settings
3. Marca "Disable HTTP Cache (when toolbox is open)"

### Verificación

Después de limpiar caché, visita la página en modo incógnito/privado para confirmar que ves los cambios nuevos.

### Contacto

Si el problema persiste después de limpiar caché, verifica que:
1. ✅ Los archivos CSS/JS estén en la carpeta correcta
2. ✅ El servidor Django esté ejecutándose
3. ✅ La URL sea correcta
