# scripts/docker/cleanup.sh
#!/bin/bash
# Docker cleanup script for development environment

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

cleanup_containers() {
    log_info "Stopping and removing containers..."
    
    # Stop all running containers from docker-compose
    if [ -f "docker-compose.yml" ]; then
        docker-compose down -v --remove-orphans
    fi
    
    # Remove exited containers
    local exited_containers=$(docker ps -aq -f status=exited)
    if [ ! -z "$exited_containers" ]; then
        docker rm $exited_containers
        log_info "Removed exited containers"
    fi
}

cleanup_images() {
    log_info "Cleaning up Docker images..."
    
    # Remove dangling images
    docker image prune -f
    
    # Remove mlchallenge images if requested
    if [ "$1" = "--all" ]; then
        local mlchallenge_images=$(docker images "mlchallenge/*" -q)
        if [ ! -z "$mlchallenge_images" ]; then
            docker rmi -f $mlchallenge_images
            log_info "Removed mlchallenge images"
        fi
    fi
}

cleanup_volumes() {
    log_info "Cleaning up Docker volumes..."
    docker volume prune -f
}

cleanup_networks() {
    log_info "Cleaning up Docker networks..."
    docker network prune -f
}

cleanup_build_cache() {
    log_info "Cleaning up Docker build cache..."
    docker builder prune -f
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --all           Remove all mlchallenge images too"
    echo "  --volumes       Clean up volumes only"
    echo "  --images        Clean up images only"
    echo "  --containers    Clean up containers only"
    echo "  --everything    Nuclear option - clean everything"
    echo "  -h, --help      Show this help"
}

main() {
    case ${1:-} in
        --all)
            cleanup_containers
            cleanup_images --all
            cleanup_volumes
            cleanup_networks
            cleanup_build_cache
            ;;
        --volumes)
            cleanup_volumes
            ;;
        --images)
            cleanup_images
            ;;
        --containers)
            cleanup_containers
            ;;
        --everything)
            log_warn "This will remove EVERYTHING Docker-related. Are you sure? (y/N)"
            read -r response
            if [[ "$response" =~ ^[Yy]$ ]]; then
                cleanup_containers
                cleanup_images --all
                cleanup_volumes  
                cleanup_networks
                cleanup_build_cache
                docker system prune -a -f --volumes
                log_info "Nuclear cleanup completed!"
            else
                log_info "Cleanup cancelled"
            fi
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        "")
            # Default cleanup
            cleanup_containers
            cleanup_images
            cleanup_volumes
            cleanup_networks
            ;;
        *)
            log_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
    
    log_info "Docker cleanup completed!"
    
    # Show disk space freed
    log_info "Current Docker disk usage:"
    docker system df
}

main "$@"