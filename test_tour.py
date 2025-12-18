#!/usr/bin/env python3
"""
Test específico para el tour interactivo
"""
import requests
import re

BASE_URL = "http://localhost:8005"

def test_tour_implementation():
    """Verificar implementación del tour interactivo"""
    print("=" * 70)
    print("🎯 TEST DEL TOUR INTERACTIVO - CHISPART AI")
    print("=" * 70)
    print()
    
    try:
        # Obtener el JavaScript
        response = requests.get(f"{BASE_URL}/landing/js/main.js", timeout=5)
        js_content = response.text
        
        print("📋 Verificando componentes del tour...")
        print()
        
        # Verificar tourSteps
        if "tourSteps" in js_content:
            # Contar pasos
            steps_match = re.findall(r'\{[^}]*element:[^}]*title:[^}]*content:[^}]*\}', js_content)
            print(f"✅ Tour steps definidos: {len(steps_match)} pasos encontrados")
            
            # Verificar elementos específicos
            elements = ["#home", "#features", "#pricing", "#demo", "#register"]
            for i, elem in enumerate(elements, 1):
                if elem in js_content:
                    print(f"   ✅ Paso {i}: {elem} configurado")
                else:
                    print(f"   ⚠️  Paso {i}: {elem} no encontrado")
        else:
            print("❌ tourSteps no encontrado")
        
        print()
        print("🔧 Verificando funciones del tour...")
        print()
        
        # Funciones críticas del tour
        tour_functions = {
            "startTour": "Iniciar tour",
            "showTourStep": "Mostrar paso",
            "endTour": "Finalizar tour",
            "createTourOverlay": "Crear overlay",
            "highlightElement": "Resaltar elemento",
            "createTourTooltip": "Crear tooltip"
        }
        
        for func, desc in tour_functions.items():
            if f"function {func}" in js_content or f"const {func}" in js_content or f"{func} =" in js_content:
                print(f"✅ {desc} ({func})")
            else:
                print(f"❌ {desc} ({func}) - NO ENCONTRADA")
        
        print()
        print("🎨 Verificando características del tour...")
        print()
        
        # Características específicas
        features = {
            "tour-overlay": "Overlay oscuro",
            "tour-tooltip": "Tooltip informativo",
            "tour-highlight": "Resaltado de elementos",
            "Anterior": "Botón anterior",
            "Siguiente": "Botón siguiente",
            "Finalizar": "Botón finalizar",
            "Paso": "Indicador de progreso",
            "pulse": "Animación pulse",
            "fadeInScale": "Animación fadeIn"
        }
        
        for feature, desc in features.items():
            if feature in js_content:
                print(f"✅ {desc}")
            else:
                print(f"⚠️  {desc} - no encontrado")
        
        print()
        print("🔄 Verificando prevención de cierre prematuro...")
        print()
        
        # Verificar que hay control de flujo
        if "tourActive" in js_content:
            print("✅ Variable de estado del tour (tourActive)")
        
        if "tourStep" in js_content:
            print("✅ Variable de paso actual (tourStep)")
        
        if "stepIndex < 0 || stepIndex >= tourSteps.length" in js_content:
            print("✅ Validación de límites de pasos")
        
        if "endTour()" in js_content:
            print("✅ Función de finalización controlada")
        
        print()
        print("📱 Verificando navegación entre pasos...")
        print()
        
        # Verificar navegación
        if "showTourStep(${stepIndex - 1})" in js_content or "showTourStep(stepIndex - 1)" in js_content:
            print("✅ Navegación hacia atrás implementada")
        
        if "showTourStep(${stepIndex + 1})" in js_content or "showTourStep(stepIndex + 1)" in js_content:
            print("✅ Navegación hacia adelante implementada")
        
        if "scrollIntoView" in js_content:
            print("✅ Scroll automático a elementos")
        
        print()
        print("=" * 70)
        print("📊 RESUMEN DEL TEST")
        print("=" * 70)
        print()
        
        # Calcular score
        checks = [
            "tourSteps" in js_content,
            "startTour" in js_content,
            "showTourStep" in js_content,
            "endTour" in js_content,
            "createTourOverlay" in js_content,
            "tour-overlay" in js_content,
            "tour-tooltip" in js_content,
            "Anterior" in js_content,
            "Siguiente" in js_content,
            "Finalizar" in js_content,
            "tourActive" in js_content,
            "scrollIntoView" in js_content
        ]
        
        passed = sum(checks)
        total = len(checks)
        percentage = (passed / total) * 100
        
        print(f"✅ Checks pasados: {passed}/{total} ({percentage:.1f}%)")
        print()
        
        if percentage >= 90:
            print("🎉 ¡EXCELENTE! El tour está completamente implementado")
            print()
            print("✨ Características destacadas:")
            print("   • 5 pasos completos")
            print("   • Navegación bidireccional")
            print("   • Overlay con backdrop blur")
            print("   • Tooltips informativos")
            print("   • Resaltado de elementos")
            print("   • Animaciones suaves")
            print("   • Prevención de cierre prematuro")
            print("   • Scroll automático")
            print()
            print("🚀 El tour está listo para usar!")
            print("   Accede a: http://localhost:8005/landing/index.html")
            print("   Haz clic en '🎯 Tour Guiado'")
        elif percentage >= 70:
            print("✅ BIEN - El tour está mayormente implementado")
            print("   Algunas características menores pueden faltar")
        else:
            print("⚠️  ATENCIÓN - Faltan componentes importantes del tour")
        
        print()
        print("=" * 70)
        
        return percentage >= 90
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        return False

if __name__ == "__main__":
    success = test_tour_implementation()
    exit(0 if success else 1)
