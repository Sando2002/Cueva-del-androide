# ✅ CHECKLIST DE DEPLOYMENT - RAILWAY

Usa este checklist para asegurar que todo está listo. ¡Marca conforme avances!

---

## 📋 FASE 1: PREPARACIÓN LOCAL (Antes de GitHub)

### 1.1 Verificar Código
- [ ] Django funciona localmente: `python manage.py runserver`
- [ ] No hay errores de sintaxis
- [ ] La BD MySQL local funciona
- [ ] Todos los archivos estáticos están en su lugar

### 1.2 Verificar Archivos Necesarios
- [ ] ✅ Procfile existe
- [ ] ✅ runtime.txt existe
- [ ] ✅ requirements.txt existe y actualizado
- [ ] ✅ .env existe (local)
- [ ] ✅ .env.example existe (para Railway)
- [ ] ✅ .gitignore existe

### 1.3 Verificar Configuración
- [ ] ✅ settings.py usa `config()` para variables
- [ ] ✅ WhiteNoise está en MIDDLEWARE
- [ ] ✅ STATIC_ROOT configurado
- [ ] ✅ DATABASES usa variables de entorno

### 1.4 Instalar Dependencias
- [ ] `pip install gunicorn whitenoise python-decouple`
- [ ] `pip freeze > requirements.txt`
- [ ] Verificar que requirements.txt tiene ~30 paquetes

### 1.5 Preparar Archivos Estáticos
- [ ] `python manage.py collectstatic --noinput`
- [ ] Verificar que `staticfiles/` fue creado

---

## 📋 FASE 2: GIT Y GITHUB

### 2.1 Preparar Git
- [ ] `git init` (si es necesario)
- [ ] `git add .`
- [ ] `git status` (verifica que .env está ignorado)
- [ ] `git commit -m "Setup para Railway"`

### 2.2 Crear Repositorio en GitHub
- [ ] Ve a https://github.com/new
- [ ] Crea un repo llamado "tiendaanime"
- [ ] NO inicialices con README (tienes código local)

### 2.3 Conectar y Subir
- [ ] `git branch -M main`
- [ ] `git remote add origin https://github.com/TU_USUARIO/tiendaanime.git`
- [ ] `git push -u origin main`
- [ ] Verifica que los archivos están en GitHub

### 2.4 Verificar en GitHub
- [ ] ✅ Procfile está visible
- [ ] ✅ requirements.txt está actualizado
- [ ] ✅ .env NO está visible (porque está en .gitignore)
- [ ] ✅ README.md o RAILWAY_QUICK_START.md visible

---

## 📋 FASE 3: RAILWAY SETUP

### 3.1 Crear Cuenta
- [ ] Ve a https://railway.app
- [ ] Login con GitHub (recomendado)
- [ ] Verifica tu email
- [ ] ¡Bienvenido con créditos gratis!

### 3.2 Crear Base de Datos MySQL
- [ ] Click "New Project"
- [ ] Selecciona "Database" → "MySQL"
- [ ] Espera a que se cree (2-3 minutos)
- [ ] **COPIA ESTAS CREDENCIALES:**
  - [ ] Database Host
  - [ ] Database Port
  - [ ] Database User
  - [ ] Database Password
  - [ ] Database Name
- [ ] Prueba la conexión

### 3.3 Importar tu BD Actual
**Opción A - phpMyAdmin (más fácil):**
- [ ] En Railway MySQL, abre la consola
- [ ] Carga tu archivo `tiendaanime.sql`
- [ ] Verifica que se importó correctamente

**Opción B - Comando (si sabes usar mysql-cli):**
```bash
mysql -h HOST -u USER -p DATABASE < tiendaanime.sql
```
- [ ] Ejecuta el comando
- [ ] Verifica que los datos están presentes

### 3.4 Crear el Proyecto Django
- [ ] Click "New Project"
- [ ] Selecciona "GitHub Repo"
- [ ] Autentica GitHub
- [ ] Selecciona el repo "tiendaanime"
- [ ] Espera a que Railway configure

### 3.5 Configurar Variables de Entorno
En tu proyecto Django, ve a "Variables" y añade:

**Variables de Django:**
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY=tu-clave-super-segura-123456` (genera una nueva)

**Variables de BD MySQL:**
- [ ] `DB_ENGINE=django.db.backends.mysql`
- [ ] `DB_NAME=` (copia de Railway MySQL)
- [ ] `DB_USER=` (copia de Railway MySQL)
- [ ] `DB_PASSWORD=` (copia de Railway MySQL)
- [ ] `DB_HOST=` (copia de Railway MySQL)
- [ ] `DB_PORT=3306`

**Variables de Hosts:**
- [ ] `ALLOWED_HOSTS=tuapp.railway.app`
- [ ] `CSRF_TRUSTED_ORIGINS=https://tuapp.railway.app`

