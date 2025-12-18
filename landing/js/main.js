// ============================================
// CHISPART AI - Landing Page JavaScript
// ============================================

// Estado global de la aplicación
const appState = {
    selectedPlan: null,
    selectedPrice: null,
    selectedPaymentMethod: null,
    tourActive: false,
    tourStep: 0,
    demoMessages: []
};

// ============================================
// TOUR INTERACTIVO
// ============================================

const tourSteps = [
    {
        element: '#home',
        title: '¡Bienvenido a Chispart AI! 🎉',
        content: 'Descubre cómo nuestra plataforma de IA multiagente puede transformar tu negocio. Te guiaremos paso a paso.',
        position: 'center'
    },
    {
        element: '#features',
        title: 'Características Poderosas 🚀',
        content: 'Explora nuestras funcionalidades: agentes inteligentes, automatización total, análisis avanzado y más.',
        position: 'top'
    },
    {
        element: '#pricing',
        title: 'Planes Flexibles 💎',
        content: 'Elige el plan perfecto para tu negocio. Desde startups hasta empresas, tenemos opciones para todos.',
        position: 'top'
    },
    {
        element: '#demo',
        title: 'Prueba Nuestro Demo 🤖',
        content: 'Interactúa con nuestro asistente de IA. Haz preguntas y descubre cómo puede ayudarte.',
        position: 'top'
    },
    {
        element: '#register',
        title: 'Comienza Ahora 🎯',
        content: 'Cuando estés listo, completa el registro y únete a miles de empresas que ya usan Chispart AI.',
        position: 'top'
    }
];

// Iniciar tour interactivo
function startTour() {
    if (appState.tourActive) return;
    
    appState.tourActive = true;
    appState.tourStep = 0;
    
    // Crear overlay
    createTourOverlay();
    
    // Mostrar primer paso
    showTourStep(0);
}

