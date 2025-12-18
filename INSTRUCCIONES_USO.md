# 📖 Instrucciones de Uso - Chispart AI Landing Page

## 🚀 Inicio Rápido

### 1. Iniciar el Servidor

```bash
cd /vercel/sandbox
python3 test_server.py
```

El servidor estará disponible en: **http://localhost:8005**

### 2. Acceder al Landing Page

Abre tu navegador y ve a:
```
http://localhost:8005/landing/index.html
```

---

## 🎯 Guía de Uso del Tour Interactivo

### Iniciar el Tour

**Opción 1: Botón en Hero Section**
1. En la página principal, busca el botón **"🎯 Tour Guiado"**
2. Haz clic en él
3. El tour comenzará automáticamente

**Opción 2: Desde la Consola del Navegador**
```javascript
startTour()
```

### Navegar por el Tour

El tour tiene **5 pasos**:

#### Paso 1: Bienvenida
- **Elemento:** Hero section
- **Contenido:** Introducción a Chispart AI
- **Acción:** Clic en "Siguiente →"

#### Paso 2: Características
- **Elemento:** Features section
- **Contenido:** Funcionalidades de la plataforma
- **Acción:** Clic en "← Anterior" o "Siguiente →"

#### Paso 3: Planes
- **Elemento:** Pricing section
- **Contenido:** Opciones de precios
- **Acción:** Clic en "← Anterior" o "Siguiente →"

#### Paso 4: Demo
- **Elemento:** Demo section
- **Contenido:** Prueba el asistente de IA
- **Acción:** Clic en "← Anterior" o "Siguiente →"

#### Paso 5: Registro
- **Elemento:** Register section
- **Contenido:** Comienza a usar la plataforma
- **Acción:** Clic en "¡Finalizar! ✨"

### Controles del Tour

- **Siguiente →**: Avanza al siguiente paso
- **← Anterior**: Retrocede al paso anterior
- **✕**: Cierra el tour en cualquier momento
- **ESC**: También cierra el tour (si está implementado)

### Características del Tour

✅ **Overlay oscuro** con backdrop blur  
✅ **Resaltado de elementos** con animación pulse  
✅ **Tooltips informativos** con diseño glassmorphism  
✅ **Scroll automático** a cada elemento  
✅ **Indicador de progreso** (Paso X de 5)  
✅ **Navegación bidireccional**  
✅ **Prevención de cierre accidental**  

---

## 💬 Guía de Uso del Demo Interactivo

### Acceder al Demo

1. Scroll hasta la sección **"Prueba Nuestro Demo"**
2. Verás un chat con un mensaje de bienvenida del asistente

### Interactuar con el Demo

Escribe preguntas en el campo de texto y presiona **Enter** o haz clic en **"Enviar"**.

### Preguntas Sugeridas

#### Saludos
```
hola
buenos días
hi
```

#### Información de Precios
```
cuanto cuesta
precios
planes
tarifas
```

#### Características
```
características
funciones
que hace
capacidades
```

#### Automatización
```
automatización
automatizar
procesos
```

#### Seguridad
```
seguridad
protección
datos
privacidad
```

#### Integraciones
```
integración
integrar
conectar
api
```

#### Soporte
```
soporte
ayuda
asistencia
```

#### Casos de Uso
```
casos
ejemplos
clientes
testimonios
```

### Respuestas del Demo

El demo tiene **10+ respuestas inteligentes** basadas en keywords. Si tu pregunta no coincide con ninguna keyword, recibirás una respuesta genérica invitándote a agendar una demo personalizada.

---

## 📝 Guía del Flujo Completo de Cliente

### Paso 1: Explorar el Landing

1. Lee la información en el hero section
2. Opcionalmente, inicia el tour guiado
3. Explora las características
4. Revisa los planes de precios

### Paso 2: Probar el Demo

1. Scroll a la sección de demo
2. Haz preguntas al asistente de IA
3. Experimenta con diferentes consultas

### Paso 3: Seleccionar un Plan

Haz clic en **"Seleccionar Plan"** en cualquiera de los 3 planes:

- **Starter**: $49/mes
- **Professional**: $149/mes (Más Popular)
- **Enterprise**: $499/mes

### Paso 4: Completar el Registro

Llena el formulario con:

- ✅ Nombre y Apellido
- ✅ Email corporativo
- ✅ Empresa
- ✅ Teléfono
- ✅ País
- ✅ Industria
- ✅ Tamaño de empresa
- ✅ Mensaje (opcional)
- ✅ Aceptar términos y condiciones

**Validaciones automáticas:**
- Email válido
- Teléfono válido
- Todos los campos requeridos

### Paso 5: Seleccionar Método de Pago

Elige entre:

- 💳 **PayPal**: Pago seguro con PayPal
- 📱 **Clip**: Pago con Clip

