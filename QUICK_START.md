# 🚀 Quick Start - Vercel Deployment

## ⚡ Despliegue en 3 Pasos

### 1️⃣ Instalar Vercel CLI
```bash
npm install -g vercel
```

### 2️⃣ Configurar API Key
```bash
vercel env add BLACKBOX_API_KEY production
# Ingresa tu API key cuando se solicite
```

### 3️⃣ Desplegar
```bash
vercel --prod
```

## 🎯 O Usa el Script Automático

```bash
./vercel-setup.sh
```

## ✅ Verificar Deployment

```bash
# Health check
curl https://tu-proyecto.vercel.app/health

# Test chat
curl -X POST https://tu-proyecto.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hola"}'
```

## 📱 Acceder a la Interfaz

Visita: `https://tu-proyecto.vercel.app/playground`

## 📚 Más Información

- **Guía Completa**: `VERCEL_DEPLOYMENT.md`
- **Resumen**: `VERCEL_SETUP_SUMMARY.md`
- **Variables de Entorno**: `.env.example`

## 🆘 Ayuda Rápida

```bash
# Ver logs
vercel logs

# Rollback
vercel rollback

# Ver deployments
vercel ls

# Abrir dashboard
vercel open
```

---

**¡Listo en minutos! 🎉**
