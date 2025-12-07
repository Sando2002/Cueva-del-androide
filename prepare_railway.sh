#!/bin/bash
# Script de preparación para Railway

echo "🚀 Preparando aplicación para Railway..."
echo ""

# 1. Instalar dependencias
echo "1️⃣ Instalando dependencias..."
pip install -r requirements.txt
echo "✅ Dependencias instaladas"
echo ""

# 2. Recolectar archivos estáticos
echo "2️⃣ Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
echo "✅ Archivos estáticos recolectados"
echo ""

# 3. Verificar migraciones
echo "3️⃣ Verificando migraciones..."
python manage.py migrate --plan
echo "✅ Migraciones verificadas"
echo ""

# 4. Crear requirements.txt limpio
echo "4️⃣ Actualizando requirements.txt..."
pip freeze > requirements.txt
echo "✅ requirements.txt actualizado"
echo ""

# 5. Preparar Git
echo "5️⃣ Preparando Git..."
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "  Inicializando Git..."
    git init
fi
git add .
git status
echo ""

echo "✅ ¡Listo para Railway!"
echo ""
echo "Próximos pasos:"
echo "1. Sube los cambios a GitHub:"
echo "   git commit -m 'Setup para Railway'"
echo "   git push -u origin main"
echo ""
echo "2. Ve a https://railway.app y sigue los pasos de la guía"
echo ""