Haz clic en el método preferido para seleccionarlo.

### Paso 6: Procesar el Pago

1. Haz clic en **"Procesar Pago"**
2. Verás un spinner de procesamiento (3 segundos)
3. Aparecerá un mensaje de éxito con efecto confetti 🎊
4. Haz clic en **"Ir al Dashboard"** para continuar

---

## 🧪 Pruebas y Verificación

### Ejecutar Pruebas Automáticas

```bash
# Pruebas generales
python3 test_landing.py

# Pruebas específicas del tour
python3 test_tour.py

# Ver información del proyecto
./info_landing.sh
```

### Verificar Manualmente

1. **Tour Interactivo**
   - Iniciar tour
   - Navegar por todos los pasos
   - Verificar que no se cierra prematuramente
   - Probar botones Anterior/Siguiente
   - Cerrar con botón X

2. **Demo**
   - Escribir varias preguntas
   - Verificar respuestas apropiadas
   - Probar con Enter y botón Enviar

3. **Registro**
   - Intentar enviar con campos vacíos
   - Intentar con email inválido
   - Completar correctamente
   - Verificar transición a pago

4. **Pago**
   - Seleccionar método de pago
   - Procesar pago
   - Verificar mensaje de éxito
   - Verificar efecto confetti

---

## 🔧 Solución de Problemas

### El servidor no inicia

```bash
# Verificar que el puerto 8005 esté libre
lsof -i :8005

# Si está ocupado, matar el proceso
kill -9 $(lsof -t -i:8005)

# Reiniciar servidor
python3 test_server.py
```

### El JavaScript no carga

```bash
# Verificar que el archivo existe
ls -lh /vercel/sandbox/landing/js/main.js

# Verificar que se sirve correctamente
curl http://localhost:8005/landing/js/main.js | head -20
```

### El tour no aparece

1. Abre la consola del navegador (F12)
2. Busca errores en JavaScript
3. Verifica que `startTour()` esté definido:
   ```javascript
   typeof startTour
   // Debe retornar: "function"
   ```

### El demo no responde

1. Verifica que el input tenga el ID correcto: `demoInput`
2. Verifica que el contenedor tenga el ID: `demoChat`
3. Revisa la consola del navegador por errores

---

## 📚 Documentación Adicional

- **Verificación Completa**: `VERIFICACION_LANDING.md`
- **Resumen de Implementación**: `RESUMEN_IMPLEMENTACION.md`
- **Código JavaScript**: `landing/js/main.js`

---

## 🎨 Personalización

### Cambiar Colores del Tour

Edita en `landing/js/main.js`:

```javascript
// Busca estas líneas en createTourTooltip()
border: 1px solid rgba(244, 114, 182, 0.3);  // Color del borde
color: #f472b6;  // Color del título
```

### Agregar Más Pasos al Tour

Edita el array `tourSteps` en `landing/js/main.js`:

```javascript
const tourSteps = [
    // ... pasos existentes
    {
        element: '#nuevo-elemento',
        title: 'Nuevo Paso',
        content: 'Descripción del nuevo paso',
        position: 'top'
    }
];
```

### Agregar Más Respuestas al Demo

Edita el array `demoResponses` en `landing/js/main.js`:

```javascript
const demoResponses = [
    // ... respuestas existentes
    {
        keywords: ['nueva', 'keyword'],
        response: 'Nueva respuesta personalizada'
    }
];
```

---

## 🌐 URLs de Referencia

- **Landing Page**: http://localhost:8005/landing/index.html
- **Frontend Principal**: http://localhost:8005/frontend/index.html
- **JavaScript**: http://localhost:8005/landing/js/main.js

---

## ✅ Checklist de Verificación

Antes de considerar el landing completo, verifica:

- [ ] Servidor corriendo en puerto 8005
- [ ] Landing page carga sin errores
- [ ] JavaScript carga correctamente
- [ ] Tour inicia y muestra 5 pasos
- [ ] Navegación del tour funciona
- [ ] Tour se puede cerrar
- [ ] Demo responde a preguntas
- [ ] Selección de plan funciona
- [ ] Formulario valida correctamente
- [ ] Proceso de pago se completa
- [ ] Mensaje de éxito aparece
- [ ] Confetti se muestra
- [ ] Notificaciones funcionan

---

## 🎉 ¡Listo para Usar!

El landing page de Chispart AI está completamente funcional y listo para recibir clientes.

**¿Necesitas ayuda?**
- Revisa la documentación en `VERIFICACION_LANDING.md`
- Ejecuta las pruebas con `python3 test_landing.py`
- Consulta el código en `landing/js/main.js`

---

**Última actualización:** 18 de diciembre de 2025  
**Versión:** 1.0.0  
**Estado:** ✅ Completado y Verificado
