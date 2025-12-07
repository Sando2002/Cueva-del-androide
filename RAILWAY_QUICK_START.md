# 🎯 DEPLOYMENT EN RAILWAY - CHECKLIST RÁPIDO

Tu proyecto Django está **100% listo** para Railway. 

## ⚡ AHORA MISMO:

### 1️⃣ En tu terminal local:
```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File prepare_railway.ps1

# O manualmente:
pip freeze > requirements.txt
python manage.py collectstatic --noinput
git add .
git commit -m "Setup para Railway"
```

### 2️⃣ Sube a GitHub:

**Primero crea un nuevo repositorio:**
1. Ve a https://github.com/new
2. Nombra el repo: `tiendaanime` (o el nombre que prefieras)
3. NO marques "Add a README" (tienes código local)
4. Click "Create repository"

**Luego en tu terminal:**
```bash
git branch -M main
git remote add origin https://github.com/TU_USUARIO/tiendaanime.git
git push -u origin main
```
⚠️ Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub

### 3️⃣ En https://railway.app:

**Paso A - Base de datos:**
- New Project → Database → MySQL
- Espera 2-3 minutos
- Copia las credenciales (Host, User, Password, Database Name)
- Importa `tiendaanime.sql` desde phpMyAdmin

**Paso B - Aplicación:**
- New Project → GitHub Repo → tiendaanime
- Verifica que los archivos estén ahí

**Paso C - Variables de entorno:**
En tu proyecto Django → Variables, añade:

```
DEBUG=False
SECRET_KEY=tu-clave-super-segura-aqui
DB_NAME=mysql_database_name
DB_USER=mysql_user
DB_PASSWORD=mysql_password
DB_HOST=mysql_host
DB_PORT=3306
ALLOWED_HOSTS=tuapp.railway.app
CSRF_TRUSTED_ORIGINS=https://tuapp.railway.app
MERCADOPAGO_PUBLIC_KEY=tu-public-key
MERCADOPAGO_ACCESS_TOKEN=tu-access-token
```

### 4️⃣ ¡Deploy!
- El servidor se iniciará automáticamente
- Verifica en Deployments (debe estar en verde)
- Haz click en la URL

---

## 📦 ARCHIVOS CREADOS/MODIFICADOS:

| Archivo | Propósito |
|---------|-----------|
| `Procfile` | Instrucciones de Railway |
| `runtime.txt` | Versión Python |
| `requirements.txt` | Dependencias (actualizado) |
| `settings.py` | Configurado para variables de entorno |
| `.env` | Variables locales |
| `.env.example` | Plantilla |
| `.gitignore` | Archivos a ignorar |
| `prepare_railway.ps1` | Script de preparación |

---

## 🆘 SI HAY PROBLEMAS:

**Error: "Access denied for MySQL"**
- ✅ Las credenciales son correctas en Variables?
- ✅ La BD existe en Railway?

**Error: "ModuleNotFoundError"**
- ✅ Ejecutaste `pip freeze > requirements.txt`?

**Archivos estáticos no cargan**
- ✅ WhiteNoise está configurado en settings.py

**Ver logs de errores:**
- En Railway → Deployments → Click en deployment → Logs

---

## 📚 DOCUMENTACIÓN:

- `RAILWAY_DEPLOYMENT_GUIDE.md` - Guía completa (paso a paso)
- `DEPLOYMENT_RAILWAY.md` - Guía alternativa
- https://docs.railway.app - Documentación oficial

---

## ✅ VERIFICACIÓN FINAL:

Antes de hacer push, asegúrate:
- [ ] `requirements.txt` actualizado
- [ ] `Procfile` existe
- [ ] `.env` NO está en .gitignore (solo variables locales)
- [ ] `settings.py` usa `config()` para variables
- [ ] Git está inicializado
- [ ] GitHub repo creado

---

## 🎉 ¡LISTO!

**Tu aplicación estará en vivo en minutos en Railway con MySQL gratuito.**

Cualquier duda, revisa `RAILWAY_DEPLOYMENT_GUIDE.md` para más detalles.