// Crear overlay del tour
function createTourOverlay() {
    // Eliminar overlay existente si hay
    const existingOverlay = document.getElementById('tour-overlay');
    if (existingOverlay) {
        existingOverlay.remove();
    }
    
    const overlay = document.createElement('div');
    overlay.id = 'tour-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: 9998;
        backdrop-filter: blur(3px);
    `;
    
    document.body.appendChild(overlay);
}

// Mostrar paso del tour
function showTourStep(stepIndex) {
    if (stepIndex < 0 || stepIndex >= tourSteps.length) {
        endTour();
        return;
    }
    
    appState.tourStep = stepIndex;
    const step = tourSteps[stepIndex];
    
    // Eliminar tooltip anterior
    const existingTooltip = document.getElementById('tour-tooltip');
    if (existingTooltip) {
        existingTooltip.remove();
    }
    
    // Scroll al elemento
    const element = document.querySelector(step.element);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Esperar a que termine el scroll
        setTimeout(() => {
            // Resaltar elemento
            highlightElement(element);
            
            // Crear tooltip
            createTourTooltip(step, stepIndex);
        }, 500);
    }
}

// Resaltar elemento
function highlightElement(element) {
    // Eliminar highlight anterior
    const existingHighlight = document.getElementById('tour-highlight');
    if (existingHighlight) {
        existingHighlight.remove();
    }
    
    const rect = element.getBoundingClientRect();
    const highlight = document.createElement('div');
    highlight.id = 'tour-highlight';
    highlight.style.cssText = `
        position: fixed;
        top: ${rect.top - 10}px;
        left: ${rect.left - 10}px;
        width: ${rect.width + 20}px;
        height: ${rect.height + 20}px;
        border: 3px solid #f472b6;
        border-radius: 12px;
        z-index: 9999;
        pointer-events: none;
        box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5);
        animation: pulse 2s infinite;
    `;
    
    document.body.appendChild(highlight);
}

// Crear tooltip del tour
function createTourTooltip(step, stepIndex) {
    const tooltip = document.createElement('div');
    tooltip.id = 'tour-tooltip';
    tooltip.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.98), rgba(40, 40, 40, 0.98));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(244, 114, 182, 0.3);
        border-radius: 16px;
        padding: 30px;
        max-width: 500px;
        z-index: 10000;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        animation: fadeInScale 0.3s ease-out;
    `;
    
    tooltip.innerHTML = `
        <div style="margin-bottom: 20px;">
            <div style="font-size: 24px; font-weight: bold; color: #f472b6; margin-bottom: 10px;">
                ${step.title}
            </div>
            <div style="color: #a0a0a0; line-height: 1.6; font-size: 16px;">
                ${step.content}
            </div>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 25px;">
            <div style="color: #67e8f9; font-size: 14px; font-weight: 600;">
                Paso ${stepIndex + 1} de ${tourSteps.length}
            </div>
            <div style="display: flex; gap: 10px;">
                ${stepIndex > 0 ? `
                    <button onclick="showTourStep(${stepIndex - 1})" style="
                        background: rgba(40, 40, 40, 0.8);
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        color: #f0f0f0;
                        padding: 10px 20px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: 600;
                        transition: all 0.3s;
                    ">
                        ← Anterior
                    </button>
                ` : ''}
                
                ${stepIndex < tourSteps.length - 1 ? `
                    <button onclick="showTourStep(${stepIndex + 1})" style="
                        background: linear-gradient(135deg, #f472b6, #db2777);
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: 600;
                        transition: all 0.3s;
                    ">
                        Siguiente →
                    </button>
                ` : `
                    <button onclick="endTour()" style="
                        background: linear-gradient(135deg, #10b981, #059669);
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: 600;
                        transition: all 0.3s;
                    ">
                        ¡Finalizar! ✨
                    </button>
                `}
                
                <button onclick="endTour()" style="
                    background: transparent;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    color: #a0a0a0;
                    padding: 10px 15px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 18px;
                    transition: all 0.3s;
                ">
                    ✕
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(tooltip);
}

// Finalizar tour
function endTour() {
    appState.tourActive = false;
    appState.tourStep = 0;
    
    // Eliminar elementos del tour
    const overlay = document.getElementById('tour-overlay');
    const tooltip = document.getElementById('tour-tooltip');
    const highlight = document.getElementById('tour-highlight');
    
    if (overlay) overlay.remove();
    if (tooltip) tooltip.remove();
    if (highlight) highlight.remove();
}

// ============================================
// DEMO INTERACTIVO
// ============================================

const demoResponses = [
    {
        keywords: ['hola', 'hi', 'hello', 'buenos días', 'buenas tardes'],
        response: '¡Hola! 👋 Soy el asistente de Chispart AI. Estoy aquí para mostrarte cómo nuestra plataforma puede revolucionar tu negocio. ¿Qué te gustaría saber?'
    },
    {
        keywords: ['precio', 'costo', 'cuanto cuesta', 'planes', 'tarifas'],
        response: 'Tenemos 3 planes flexibles: 💎 Starter ($49/mes), Professional ($149/mes) y Enterprise ($499/mes). Cada uno diseñado para diferentes necesidades. ¿Te gustaría conocer más detalles de alguno?'
    },
    {
        keywords: ['características', 'funciones', 'que hace', 'capacidades'],
        response: 'Chispart AI ofrece: 🤖 Agentes inteligentes colaborativos, ⚡ Automatización de procesos, 📊 Análisis avanzado con IA, 🔒 Seguridad empresarial, 🌐 Integraciones fáciles, y 📈 Escalabilidad ilimitada. ¿Qué característica te interesa más?'
    },
    {
        keywords: ['automatización', 'automatizar', 'procesos'],
        response: 'Nuestra automatización es increíble! 🚀 Puedes automatizar tareas repetitivas, flujos de trabajo complejos, análisis de datos, generación de reportes y mucho más. Los clientes ahorran hasta 20 horas semanales. ¿Qué procesos te gustaría automatizar?'
    },
    {
        keywords: ['seguridad', 'protección', 'datos', 'privacidad'],
        response: '🔒 La seguridad es nuestra prioridad. Ofrecemos: encriptación end-to-end, cumplimiento GDPR y SOC2, backups automáticos, autenticación multifactor y auditorías de seguridad. Tus datos están 100% protegidos.'
    },
    {
        keywords: ['integración', 'integrar', 'conectar', 'api'],
        response: '🌐 Nos integramos con todo! Slack, Microsoft Teams, Google Workspace, Salesforce, HubSpot, Zapier y más. También ofrecemos API REST completa y webhooks. ¿Con qué herramientas necesitas integrarte?'
    },
    {
        keywords: ['empezar', 'comenzar', 'registrar', 'prueba', 'demo'],
        response: '¡Excelente! 🎉 Para empezar: 1) Elige tu plan ideal, 2) Completa el registro rápido, 3) Configura tu primer agente en minutos. Ofrecemos onboarding personalizado y soporte 24/7. ¿Listo para transformar tu negocio?'
    },
    {
        keywords: ['soporte', 'ayuda', 'asistencia', 'support'],
        response: '💬 Nuestro soporte es excepcional: Email 24/7 en todos los planes, Chat prioritario en Professional y Enterprise, y Account Manager dedicado en Enterprise. Tiempo de respuesta promedio: 2 horas. ¡Siempre estamos aquí para ti!'
    },
    {
        keywords: ['casos', 'ejemplos', 'clientes', 'testimonios'],
        response: '🌟 Nuestros clientes han logrado resultados increíbles: 40% reducción en costos operativos, 3x aumento en productividad, 95% satisfacción del cliente. Empresas de tecnología, finanzas, retail y salud confían en nosotros.'
    },
    {
        keywords: ['diferencia', 'competencia', 'mejor', 'por qué'],
        response: '✨ Lo que nos hace únicos: Agentes multiagente colaborativos (no solo chatbots), IA de última generación, interfaz intuitiva, personalización total, y el mejor soporte del mercado. Pruébanos y verás la diferencia!'
    }
];

// Enviar mensaje en el demo
function sendDemoMessage() {
    const input = document.getElementById('demoInput');
    const chatContainer = document.getElementById('demoChat');
    
    if (!input || !chatContainer) return;
    
    const message = input.value.trim();
    if (!message) return;
    
    // Agregar mensaje del usuario
    addDemoChatMessage(message, 'user');
    input.value = '';
    
    // Simular "escribiendo..."
    setTimeout(() => {
        const response = getDemoResponse(message);
        addDemoChatMessage(response, 'bot');
    }, 1000 + Math.random() * 1000);
}

// Agregar mensaje al chat del demo
function addDemoChatMessage(text, sender) {
    const chatContainer = document.getElementById('demoChat');
    if (!chatContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    
    if (sender === 'bot') {
        messageDiv.innerHTML = `
            <strong>Asistente Chispart AI</strong>
            <p>${text}</p>
        `;
    } else {
        messageDiv.innerHTML = `
            <strong>Tú</strong>
            <p>${text}</p>
        `;
    }
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // Guardar en estado
    appState.demoMessages.push({ text, sender });
}

// Obtener respuesta del demo
function getDemoResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Buscar respuesta basada en keywords
    for (const response of demoResponses) {
        for (const keyword of response.keywords) {
            if (lowerMessage.includes(keyword)) {
                return response.response;
            }
        }
    }
    
    // Respuesta por defecto
    return '¡Interesante pregunta! 🤔 Chispart AI puede ayudarte con eso y mucho más. Nuestros agentes inteligentes aprenden de tu negocio para ofrecer soluciones personalizadas. ¿Te gustaría agendar una demo personalizada con nuestro equipo?';
}

// Manejar Enter en el input del demo
function handleDemoEnter(event) {
    if (event.key === 'Enter') {
        sendDemoMessage();
    }
}

// ============================================
// SELECCIÓN DE PLAN
// ============================================

function selectPlan(planName, price) {
    appState.selectedPlan = planName;
    appState.selectedPrice = price;
    
    // Ocultar secciones anteriores
    document.getElementById('home').style.display = 'none';
    document.getElementById('features').style.display = 'none';
    document.getElementById('pricing').style.display = 'none';
    document.getElementById('demo').style.display = 'none';
    
    // Mostrar sección de registro
    const registerSection = document.getElementById('register');
    registerSection.classList.remove('hidden');
    registerSection.style.display = 'block';
    
    // Scroll a la sección de registro
    registerSection.scrollIntoView({ behavior: 'smooth' });
    
    // Mostrar notificación
    showNotification(`Plan ${planName} seleccionado. Completa tu registro para continuar.`, 'success');
}

// ============================================
// REGISTRO
// ============================================

function handleRegistration(event) {
    event.preventDefault();
    
    // Obtener datos del formulario
    const formData = {
        firstName: document.getElementById('firstName').value,
        lastName: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        company: document.getElementById('company').value,
        phone: document.getElementById('phone').value,
        country: document.getElementById('country').value,
        industry: document.getElementById('industry').value,
        employees: document.getElementById('employees').value,
        message: document.getElementById('message').value
    };
    
    // Validar datos
    if (!validateRegistrationForm(formData)) {
        return;
    }
    
    // Guardar en estado (en producción, enviar al backend)
    console.log('Datos de registro:', formData);
    
    // Ocultar formulario de registro
    document.getElementById('register').style.display = 'none';
    
    // Mostrar sección de pago
    const paymentSection = document.getElementById('payment');
    paymentSection.classList.remove('hidden');
    paymentSection.style.display = 'block';
    
    // Actualizar información del plan seleccionado
    document.getElementById('selectedPlanName').textContent = appState.selectedPlan.toUpperCase();
    document.getElementById('selectedPlanPrice').textContent = appState.selectedPrice;
    
    // Scroll a la sección de pago
    paymentSection.scrollIntoView({ behavior: 'smooth' });
    
    showNotification('Registro completado. Selecciona tu método de pago.', 'success');
}

// Validar formulario de registro
function validateRegistrationForm(data) {
    // Validar email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
        showNotification('Por favor ingresa un email válido.', 'error');
        return false;
    }
    
    // Validar teléfono
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    if (!phoneRegex.test(data.phone)) {
        showNotification('Por favor ingresa un teléfono válido.', 'error');
        return false;
    }
    
    // Validar campos requeridos
    const requiredFields = ['firstName', 'lastName', 'email', 'company', 'phone', 'country', 'industry', 'employees'];
    for (const field of requiredFields) {
        if (!data[field] || data[field].trim() === '') {
            showNotification('Por favor completa todos los campos requeridos.', 'error');
            return false;
        }
    }
    
    return true;
}

// ============================================
// PAGO
// ============================================

function selectPaymentMethod(method) {
    appState.selectedPaymentMethod = method;
    
    // Actualizar UI
    document.querySelectorAll('.payment-method').forEach(el => {
        el.classList.remove('selected');
    });
    
    event.target.closest('.payment-method').classList.add('selected');
    
    // Mostrar detalles de pago
    document.getElementById('paymentDetails').classList.remove('hidden');
    document.getElementById('paymentDetails').style.display = 'block';
    
    showNotification(`Método de pago ${method} seleccionado.`, 'success');
}

function processPayment() {
    if (!appState.selectedPaymentMethod) {
        showNotification('Por favor selecciona un método de pago.', 'error');
        return;
    }
    
    // Ocultar detalles de pago
    document.getElementById('paymentDetails').style.display = 'none';
    
    // Mostrar procesando
    const processingDiv = document.getElementById('paymentProcessing');
    processingDiv.classList.remove('hidden');
    processingDiv.style.display = 'block';
    
    // Simular procesamiento de pago
    setTimeout(() => {
        // Ocultar procesando
        processingDiv.style.display = 'none';
        
        // Mostrar éxito
        const successDiv = document.getElementById('paymentSuccess');
        successDiv.classList.remove('hidden');
        successDiv.style.display = 'block';
        
        // Scroll al mensaje de éxito
        successDiv.scrollIntoView({ behavior: 'smooth' });
        
        // Confetti animation (opcional)
        createConfetti();
        
        // Guardar en localStorage
        localStorage.setItem('chispart_subscription', JSON.stringify({
            plan: appState.selectedPlan,
            price: appState.selectedPrice,
            date: new Date().toISOString()
        }));
        
    }, 3000);
}

// ============================================
// UTILIDADES
// ============================================

// Mostrar notificación
function showNotification(message, type = 'info') {
    // Eliminar notificación existente
    const existingNotification = document.getElementById('notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.id = 'notification';
    
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#3b82f6',
        warning: '#f59e0b'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type] || colors.info};
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 10001;
        animation: slideInRight 0.3s ease-out;
        max-width: 400px;
        font-weight: 600;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Crear efecto confetti
function createConfetti() {
    const colors = ['#f472b6', '#67e8f9', '#a3e635', '#fbbf24', '#c084fc'];
    const confettiCount = 50;
    
    for (let i = 0; i < confettiCount; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                top: -10px;
                left: ${Math.random() * 100}%;
                opacity: 1;
                transform: rotate(${Math.random() * 360}deg);
                z-index: 10000;
                pointer-events: none;
                animation: confettiFall ${2 + Math.random() * 2}s linear forwards;
            `;
            
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 4000);
        }, i * 30);
    }
}

