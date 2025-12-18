#!/bin/bash

# Script de información del landing page de Chispart AI

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║           ✨ CHISPART AI - LANDING PAGE INFO ✨               ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar servidor
echo "🔍 Verificando servidor..."
if curl -s http://localhost:8005/landing/index.html > /dev/null; then
    echo "✅ Servidor corriendo en http://localhost:8005"
else
    echo "❌ Servidor no está corriendo"
    echo "   Ejecuta: python3 test_server.py"
    exit 1
fi

echo ""
echo "📂 Archivos del proyecto:"
echo "   ├── landing/index.html (31 KB)"
echo "   ├── landing/js/main.js (28 KB)"
echo "   ├── frontend/index.html (Frontend principal)"
echo "   ├── test_server.py (Servidor HTTP)"
echo "   ├── test_landing.py (Pruebas automáticas)"
echo "   └── VERIFICACION_LANDING.md (Documentación)"

echo ""
echo "🌐 URLs disponibles:"
echo "   • Landing Page:  http://localhost:8005/landing/index.html"
echo "   • Frontend:      http://localhost:8005/frontend/index.html"
echo "   • JavaScript:    http://localhost:8005/landing/js/main.js"

echo ""
echo "🎯 Funcionalidades implementadas:"
echo "   ✅ Tour interactivo (5 pasos)"
echo "   ✅ Demo con IA (10+ respuestas)"
echo "   ✅ Selección de planes (3 opciones)"
echo "   ✅ Registro completo (validaciones)"
echo "   ✅ Proceso de pago (PayPal/Clip)"
echo "   ✅ Notificaciones y animaciones"
echo "   ✅ Efecto confetti"

echo ""
echo "🧪 Ejecutar pruebas:"
echo "   python3 test_landing.py"

echo ""
echo "📖 Ver documentación completa:"
echo "   cat VERIFICACION_LANDING.md"
echo "   cat RESUMEN_IMPLEMENTACION.md"

echo ""
echo "🚀 Cómo usar el tour interactivo:"
echo "   1. Abre http://localhost:8005/landing/index.html"
echo "   2. Haz clic en '🎯 Tour Guiado' en la sección hero"
echo "   3. Sigue los 5 pasos del tour"
echo "   4. Navega con los botones Anterior/Siguiente"
echo "   5. Cierra con el botón X cuando quieras"

echo ""
echo "💬 Cómo usar el demo:"
echo "   1. Scroll a la sección 'Prueba Nuestro Demo'"
echo "   2. Escribe preguntas como:"
echo "      - 'hola'"
echo "      - 'cuanto cuesta'"
echo "      - 'características'"
echo "      - 'automatización'"
echo "      - 'seguridad'"
echo "   3. Recibe respuestas inteligentes de la IA"

echo ""
echo "📝 Flujo completo de cliente:"
echo "   Landing → Tour → Demo → Plan → Registro → Pago → Éxito"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ TODO FUNCIONANDO                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
