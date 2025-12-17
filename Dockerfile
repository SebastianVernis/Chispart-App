# Multi-stage build para optimización
FROM python:3.11-slim as builder

# Instalar dependencias de compilación
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar solo archivos de requisitos primero (mejor caché)
COPY requirements.txt .

# Instalar dependencias en un directorio temporal
RUN pip install --no-cache-dir --user -r requirements.txt

# Etapa final
FROM python:3.11-slim

# Instalar curl para healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/logs /app/config /app/static /app/frontend && \
    chown -R appuser:appuser /app

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias de Python desde builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copiar código fuente
COPY --chown=appuser:appuser . .

# Asegurar que los directorios necesarios existan
RUN mkdir -p /app/logs /app/config /app/static /app/frontend && \
    chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Agregar binarios de Python al PATH
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto - servidor FastAPI
CMD ["python", "main.py"]
