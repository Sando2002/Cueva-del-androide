# 🚀 GUÍA DE DEPLOYMENT EN RAILWAY CON MYSQL

## Pasos para desplegar en Railway:

### 1. Preparación local
```bash
# Instala las dependencias nuevas
pip install -r requirements.txt

# Ejecuta las migraciones localmente (opcional pero recomendado)
python manage.py migrate
```

### 2. Crea un repositorio Git (si aún no lo tienes)
```bash
git init
git add .
git commit -m "Initial commit"
```

### 3. Sube a GitHub (necesario para Railway)
- Ve a https://github.com/new
- Crea un nuevo repositorio (ej: "tiendaanime")
- Sigue las instrucciones para pushear tu código local
```bash
git branch -M main
git remote add origin https://github.com/TU_USUARIO/tiendaanime.git
git push -u origin main
```

### 4. Configura Railway

#### 4.1 Crea la base de datos MySQL
- Ve a https://railway.app
- Haz login/signup
- Click en "New Project"
- Selecciona "Database" → "MySQL"
- Espera a que se cree (2-3 minutos)
- En la sección "MySQL", copia las credenciales:
  - Host
  - Port
  - Username
  - Password
  - Database

#### 4.2 Importa tu base de datos actual
Tienes varias opciones:
- **Opción 1 (Recomendado):** Usa phpMyAdmin
  - En Railway, abre la consola de MySQL
  - Importa tu archivo `tiendaanime.sql`
  
- **Opción 2:** Usa mysql-cli
```bash
mysql -h HOST -u USER -p DATABASE < tiendaanime.sql
```

#### 4.3 Deploya la aplicación Django
- En Railway, click "New Project"
- Selecciona "GitHub Repo"
- Autentica con tu cuenta de GitHub
- Selecciona el repositorio "tiendaanime"
- Railway detectará que es una app Python

#### 4.4 Configura las variables de entorno
En Railway, ve a la pestaña "Variables":
```
DEBUG=False
SECRET_KEY=genera-una-nueva-aqui-es-importante
DB_ENGINE=django.db.backends.mysql
DB_NAME=tu_nombre_bd
DB_USER=usuario_mysql_railway
DB_PASSWORD=contraseña_mysql_railway
DB_HOST=host_mysql_railway
DB_PORT=3306
ALLOWED_HOSTS=tu-app-railway.railway.app
CSRF_TRUSTED_ORIGINS=https://tu-app-railway.railway.app
MERCADOPAGO_PUBLIC_KEY=tu-public-key
MERCADOPAGO_ACCESS_TOKEN=tu-access-token
```

**Para generar SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### 4.5 Conecta la base de datos MySQL
En Railway:
- En tu proyecto Django, ve a "Plugins"
- Click "Add Plugin"
- Selecciona "MySQL" (si no la has añadido)
- Railway vinculará automáticamente las variables de entorno

### 5. Deploy automático
- Railway automáticamente deployará cada vez que hagas push a `main`
- Puedes ver el estado en "Deployments"

### 6. Recolectar archivos estáticos
Esto se hace automáticamente gracias a `Procfile` con `release: python manage.py migrate`

### 7. Verificar la aplicación
- En Railway, copia la URL de tu app (ej: `https://tu-app.railway.app`)
- Accede desde el navegador
- Si hay errores, revisa los logs en Railway

---

## 📋 Checklist Pre-Deploy

- [ ] Git configurado y código en GitHub
- [ ] `requirements.txt` actualizado (incluye gunicorn, whitenoise, python-decouple)
- [ ] `Procfile` presente
- [ ] `runtime.txt` presente
- [ ] `settings.py` configurado con variables de entorno
- [ ] Base de datos MySQL creada en Railway
- [ ] Datos importados a la BD
- [ ] Variables de entorno configuradas en Railway
- [ ] Primer deploy exitoso

---

## 🆘 Problemas comunes

**"ModuleNotFoundError: No module named 'django'"**
- Los paquetes en `requirements.txt` pueden no ser los correctos para Railway
- Usa `pip freeze > requirements.txt` para generar una lista exacta

**"Access denied for user 'root'@'...'"`
- Verifica las credenciales de MySQL en las variables de entorno
- Asegúrate de que la BD existe

**"collectstatic failed"`
- Ejecuta localmente: `python manage.py collectstatic --noinput`
- Verifica que `STATIC_ROOT` esté configurado

**Archivos estáticos no cargan**
- WhiteNoise está configurado en settings.py
- Verifica que `STATICFILES_STORAGE` está correcto

---

## 📚 Recursos útiles

- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
- MySQL en Railway: https://railway.app/docs/guides/mysql

¡Listo! Tu app Django estará en producción en Railway con MySQL. 🎉
