# ✅ Resumen de Configuración para Vercel

## 🎉 Configuración Completada

Tu proyecto **Blackbox Hybrid Tool** ha sido adaptado exitosamente para deployment en Vercel.

## 📁 Archivos Creados/Modificados

### ✨ Nuevos Archivos

1. **`vercel.json`** - Configuración principal de Vercel
   - Runtime de Python configurado
   - Rutas API y archivos estáticos
   - Variables de entorno
   - Límites de función (1024MB, 60s timeout)

2. **`api/index.py`** - Entry point serverless
   - Adaptador Mangum para FastAPI
   - Configuración para entorno serverless
   - Manejo de paths y configuración

3. **`.vercelignore`** - Exclusiones de deployment
   - Archivos de desarrollo
   - Tests y documentación
   - Archivos grandes innecesarios

4. **`.env.example`** - Template de variables de entorno
   - Todas las variables documentadas
   - Valores de ejemplo

5. **`VERCEL_DEPLOYMENT.md`** - Guía completa de deployment
   - Instrucciones paso a paso
   - Troubleshooting
   - Optimizaciones
   - Mejores prácticas

6. **`vercel-setup.sh`** - Script de configuración automática
   - Verificación de requisitos
   - Configuración de variables
   - Deployment automatizado

### 🔄 Archivos Modificados

1. **`requirements.txt`**
   - ✅ Agregado `mangum>=0.17.0` (adaptador ASGI)
   - ✅ Agregado `uvicorn>=0.24.0`
   - ✅ Agregado `pydantic>=2.0.0`
   - ✅ Actualizado `fastapi>=0.104.0`

## 🚀 Pasos para Desplegar

### Opción 1: Script Automático (Recomendado)

```bash
./vercel-setup.sh
```

Este script te guiará a través de:
1. Verificación de Vercel CLI
2. Configuración de variables de entorno
3. Prueba local (opcional)
4. Deployment a producción

### Opción 2: Manual

#### 1. Instalar Vercel CLI

```bash
npm install -g vercel
```

#### 2. Configurar Variables de Entorno

```bash
# Login en Vercel
vercel login

# Agregar variables de entorno
vercel env add BLACKBOX_API_KEY production
# Ingresa tu API key

vercel env add CONFIG_FILE production
# Ingresa: config/models.json

vercel env add WRITE_ROOT production
# Ingresa: /tmp

vercel env add AUTO_SNAPSHOT production
# Ingresa: false
```

#### 3. Desplegar

```bash
# Deploy a producción
vercel --prod
```

### Opción 3: Desde GitHub

1. Push tu código a GitHub:
   ```bash
   git add .
   git commit -m "Configurar para Vercel"
   git push origin main
   ```

