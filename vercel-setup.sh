#!/bin/bash
# Script de configuración rápida para Vercel deployment

set -e

echo "🚀 Configuración de Vercel para Blackbox Hybrid Tool"
echo "=================================================="
echo ""

# Verificar si Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "⚠️  Vercel CLI no está instalado."
    echo "Instalando Vercel CLI..."
    npm install -g vercel
    echo "✅ Vercel CLI instalado"
else
    echo "✅ Vercel CLI ya está instalado"
fi

echo ""

# Verificar archivos necesarios
echo "📋 Verificando archivos de configuración..."

files=(
    "vercel.json"
    "api/index.py"
    "requirements.txt"
    ".vercelignore"
    ".env.example"
)

all_files_exist=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - FALTA"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo ""
    echo "❌ Faltan archivos necesarios. Por favor, ejecuta el script de setup primero."
    exit 1
fi

echo ""
echo "✅ Todos los archivos de configuración están presentes"
echo ""

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "⚠️  No se encontró archivo .env"
    echo "Creando .env desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado"
    echo ""
    echo "⚠️  IMPORTANTE: Edita .env y agrega tu BLACKBOX_API_KEY"
    echo ""
    read -p "¿Quieres editar .env ahora? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
else
    echo "✅ Archivo .env ya existe"
fi

echo ""
echo "🔐 Configuración de Variables de Entorno en Vercel"
echo "=================================================="
echo ""
echo "Necesitas configurar las siguientes variables en Vercel:"
echo ""
echo "  1. BLACKBOX_API_KEY (requerido)"
echo "  2. CONFIG_FILE=config/models.json"
echo "  3. WRITE_ROOT=/tmp"
echo "  4. AUTO_SNAPSHOT=false"
echo ""
read -p "¿Quieres configurar las variables ahora? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Configurando variables de entorno..."
    
    # BLACKBOX_API_KEY
    echo ""
    read -p "Ingresa tu BLACKBOX_API_KEY: " api_key
    if [ ! -z "$api_key" ]; then
        echo "$api_key" | vercel env add BLACKBOX_API_KEY production
        echo "✅ BLACKBOX_API_KEY configurada"
    fi
    
    # CONFIG_FILE
    echo "config/models.json" | vercel env add CONFIG_FILE production
    echo "✅ CONFIG_FILE configurada"
    
    # WRITE_ROOT
    echo "/tmp" | vercel env add WRITE_ROOT production
    echo "✅ WRITE_ROOT configurada"
    
    # AUTO_SNAPSHOT
    echo "false" | vercel env add AUTO_SNAPSHOT production
    echo "✅ AUTO_SNAPSHOT configurada"
    
    echo ""
    echo "✅ Variables de entorno configuradas"
fi

echo ""
echo "🧪 Prueba Local (Opcional)"
echo "=========================="
echo ""
read -p "¿Quieres probar la aplicación localmente con 'vercel dev'? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Iniciando servidor de desarrollo..."
    echo "La aplicación estará disponible en http://localhost:3000"
    echo ""
    echo "Presiona Ctrl+C para detener el servidor"
    echo ""
    vercel dev
fi

echo ""
echo "🚀 Deployment a Producción"
echo "=========================="
echo ""
read -p "¿Quieres desplegar a producción ahora? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Desplegando a producción..."
    vercel --prod
    echo ""
    echo "✅ Deployment completado!"
else
    echo ""
    echo "Para desplegar más tarde, ejecuta:"
    echo "  vercel --prod"
fi

echo ""
echo "✨ Configuración completada!"
echo ""
echo "📚 Recursos útiles:"
echo "  - Guía completa: VERCEL_DEPLOYMENT.md"
echo "  - Dashboard: https://vercel.com/dashboard"
echo "  - Logs: vercel logs"
echo ""
echo "🎉 ¡Listo para usar!"
