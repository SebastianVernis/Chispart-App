#!/bin/bash
# Script de inicio rápido para Chispart AI con Docker
# Uso: ./docker-quick-start.sh [comando]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Verificar que Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        echo "Instala Docker desde: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose no está instalado"
        echo "Instala Docker Compose desde: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker y Docker Compose están instalados"
}

# Verificar archivo .env
check_env() {
    if [ ! -f .env ]; then
        print_warning "Archivo .env no encontrado"
        print_info "Creando .env desde .env.example..."
        cp .env.example .env
        print_warning "⚠ IMPORTANTE: Edita .env y configura BLACKBOX_API_KEY"
        echo ""
        echo "Abre .env y configura:"
        echo "  BLACKBOX_API_KEY=tu_api_key_aqui"
        echo ""
        read -p "Presiona Enter cuando hayas configurado la API key..."
    else
        print_success "Archivo .env encontrado"
    fi
}

# Construir imagen
build() {
    print_info "Construyendo imagen Docker..."
    docker-compose build blackbox-hybrid-tool
    print_success "Imagen construida exitosamente"
}

# Iniciar servicios
start() {
    print_info "Iniciando Chispart AI..."
    docker-compose up -d blackbox-hybrid-tool
    print_success "Servicio iniciado"
    
    # Esperar a que el servicio esté listo
    print_info "Esperando a que el servicio esté listo..."
    sleep 5
    
    # Verificar healthcheck
    if docker-compose ps | grep -q "healthy"; then
        print_success "Servicio saludable y listo"
    else
        print_warning "Servicio iniciado pero healthcheck pendiente"
    fi
    
    echo ""
    echo "🌐 Accede a la aplicación en:"
    echo "   Frontend: http://localhost:8005"
    echo "   Playground: http://localhost:8005/playground"
    echo "   API Docs: http://localhost:8005/docs"
    echo "   Health: http://localhost:8005/health"
}

# Iniciar en modo desarrollo
dev() {
    print_info "Iniciando en modo desarrollo..."
    docker-compose --profile dev up
}

# Detener servicios
stop() {
    print_info "Deteniendo servicios..."
    docker-compose down
    print_success "Servicios detenidos"
}

# Ver logs
logs() {
    print_info "Mostrando logs (Ctrl+C para salir)..."
    docker-compose logs -f blackbox-hybrid-tool
}

# Ver estado
status() {
    print_info "Estado de los servicios:"
    docker-compose ps
    
    echo ""
    print_info "Verificando health endpoint..."
    if curl -sf http://localhost:8005/health > /dev/null 2>&1; then
        print_success "API respondiendo correctamente"
        curl -s http://localhost:8005/health | python3 -m json.tool
    else
        print_warning "API no está respondiendo"
    fi
}

# Reiniciar servicios
restart() {
    print_info "Reiniciando servicios..."
    docker-compose restart blackbox-hybrid-tool
    print_success "Servicios reiniciados"
}

# Reconstruir y reiniciar
rebuild() {
    print_info "Reconstruyendo y reiniciando..."
    docker-compose down
    docker-compose build blackbox-hybrid-tool
    docker-compose up -d blackbox-hybrid-tool
    print_success "Reconstrucción completada"
}

# Limpiar todo
clean() {
    print_warning "Esto eliminará contenedores, imágenes y volúmenes"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Limpiando..."
        docker-compose down -v
        docker-compose rm -f
        print_success "Limpieza completada"
    else
        print_info "Operación cancelada"
    fi
}

# Mostrar ayuda
show_help() {
    cat << EOF
🚀 Chispart AI - Docker Quick Start

Uso: $0 [comando]

Comandos disponibles:

  setup       Verificar requisitos y configurar .env
  build       Construir imagen Docker
  start       Iniciar servicios en producción
  dev         Iniciar en modo desarrollo (con hot reload)
  stop        Detener servicios
  restart     Reiniciar servicios
  rebuild     Reconstruir imagen y reiniciar
  logs        Ver logs en tiempo real
  status      Ver estado de servicios y health
  clean       Limpiar contenedores e imágenes
  help        Mostrar esta ayuda

Ejemplos:

  # Primera vez
  $0 setup
  $0 build
  $0 start

  # Desarrollo
  $0 dev

  # Ver logs
  $0 logs

  # Reiniciar después de cambios
  $0 rebuild

EOF
}

# Comando principal
case "${1:-help}" in
    setup)
        check_docker
        check_env
        print_success "Setup completado"
        echo ""
        echo "Siguiente paso: $0 build"
        ;;
    build)
        check_docker
        build
        ;;
    start)
        check_docker
        check_env
        start
        ;;
    dev)
        check_docker
        check_env
        dev
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    rebuild)
        check_docker
        rebuild
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    clean)
        clean
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Comando desconocido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