**Variables de Mercado Pago:**
- [ ] `MERCADOPAGO_PUBLIC_KEY=APP_USR-93bc5673-82fd-4165-94b4-194c7160b4ff`
- [ ] `MERCADOPAGO_ACCESS_TOKEN=APP_USR-7207881648330267-111519-a66d30ce1599365c02d3c34ef1619608-2992706644`

### 3.6 Conectar la BD (si es necesario)
- [ ] En Railway, ve a tu proyecto Django
- [ ] Click "Plugins"
- [ ] Verifica que MySQL está vinculada
- [ ] Las variables de BD deberían estar auto-rellenadas

---

## 📋 FASE 4: DEPLOYMENT

### 4.1 Iniciar Deploy
- [ ] En Railway, ve a "Deployments"
- [ ] Verifica que el deploy está en progreso
- [ ] Espera a que termine (2-3 minutos)

### 4.2 Verificar Deploy
- [ ] El status debe estar en verde (SUCCESS)
- [ ] Verifica los logs, no debe haber errores
- [ ] Copia la URL de tu app

### 4.3 Prueba la Aplicación
- [ ] Ve a tu URL de Railway (ej: https://tuapp.railway.app)
- [ ] ¿Carga la página? ✅
- [ ] ¿Funciona el login? ✅
- [ ] ¿Funciona la BD? ✅
- [ ] ¿Se cargan los CSS/JS? ✅

### 4.4 Pruebas Funcionales
- [ ] Navega por tu tienda
- [ ] Intenta crear un producto
- [ ] Intenta hacer un pedido (sin pagar)
- [ ] Verifica que todo está en la BD
- [ ] Prueba el carrito

---

## 📋 FASE 5: PRODUCCIÓN (Después del Deploy)

### 5.1 Monitoreo
- [ ] Revisa los logs regularmente
- [ ] Configura alertas en Railway (opcional)
- [ ] Monitorea el uso de créditos

### 5.2 Backups
- [ ] Exporta tu BD MySQL regularmente
- [ ] Guarda copias locales
- [ ] Prueba que puedes restaurar

### 5.3 Seguridad (Importante)
- [ ] Cambia todas las credenciales de prueba
- [ ] Actualiza MERCADOPAGO_PUBLIC_KEY y TOKEN con tus datos reales
- [ ] Usa una SECRET_KEY nueva y segura
- [ ] Configura HTTPS (Railway lo hace automáticamente)

### 5.4 Dominio Personalizado (Opcional)
- [ ] Compra un dominio (ej: tiendaanime.com)
- [ ] En Railway Settings, añade el dominio
- [ ] Configura los registros DNS
- [ ] Verifica que funciona

---

## 🆘 TROUBLESHOOTING

Si algo no funciona:

### Error al desplegar
- [ ] Revisa "Deployments" → Logs
- [ ] Busca el error específico
- [ ] Consulta `RAILWAY_DEPLOYMENT_GUIDE.md`

### BD no conecta
- [ ] Verifica credenciales en Variables
- [ ] Asegúrate que la BD existe
- [ ] Prueba la conexión desde tu máquina local

### App carga pero da 404
- [ ] Revisa ALLOWED_HOSTS
- [ ] Verifica URLs en urls.py
- [ ] Consulta `sysApp/urls.py`

### Archivos estáticos no cargan
- [ ] Verifica WhiteNoise en settings.py
- [ ] Comprueba que STATIC_URL es correcto
- [ ] Intenta `python manage.py collectstatic`

---

## ✅ CONFIRMACIÓN FINAL

Antes de marcar como "completo", asegúrate:

- [ ] Tu app está en vivo en Railway
- [ ] Se puede acceder desde cualquier navegador
- [ ] La BD funciona correctamente
- [ ] Los archivos estáticos cargan
- [ ] No hay errores en los logs
- [ ] Todas las funciones principales funcionan

---

## 🎉 ¡LISTO!

```
╔════════════════════════════════════════════════════╗
║                                                    ║
║  ✅ Tu tienda anime está en vivo en la nube       ║
║                                                    ║
║  URL: https://tuapp.railway.app                   ║
║                                                    ║
║  MySQL: ✅ Funcionando                            ║
║  Django: ✅ Funcionando                           ║
║  Estáticos: ✅ Funcionando                        ║
║  Mercado Pago: ✅ Configurado                     ║
║                                                    ║
║  🎊 ¡Felicidades! Deployment completado 🎊       ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

---

**Completado el:** _______________  
**Por:** _______________  
**Notas:** _______________________________________________

---

**¿Necesitas ayuda?** Consulta `RAILWAY_DEPLOYMENT_GUIDE.md` para más detalles.
