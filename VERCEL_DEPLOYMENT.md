# 🚀 Guía de Deployment en Vercel

Esta guía te ayudará a desplegar tu aplicación Blackbox Hybrid Tool en Vercel.

## 📋 Pre-requisitos

1. **Cuenta de Vercel**: Crea una cuenta en [vercel.com](https://vercel.com)
2. **Vercel CLI** (opcional, para deployment local):
   ```bash
   npm install -g vercel
   ```
3. **API Key de Blackbox**: Obtén tu API key de [Blackbox AI](https://blackbox.ai)

## 🔧 Configuración Inicial

### 1. Preparar el Proyecto

El proyecto ya está configurado con los archivos necesarios:
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `api/index.py` - Entry point serverless
- ✅ `requirements.txt` - Dependencias Python con Mangum
- ✅ `.vercelignore` - Archivos excluidos del deployment
- ✅ `.env.example` - Template de variables de entorno

### 2. Configurar Variables de Entorno en Vercel

#### Opción A: Desde el Dashboard de Vercel

1. Ve a tu proyecto en Vercel Dashboard
2. Navega a **Settings** → **Environment Variables**
3. Agrega las siguientes variables:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `BLACKBOX_API_KEY` | `tu_api_key` | **Requerido**: Tu API key de Blackbox |
| `CONFIG_FILE` | `config/models.json` | Ruta al archivo de configuración |
| `WRITE_ROOT` | `/tmp` | Directorio de escritura (solo /tmp es writable en Vercel) |
| `AUTO_SNAPSHOT` | `false` | Deshabilitar snapshots en serverless |
| `APP_NAME` | `Blackbox Hybrid Tool` | Nombre de la aplicación |
| `APP_VERSION` | `1.0.0` | Versión de la aplicación |

#### Opción B: Desde Vercel CLI

```bash
vercel env add BLACKBOX_API_KEY
# Ingresa tu API key cuando se solicite

vercel env add CONFIG_FILE
# Ingresa: config/models.json

vercel env add WRITE_ROOT
# Ingresa: /tmp

vercel env add AUTO_SNAPSHOT
# Ingresa: false
```

### 3. Verificar Configuración Local (Opcional)

Antes de desplegar, puedes probar localmente:

```bash
# Instalar Vercel CLI si no lo tienes
npm install -g vercel

# Crear archivo .env local (no commitear)
cp .env.example .env
# Edita .env y agrega tu BLACKBOX_API_KEY

# Ejecutar en modo desarrollo
vercel dev
```

La aplicación estará disponible en `http://localhost:3000`

## 🚀 Deployment

### Opción 1: Deployment desde GitHub (Recomendado)

1. **Sube tu código a GitHub**:
   ```bash
   git add .
   git commit -m "Configurar para Vercel deployment"
   git push origin main
   ```

2. **Conecta con Vercel**:
   - Ve a [vercel.com/new](https://vercel.com/new)
   - Selecciona "Import Git Repository"
   - Elige tu repositorio
   - Vercel detectará automáticamente la configuración de `vercel.json`

3. **Configura las variables de entorno** (ver sección anterior)

4. **Deploy**: Click en "Deploy"

### Opción 2: Deployment desde CLI

```bash
# Login en Vercel (primera vez)
vercel login

# Deploy a producción
vercel --prod

# O deploy a preview
vercel
```

## 🔍 Verificación Post-Deployment

Una vez desplegado, verifica que todo funcione:

### 1. Health Check
```bash
curl https://tu-proyecto.vercel.app/health
# Respuesta esperada: {"status": "healthy"}
```

### 2. Listar Modelos
```bash
curl https://tu-proyecto.vercel.app/models
```

### 3. Test de Chat
```bash
curl -X POST https://tu-proyecto.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hola, ¿cómo estás?",
    "model_type": "blackboxai/openai/o1"
  }'
```

### 4. Acceder a la Interfaz Web
Visita: `https://tu-proyecto.vercel.app/playground`

## 📊 Monitoreo

### Ver Logs en Tiempo Real

1. **Desde Dashboard**:
   - Ve a tu proyecto en Vercel
   - Click en "Deployments"
   - Selecciona un deployment
   - Click en "View Function Logs"

2. **Desde CLI**:
   ```bash
   vercel logs
   ```

### Métricas de Performance

Vercel proporciona métricas automáticas:
- Tiempo de respuesta
- Tasa de errores
- Uso de memoria
- Cold starts

Accede a ellas en: **Dashboard → Analytics**

## ⚙️ Configuración Avanzada

### Ajustar Límites de Función

En `vercel.json`, puedes ajustar:

```json
{
  "functions": {
    "api/index.py": {
      "memory": 1024,        // MB de memoria (512-3008)
      "maxDuration": 60      // Segundos (10-300 en Pro)
    }
  }
}
```

### Configurar Regiones

Para mejor latencia, especifica regiones:

```json
{
  "regions": ["iad1", "sfo1"]  // Virginia y San Francisco
}
```

Regiones disponibles:
- `iad1` - Washington, D.C., USA
- `sfo1` - San Francisco, USA
- `gru1` - São Paulo, Brazil
- `fra1` - Frankfurt, Germany
- `hnd1` - Tokyo, Japan
- `sin1` - Singapore

### Custom Domain

1. Ve a **Settings → Domains**
2. Agrega tu dominio personalizado
3. Configura los DNS según las instrucciones

## 🐛 Troubleshooting

### Error: "Module not found"

**Solución**: Verifica que todas las dependencias estén en `requirements.txt`

```bash
# Regenerar requirements.txt
pip freeze > requirements.txt
```

### Error: "Function timeout"

**Solución**: Aumenta `maxDuration` en `vercel.json`:

```json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 60
    }
  }
}
```

### Error: "Cannot write to filesystem"

**Solución**: Asegúrate de usar `/tmp` para escritura:

```python
os.environ["WRITE_ROOT"] = "/tmp"
```

### Cold Starts Lentos

**Soluciones**:
1. Optimiza imports (lazy loading)
2. Reduce tamaño de dependencias
3. Considera Vercel Pro para mejor performance
4. Usa warming requests (ping periódico)

### Error: "Environment variable not found"

**Solución**: Verifica que las variables estén configuradas en Vercel:

```bash
vercel env ls
```

## 🔒 Seguridad

### Mejores Prácticas

1. **Nunca commitear secrets**:
   ```bash
   # Asegúrate de que .env está en .gitignore
   echo ".env" >> .gitignore
   ```

2. **Usar variables de entorno de Vercel** para todos los secrets

3. **Limitar acceso a archivos**:
   - Solo `/tmp` es writable
   - Validar paths de usuario

4. **Rate Limiting**: Considera agregar rate limiting para APIs públicas

5. **CORS**: Ajusta CORS según tus necesidades en `main.py`

## 📈 Optimización

### Reducir Cold Starts

1. **Minimizar imports**:
   ```python
   # Malo
   import heavy_library
   
   # Bueno
   def my_function():
       import heavy_library
       # usar library
   ```

2. **Usar lifespan="off"** en Mangum (ya configurado)

3. **Warming function** (opcional):
   ```bash
   # Cron job para mantener función caliente
   */5 * * * * curl https://tu-proyecto.vercel.app/health
   ```

### Reducir Tamaño de Deployment

1. Usa `.vercelignore` para excluir archivos innecesarios
2. Minimiza dependencias en `requirements.txt`
3. Usa versiones específicas de paquetes

## 🔄 CI/CD

### Deployment Automático

Vercel despliega automáticamente cuando:
- Push a `main` → Producción
- Push a otras ramas → Preview

### Preview Deployments

Cada PR obtiene una URL única de preview:
```
https://tu-proyecto-git-branch-user.vercel.app
```

### Rollback

Si algo sale mal:

1. **Desde Dashboard**:
   - Ve a "Deployments"
   - Encuentra el deployment anterior
   - Click en "..." → "Promote to Production"

2. **Desde CLI**:
   ```bash
   vercel rollback
   ```

## 📚 Recursos Adicionales

- [Documentación de Vercel](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Mangum Documentation](https://mangum.io/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## 💡 Tips

1. **Usa Preview Deployments** para probar cambios antes de producción
2. **Monitorea logs** regularmente para detectar errores
3. **Configura alertas** en Vercel para errores críticos
4. **Documenta cambios** en variables de entorno
5. **Mantén actualizado** `requirements.txt`

## 🆘 Soporte

Si encuentras problemas:

1. Revisa los logs: `vercel logs`
2. Consulta la [documentación de Vercel](https://vercel.com/docs)
3. Abre un issue en el repositorio
4. Contacta al equipo de soporte de Vercel

---

**¡Listo para desplegar! 🚀**

Para comenzar:
```bash
vercel --prod
```