// ============================================
// ANIMACIONES CSS
// ============================================

// Agregar estilos de animación
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5), 0 0 20px rgba(244, 114, 182, 0.5);
        }
        50% {
            box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5), 0 0 40px rgba(244, 114, 182, 0.8);
        }
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    @keyframes confettiFall {
        to {
            top: 100vh;
            opacity: 0;
            transform: translateX(${Math.random() * 200 - 100}px) rotate(${Math.random() * 720}deg);
        }
    }
    
    /* Estilos para botones hover */
    button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    button:active {
        transform: translateY(0);
    }
`;
document.head.appendChild(style);

// ============================================
// INICIALIZACIÓN
// ============================================

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('Chispart AI Landing Page cargada');
    
    // Agregar mensaje inicial al demo
    setTimeout(() => {
        const demoChat = document.getElementById('demoChat');
        if (demoChat && appState.demoMessages.length === 0) {
            // El mensaje inicial ya está en el HTML
            appState.demoMessages.push({
                text: '¡Hola! Soy tu asistente de ventas inteligente...',
                sender: 'bot'
            });
        }
    }, 500);
    
    // Iniciar tour automáticamente después de 2 segundos (opcional)
    // setTimeout(() => {
    //     if (!localStorage.getItem('chispart_tour_completed')) {
    //         startTour();
    //     }
    // }, 2000);
    
    // Agregar botón para iniciar tour manualmente
    const heroButtons = document.querySelector('.hero-buttons');
    if (heroButtons) {
        const tourButton = document.createElement('button');
        tourButton.className = 'btn-secondary';
        tourButton.textContent = '🎯 Tour Guiado';
        tourButton.onclick = startTour;
        tourButton.style.marginLeft = '10px';
        heroButtons.appendChild(tourButton);
    }
});

// Exponer funciones globales
window.startTour = startTour;
window.endTour = endTour;
window.showTourStep = showTourStep;
window.sendDemoMessage = sendDemoMessage;
window.handleDemoEnter = handleDemoEnter;
window.selectPlan = selectPlan;
window.handleRegistration = handleRegistration;
window.selectPaymentMethod = selectPaymentMethod;
window.processPayment = processPayment;

console.log('✨ Chispart AI JavaScript cargado correctamente');
