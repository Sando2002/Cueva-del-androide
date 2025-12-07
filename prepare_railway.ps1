# Script de preparación para Railway (Windows)
# Ejecuta con: powershell -ExecutionPolicy Bypass -File prepare_railway.ps1

Write-Host "🚀 Preparando aplicación para Railway..." -ForegroundColor Green
Write-Host ""

# 1. Instalar dependencias
Write-Host "1️⃣ Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✅ Dependencias instaladas" -ForegroundColor Green
Write-Host ""

# 2. Recolectar archivos estáticos
Write-Host "2️⃣ Recolectando archivos estáticos..." -ForegroundColor Yellow
python manage.py collectstatic --noinput
Write-Host "✅ Archivos estáticos recolectados" -ForegroundColor Green
Write-Host ""

# 3. Verificar migraciones
Write-Host "3️⃣ Verificando migraciones..." -ForegroundColor Yellow
python manage.py migrate --plan
Write-Host "✅ Migraciones verificadas" -ForegroundColor Green
Write-Host ""

# 4. Crear requirements.txt limpio
Write-Host "4️⃣ Actualizando requirements.txt..." -ForegroundColor Yellow
pip freeze > requirements.txt
Write-Host "✅ requirements.txt actualizado" -ForegroundColor Green
Write-Host ""

# 5. Preparar Git
Write-Host "5️⃣ Preparando Git..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "  Inicializando Git..."
    git init
}
git add .
git status
Write-Host ""

Write-Host "✅ ¡Listo para Railway!" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Sube los cambios a GitHub:"
Write-Host "   git commit -m 'Setup para Railway'"
Write-Host "   git push -u origin main"
Write-Host ""
Write-Host "2. Ve a https://railway.app y sigue los pasos de la guía"
Write-Host ""