2. Conecta tu repositorio en [vercel.com/new](https://vercel.com/new)

3. Configura las variables de entorno en el dashboard

4. Deploy automático

## 🔐 Variables de Entorno Requeridas

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `BLACKBOX_API_KEY` | `tu_api_key` | ⚠️ **REQUERIDO** - Tu API key de Blackbox |
| `CONFIG_FILE` | `config/models.json` | Ruta al archivo de configuración |
| `WRITE_ROOT` | `/tmp` | Directorio de escritura (solo /tmp en Vercel) |
| `AUTO_SNAPSHOT` | `false` | Deshabilitar snapshots en serverless |

### Variables Opcionales

- `APP_NAME` - Nombre de la aplicación
- `APP_VERSION` - Versión
- `SERPAPI_KEY` - Para búsqueda web
- `TAVILY_API_KEY` - Para búsqueda web alternativa
- `GH_TOKEN` - Para integración con GitHub

## 🧪 Verificación Post-Deployment

Una vez desplegado, verifica:

### 1. Health Check
```bash
curl https://tu-proyecto.vercel.app/health
```
**Respuesta esperada**: `{"status": "healthy"}`

### 2. API de Modelos
```bash
curl https://tu-proyecto.vercel.app/models
```

### 3. Chat Endpoint
```bash
curl -X POST https://tu-proyecto.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hola", "model_type": "blackboxai/openai/o1"}'
```

### 4. Interfaz Web
Visita: `https://tu-proyecto.vercel.app/playground`

## 📊 Estructura del Proyecto

```
/vercel/sandbox/
├── api/
│   └── index.py              # ✨ Entry point serverless
├── blackbox_hybrid_tool/     # Código principal
│   ├── cli/
│   ├── core/
│   ├── config/
│   └── utils/
├── config/
│   └── models.json           # Configuración de modelos
├── frontend/                 # Archivos frontend
├── static/                   # Archivos estáticos
├── main.py                   # App FastAPI original
├── requirements.txt          # 🔄 Actualizado con mangum
├── vercel.json              # ✨ Configuración Vercel
├── .vercelignore            # ✨ Exclusiones
├── .env.example             # ✨ Template variables
├── vercel-setup.sh          # ✨ Script de setup
├── VERCEL_DEPLOYMENT.md     # ✨ Guía completa
└── VERCEL_SETUP_SUMMARY.md  # ✨ Este archivo
```

## 🔧 Configuración Técnica

### Runtime
- **Python**: 3.9+
- **Framework**: FastAPI con Mangum adapter
- **Región**: `iad1` (Virginia, USA)

### Límites de Función
- **Memoria**: 1024 MB
- **Timeout**: 60 segundos
- **Región**: iad1 (configurable)

### Rutas Configuradas

| Ruta | Destino | Descripción |
|------|---------|-------------|
| `/api/*` | `api/index.py` | Endpoints API |
| `/static/*` | Archivos estáticos | CSS, JS, imágenes |
| `/frontend/*` | Archivos frontend | HTML, componentes |
| `/` | `api/index.py` | Página principal |
| `/playground` | `api/index.py` | Interfaz de prueba |
| `/health` | `api/index.py` | Health check |
| `/chat` | `api/index.py` | Chat endpoint |
| `/models` | `api/index.py` | Gestión de modelos |

## 🎯 Características Soportadas

### ✅ Funcionalidades Disponibles

- ✅ API REST completa
- ✅ Chat con múltiples modelos
- ✅ Generación de imágenes
- ✅ Generación de videos
- ✅ Gestión de modelos
- ✅ Interfaz web (playground)
- ✅ Health checks
- ✅ CORS configurado
- ✅ Documentación automática (`/docs`)

### ⚠️ Limitaciones en Vercel

- ⚠️ Filesystem read-only (excepto `/tmp`)
- ⚠️ Timeout máximo: 60s (300s en Pro)
- ⚠️ Cold starts en funciones serverless
- ⚠️ No persistencia de archivos entre requests
- ⚠️ Límite de tamaño de deployment

### 💡 Soluciones

1. **Archivos temporales**: Usar `/tmp` (configurado en `WRITE_ROOT`)
2. **Persistencia**: Usar servicios externos (S3, Database)
3. **Cold starts**: Optimizar imports, usar warming
4. **Timeouts**: Optimizar código, considerar Vercel Pro

## 📈 Optimizaciones Implementadas

1. **Mangum Adapter**: Configurado con `lifespan="off"` para reducir cold starts
2. **Exclusiones**: `.vercelignore` reduce tamaño de deployment
3. **Configuración**: Variables de entorno optimizadas para serverless
4. **Paths**: Adaptados para filesystem read-only

## 🐛 Troubleshooting Común

### Error: "Module not found: mangum"
**Solución**: Verifica que `mangum>=0.17.0` esté en `requirements.txt`

### Error: "Cannot write to filesystem"
**Solución**: Usa `/tmp` para escritura (ya configurado en `WRITE_ROOT`)

### Error: "Function timeout"
**Solución**: Aumenta `maxDuration` en `vercel.json` o optimiza código

### Error: "Environment variable not found"
**Solución**: Configura variables en Vercel Dashboard o CLI

## 📚 Recursos

- **Guía Completa**: `VERCEL_DEPLOYMENT.md`
- **Documentación Vercel**: https://vercel.com/docs
- **Vercel Python Runtime**: https://vercel.com/docs/runtimes#official-runtimes/python
- **Mangum**: https://mangum.io/
- **FastAPI**: https://fastapi.tiangolo.com/

## 🆘 Soporte

### Ver Logs
```bash
vercel logs
```

### Rollback
```bash
vercel rollback
```

### Dashboard
https://vercel.com/dashboard

## ✨ Próximos Pasos

1. **Desplegar**: Ejecuta `./vercel-setup.sh` o `vercel --prod`
2. **Verificar**: Prueba los endpoints
3. **Monitorear**: Revisa logs y métricas
4. **Optimizar**: Ajusta configuración según necesidades
5. **Escalar**: Considera Vercel Pro para más recursos

## 🎉 ¡Listo!

Tu aplicación está lista para desplegarse en Vercel. Ejecuta:

```bash
./vercel-setup.sh
```

O manualmente:

```bash
vercel --prod
```

---

**Desarrollado con ✨ por Chispart AI Team**
**Adaptado para Vercel 🚀**
