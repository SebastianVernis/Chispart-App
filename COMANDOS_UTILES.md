# 🛠️ Comandos Útiles - Chispart AI

Referencia rápida de comandos para trabajar con Chispart AI.

---

## 🚀 Inicio Rápido

### **Con Script (Recomendado)**
```bash
# Primera vez
./docker-quick-start.sh setup
./docker-quick-start.sh build
./docker-quick-start.sh start

# Desarrollo
./docker-quick-start.sh dev

# Ver ayuda
./docker-quick-start.sh help
```

### **Manual con Docker Compose**
```bash
# Producción
docker-compose up -d --build

# Desarrollo
docker-compose --profile dev up

# Detener
docker-compose down
```

---

## 🐳 Docker

### **Construcción**
```bash
# Construir imagen
docker-compose build blackbox-hybrid-tool

# Construir sin cache
docker-compose build --no-cache blackbox-hybrid-tool

# Ver imágenes
docker images | grep blackbox
```

### **Ejecución**
```bash
# Iniciar servicios
docker-compose up -d

# Iniciar con logs
docker-compose up

# Iniciar solo un servicio
docker-compose up -d blackbox-hybrid-tool

# Reiniciar
docker-compose restart blackbox-hybrid-tool
```

### **Logs**
```bash
# Ver logs en tiempo real
docker-compose logs -f blackbox-hybrid-tool

# Ver últimas 100 líneas
docker-compose logs --tail=100 blackbox-hybrid-tool

# Ver logs desde hace 1 hora
docker-compose logs --since 1h blackbox-hybrid-tool
```

### **Estado**
```bash
# Ver contenedores
docker-compose ps

# Ver detalles de healthcheck
docker inspect --format='{{json .State.Health}}' blackbox-hybrid-tool | jq

# Ver uso de recursos
docker stats blackbox-hybrid-tool
```

### **Limpieza**
```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar también volúmenes
docker-compose down -v

# Limpiar todo Docker
docker system prune -a
```

---

## 🧪 Testing de Endpoints

### **Health Check**
```bash
# Simple
curl http://localhost:8005/health

# Con formato JSON
curl -s http://localhost:8005/health | jq

# Verificar código de estado
curl -I http://localhost:8005/health
```

### **Modelos**
```bash
# Listar modelos
curl -s http://localhost:8005/models | jq

# Cambiar modelo
curl -X POST http://localhost:8005/models/switch \
  -H "Content-Type: application/json" \
  -d '{"model": "blackboxai/openai/o1"}' | jq
```

### **Chat**
```bash
# Chat simple
curl -X POST http://localhost:8005/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}' | jq

# Chat con parámetros
curl -X POST http://localhost:8005/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain Docker in 50 words",
    "model_type": "blackboxai/openai/o1",
    "max_tokens": 100,
    "temperature": 0.7
  }' | jq
```

### **Ciclos de Desarrollo**
```bash
# Listar ciclos
curl -s http://localhost:8005/cycles | jq

# Crear ciclo
curl -X POST http://localhost:8005/cycles \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Feature",
    "initial_prompt": "Let'\''s build something"
  }' | jq

# Ver ciclo específico
curl -s http://localhost:8005/cycles/{cycle_id} | jq
```

### **Archivos**
```bash
# Escribir archivo
curl -X POST http://localhost:8005/files/write \
  -H "Content-Type: application/json" \
  -d '{
    "path": "test.txt",
    "content": "Hello World",
    "overwrite": true
  }' | jq
```

---

## 🔍 Debugging

### **Entrar al Contenedor**
```bash
# Shell interactivo
docker-compose exec blackbox-hybrid-tool bash

# Como root (si necesitas instalar algo)
docker-compose exec -u root blackbox-hybrid-tool bash

# Ejecutar comando único
docker-compose exec blackbox-hybrid-tool ls -la /app
```

### **Ver Variables de Entorno**
```bash
# Dentro del contenedor
docker-compose exec blackbox-hybrid-tool env | grep -E 'BLACKBOX|APP_'

# Desde docker-compose
docker-compose config
```

### **Verificar Archivos**
```bash
# Ver estructura
docker-compose exec blackbox-hybrid-tool tree -L 2 /app

# Ver logs de la app
docker-compose exec blackbox-hybrid-tool cat /app/logs/app.log

# Ver configuración
docker-compose exec blackbox-hybrid-tool cat /app/config/models.json
```

---

## 📊 Monitoreo

### **Healthcheck Continuo**
```bash
# Verificar cada 5 segundos
watch -n 5 'curl -s http://localhost:8005/health | jq'

# Con timestamp
while true; do
  echo "$(date): $(curl -s http://localhost:8005/health | jq -r .status)"
  sleep 5
done
```

### **Logs en Tiempo Real**
```bash
# Todos los logs
docker-compose logs -f

# Solo errores
docker-compose logs -f | grep -i error

# Con timestamp
docker-compose logs -f --timestamps
```

