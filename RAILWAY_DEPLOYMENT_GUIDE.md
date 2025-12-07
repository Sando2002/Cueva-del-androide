# 🚀 GUÍA COMPLETADE DEPLOYMENT EN RAILWAY + MYSQL

Tu aplicación Django ya está preparada para Railway. Aquí están los pasos finales:

## ✅ Lo que ya hemos hecho:

1. ✅ Actualizado `settings.py` para usar variables de entorno
2. ✅ Añadido `Procfile` para Railway
3. ✅ Configurado `WhiteNoise` para archivos estáticos
4. ✅ Instalado `python-decouple` para gestionar variables
5. ✅ Creado archivos `.env` y `.env.example`
6. ✅ Verificado que funciona localmente

---

## 📋 PASOS PARA DESPLEGAR EN RAILWAY

### Paso 1: Prepara tu código en GitHub

```bash
# En tu proyecto local:
git init
git add .
git commit -m "Setup para Railway deployment"

# Crea un repo en https://github.com/new (ej: tiendaanime)
# Luego:
git branch -M main
git remote add origin https://github.com/TU_USUARIO/tiendaanime.git
git push -u origin main
```

### Paso 2: Configura Railway

#### 2.1 Crea la base de datos MySQL
1. Ve a https://railway.app
2. Haz login (puedes usar GitHub)
3. Click "New Project" → "Database" → "MySQL"
4. Espera 2-3 minutos a que se cree
5. **Copia estas credenciales** (las necesitarás después):
   - **Database Host**
   - **Database Port** 
   - **Database User**
   - **Database Password**
   - **Database Name**

#### 2.2 Importa tu base de datos actual
Opción A (phpMyAdmin - más fácil):
- En Railway, abre la consola de MySQL
- Haz click en "MySQL" → "Connect"
- Importa tu archivo `tiendaanime.sql`

Opción B (comando):
```bash
mysql -h HOST_RAILWAY -u USER_RAILWAY -p DATABASE_NAME < tiendaanime.sql
```

#### 2.3 Deploya tu app Django
1. En Railway, click "New Project"
2. Selecciona "GitHub Repo"
3. Autentica tu cuenta GitHub
4. Selecciona el repo `tiendaanime`
5. Railway detectará automáticamente que es una app Python

#### 2.4 Configura Variables de Entorno
En Railway, en tu proyecto Django, ve a "Variables":

```
DEBUG=False
SECRET_KEY=EsTu-ClaveSuperSeguraAquiGeneraPorFavor123456789!
DB_ENGINE=django.db.backends.mysql
DB_NAME=NombreDelaDatabaseDeRailway
DB_USER=UsuarioRailway
DB_PASSWORD=ContraseñaRailway
DB_HOST=HostRailway
DB_PORT=3306
ALLOWED_HOSTS=tuapp.railway.app
CSRF_TRUSTED_ORIGINS=https://tuapp.railway.app
MERCADOPAGO_PUBLIC_KEY=APP_USR-93bc5673-82fd-4165-94b4-194c7160b4ff
MERCADOPAGO_ACCESS_TOKEN=APP_USR-7207881648330267-111519-a66d30ce1599365c02d3c34ef1619608-2992706644
```

**IMPORTANTE: Para generar SECRET_KEY seguro:**
```bash
# Ejecuta esto en tu terminal local:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado en las variables de Railway.

#### 2.5 Conecta la base de datos (Automático)
Railway vinculará automáticamente el MySQL. Si no lo hace:
- Abre tu proyecto Django en Railway
- Ve a "Plugins"
- Añade el MySQL que creaste antes

### Paso 3: Deploy automático

Una vez que hayas pusheado a GitHub:
```bash
git add .
git commit -m "Deploy en Railway"
git push origin main
```

Railway automáticamente:
1. Detectará los cambios
2. Instalará dependencias (`requirements.txt`)
3. Ejecutará migraciones (`Procfile`)
4. Recolectará archivos estáticos
5. Iniciará el servidor

---

## 🔍 VERIFICAR EL DEPLOYMENT

1. En Railway, ve a tu proyecto Django
2. En "Deployments" verás el estado
3. Cuando esté verde (SUCCESS), haz click en la URL
4. ¡Tu app estará en vivo!

Si hay problemas, ve a "Logs" para ver errores.

---

## ⚠️ PROBLEMAS COMUNES Y SOLUCIONES

### "ModuleNotFoundError"
- Asegúrate que `requirements.txt` tiene TODAS las dependencias
- En tu terminal local: `pip freeze > requirements.txt`

### "Access denied for MySQL"
- Verifica que las credenciales son correctas en Variables
- Comprueba que la BD existe en Railway

### "collectstatic failed"
- Esto no suele pasar porque WhiteNoise lo maneja
- Si pasa, añade a Variables: `STATIC_ROOT=/app/staticfiles`

### "Static files not loading"
- Verifica que los archivos están en `sysApp/static/`
- Railway debería servirlos automáticamente

### "Page not found (404)"
- Revisa que `ALLOWED_HOSTS` incluye tu dominio de Railway
- En Variables, actualiza a: `ALLOWED_HOSTS=tuapp.railway.app`

---

## 📱 ¿Y AHORA QUÉ?

Tu aplicación estará en vivo en una URL como:
```
https://tiendaanime.railway.app
```

### Próximos pasos:
- [ ] Configurar un dominio personalizado (opcional, en Railroad Settings)
- [ ] Monitorear los logs regularmente
- [ ] Hacer backups de la BD MySQL
- [ ] Configurar emails (si tu app los envía)
- [ ] Optimizar la base de datos para producción

---

## 🆘 SOPORTE

- **Railway Docs:** https://docs.railway.app
- **Django Docs:** https://docs.djangoproject.com/en/5.2/
- **MySQL:** https://docs.railway.app/guides/mysql

---

## 📝 RESUMEN DE ARCHIVOS MODIFICADOS

✅ `requirements.txt` - Añadidas dependencias para producción
✅ `settings.py` - Configurado para variables de entorno
✅ `Procfile` - Instrucciones para Railway
✅ `runtime.txt` - Versión de Python
✅ `.env` - Variables locales (NO subir a GitHub)
✅ `.env.example` - Plantilla para variables
✅ `.gitignore` - Archivos a ignorar en Git

---

## ¡Listo! 🎉

Tu aplicación Django + MySQL está lista para Railway. Sigue los pasos y en minutos tendrás tu tienda online en producción.

¿Necesitas ayuda en algún paso? Pregunta.
