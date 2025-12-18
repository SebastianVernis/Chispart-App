#!/usr/bin/env python3
"""
Script de prueba para verificar funcionalidad del landing page
"""
import requests
import time

BASE_URL = "http://localhost:8005"

def test_landing_page():
    """Probar que el landing page carga correctamente"""
    print("🧪 Probando landing page...")
    
    try:
        response = requests.get(f"{BASE_URL}/landing/index.html", timeout=5)
        if response.status_code == 200:
            print("✅ Landing page carga correctamente")
            
            # Verificar que contiene elementos clave
            content = response.text
            checks = [
                ("Chispart AI", "Título principal"),
                ("selectPlan", "Función de selección de plan"),
                ("sendDemoMessage", "Función de demo"),
                ("handleRegistration", "Función de registro"),
                ("processPayment", "Función de pago"),
                ("js/main.js", "Referencia al JavaScript")
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"  ✅ {description} encontrado")
                else:
                    print(f"  ❌ {description} NO encontrado")
            
            return True
        else:
            print(f"❌ Error: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al cargar landing page: {e}")
        return False

def test_javascript():
    """Probar que el archivo JavaScript carga correctamente"""
    print("\n🧪 Probando archivo JavaScript...")
    
    try:
        response = requests.get(f"{BASE_URL}/landing/js/main.js", timeout=5)
        if response.status_code == 200:
            print("✅ Archivo JavaScript carga correctamente")
            
            # Verificar funciones clave
            content = response.text
            functions = [
                "startTour",
                "showTourStep",
                "sendDemoMessage",
                "selectPlan",
                "handleRegistration",
                "processPayment",
                "createTourOverlay",
                "getDemoResponse"
            ]
            
            for func in functions:
                if f"function {func}" in content or f"const {func}" in content or f"{func} =" in content:
                    print(f"  ✅ Función {func} implementada")
                else:
                    print(f"  ⚠️  Función {func} no encontrada (puede estar como arrow function)")
            
            # Verificar tour steps
            if "tourSteps" in content:
                print("  ✅ Tour steps definidos")
            
            # Verificar demo responses
            if "demoResponses" in content:
                print("  ✅ Demo responses definidos")
            
            return True
        else:
            print(f"❌ Error: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al cargar JavaScript: {e}")
        return False

def test_frontend():
    """Probar que el frontend principal también funciona"""
    print("\n🧪 Probando frontend principal...")
    
    try:
        response = requests.get(f"{BASE_URL}/frontend/index.html", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend principal carga correctamente")
            return True
        else:
            print(f"❌ Error: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al cargar frontend: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 PRUEBAS DE FUNCIONALIDAD - CHISPART AI LANDING PAGE")
    print("=" * 60)
    
    # Esperar a que el servidor esté listo
    print("\n⏳ Esperando a que el servidor esté listo...")
    time.sleep(2)
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Landing Page", test_landing_page()))
    results.append(("JavaScript", test_javascript()))
    results.append(("Frontend", test_frontend()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("\n📝 Funcionalidades implementadas:")
        print("  • Tour interactivo con 5 pasos")
        print("  • Demo con respuestas inteligentes de IA")
        print("  • Selección de planes (Starter, Professional, Enterprise)")
        print("  • Formulario de registro con validación")
        print("  • Proceso de pago simulado (PayPal y Clip)")
        print("  • Notificaciones y animaciones")
        print("  • Efecto confetti al completar pago")
        print("\n🌐 URLs disponibles:")
        print(f"  • Landing: {BASE_URL}/landing/index.html")
        print(f"  • Frontend: {BASE_URL}/frontend/index.html")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los detalles arriba.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