### **Métricas de Recursos**
```bash
# Uso de CPU y memoria
docker stats blackbox-hybrid-tool --no-stream

# Continuo
docker stats blackbox-hybrid-tool

# Formato personalizado
docker stats blackbox-hybrid-tool --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

---

## 🔧 Desarrollo Local (Sin Docker)

### **Instalación**
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### **Ejecución**
```bash
# Servidor de desarrollo
python main.py

# Con uvicorn y hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Con puerto específico
PORT=8007 python main.py
```

### **Testing**
```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=blackbox_hybrid_tool

# Test específico
pytest tests/test_endpoints.py -v
```

---

## 🔐 Seguridad

### **Verificar Permisos**
```bash
# Ver usuario del proceso
docker-compose exec blackbox-hybrid-tool whoami

# Ver permisos de archivos
docker-compose exec blackbox-hybrid-tool ls -la /app

# Verificar que no corre como root
docker-compose exec blackbox-hybrid-tool id
```

### **Escanear Vulnerabilidades**
```bash
# Con Docker Scout (si está disponible)
docker scout cves blackbox-hybrid-tool:latest

# Con Trivy
trivy image blackbox-hybrid-tool:latest
```

---

## 📦 Backup y Restore

### **Backup**
```bash
# Backup de configuración
cp config/models.json config/models.json.backup

# Backup de logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/

# Backup de volúmenes Docker
docker run --rm -v blackbox-hybrid-tool_logs:/data -v $(pwd):/backup \
  alpine tar czf /backup/volumes-backup.tar.gz /data
```

### **Restore**
```bash
# Restore configuración
cp config/models.json.backup config/models.json

# Restore logs
tar -xzf logs-backup-20251217.tar.gz

# Reiniciar servicios
docker-compose restart
```

---

## 🚀 Deploy a Producción

### **Pre-Deploy**
```bash
# 1. Pull de cambios
git pull origin main

# 2. Verificar cambios
git log -5 --oneline

# 3. Backup actual
./docker-quick-start.sh stop
tar -czf backup-$(date +%Y%m%d-%H%M%S).tar.gz config/ logs/
```

### **Deploy**
```bash
# 1. Rebuild
./docker-quick-start.sh rebuild

# 2. Verificar
./docker-quick-start.sh status

# 3. Test endpoints
curl http://localhost:8005/health
curl http://localhost:8005/models
```

### **Post-Deploy**
```bash
# 1. Monitorear logs
./docker-quick-start.sh logs

# 2. Verificar healthcheck
watch -n 10 './docker-quick-start.sh status'

# 3. Test funcional
curl -X POST http://localhost:8005/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test post-deploy"}' | jq
```

---

## 🐛 Troubleshooting

### **Contenedor no inicia**
```bash
# Ver logs de error
docker-compose logs blackbox-hybrid-tool

# Ver eventos de Docker
docker events --filter container=blackbox-hybrid-tool

# Verificar configuración
docker-compose config --quiet && echo "Config OK" || echo "Config ERROR"
```

### **Healthcheck falla**
```bash
# Verificar endpoint manualmente
docker-compose exec blackbox-hybrid-tool curl -f http://localhost:8000/health

# Ver logs de healthcheck
docker inspect blackbox-hybrid-tool | jq '.[0].State.Health'

# Reiniciar servicio
docker-compose restart blackbox-hybrid-tool
```

### **Puerto ocupado**
```bash
# Ver qué usa el puerto
lsof -i :8005
# o
netstat -tulpn | grep 8005

# Cambiar puerto en .env
echo "PORT=8007" >> .env
docker-compose up -d
```

### **Problemas de permisos**
```bash
# Verificar permisos de volúmenes
ls -la logs/ config/

# Arreglar permisos
sudo chown -R $USER:$USER logs/ config/

# Recrear contenedor
docker-compose down
docker-compose up -d
```

---

## 📚 Referencias Rápidas

### **URLs Importantes**
- Frontend: http://localhost:8005
- Playground: http://localhost:8005/playground
- API Docs: http://localhost:8005/docs
- ReDoc: http://localhost:8005/redoc
- Health: http://localhost:8005/health

### **Archivos Clave**
- Configuración: `config/models.json`
- Variables: `.env`
- Logs: `logs/`
- Docker: `Dockerfile`, `docker-compose.yml`
- Script: `docker-quick-start.sh`

### **Comandos del Script**
```bash
./docker-quick-start.sh setup      # Configurar
./docker-quick-start.sh build      # Construir
./docker-quick-start.sh start      # Iniciar
./docker-quick-start.sh dev        # Desarrollo
./docker-quick-start.sh stop       # Detener
./docker-quick-start.sh restart    # Reiniciar
./docker-quick-start.sh rebuild    # Reconstruir
./docker-quick-start.sh logs       # Ver logs
./docker-quick-start.sh status     # Ver estado
./docker-quick-start.sh clean      # Limpiar
```

---

**Tip:** Guarda este archivo como referencia rápida. Todos los comandos han sido probados y funcionan correctamente.

**Última actualización:** 17 de Diciembre, 2025
