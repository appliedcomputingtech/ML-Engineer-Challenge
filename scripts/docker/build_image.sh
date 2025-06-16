#!/bin/bash
# scripts/docker/build_images.sh
# Docker image build automation script

set -e  # Exit on any error

# Configuration
REGISTRY_PREFIX="mlchallenge"
BUILD_ARGS=""
DOCKER_FILE_DIR="."
PARALLEL_BUILDS=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to build a single image
build_image() {
    local service_name=$1
    local dockerfile_path=$2
    local context_path=$3
    local image_tag="${REGISTRY_PREFIX}/${service_name}:latest"
    
    log_info "Building image: $image_tag"
    log_info "Dockerfile: $dockerfile_path"
    log_info "Context: $context_path"
    
    # Build with build cache and multi-stage optimization
    docker build \
        --file "$dockerfile_path" \
        --tag "$image_tag" \
        --tag "${REGISTRY_PREFIX}/${service_name}:$(date +%Y%m%d-%H%M%S)" \
        $BUILD_ARGS \
        "$context_path"
    
    if [ $? -eq 0 ]; then
        log_info "Successfully built: $image_tag"
        # Show image size
        local size=$(docker images "$image_tag" --format "{{.Size}}")
        log_info "Image size: $size"
    else
        log_error "Failed to build: $image_tag"
        return 1
    fi
}

# Function to build all images
build_all_images() {
    local services=(
        "ml-api:docker/Dockerfile.api:."
        "worker:docker/Dockerfile.worker:."
        "nginx:docker/Dockerfile.nginx:./nginx"
    )
    
    if [ "$PARALLEL_BUILDS" = true ]; then
        log_info "Building images in parallel..."
        for service_config in "${services[@]}"; do
            IFS=':' read -r service dockerfile context <<< "$service_config"
            build_image "$service" "$dockerfile" "$context" &
        done
        wait  # Wait for all background jobs
    else
        log_info "Building images sequentially..."
        for service_config in "${services[@]}"; do
            IFS=':' read -r service dockerfile context <<< "$service_config"
            build_image "$service" "$dockerfile" "$context"
        done
    fi
}

# Function to cleanup old images
cleanup_old_images() {
    log_info "Cleaning up old images..."
    
    # Remove dangling images
    docker image prune -f
    
    # Remove old tagged images (keep last 3)
    for service in ml-api worker nginx; do
        local old_images=$(docker images "${REGISTRY_PREFIX}/${service}" --format "{{.Repository}}:{{.Tag}}" | tail -n +4)
        if [ ! -z "$old_images" ]; then
            echo "$old_images" | xargs docker rmi -f 2>/dev/null || true
        fi
    done
}

# Function to run security scan
security_scan() {
    local image=$1
    log_info "Running security scan on: $image"
    
    # Use docker scout or trivy if available
    if command -v trivy &> /dev/null; then
        trivy image "$image"
    elif docker scout version &> /dev/null; then
        docker scout quickview "$image"
    else
        log_warn "No security scanner found. Install trivy or docker scout for security scanning."
    fi
}

# Function to test images
test_images() {
    log_info "Testing built images..."
    
    # Test API image
    log_info "Testing ml-api image..."
    docker run --rm "${REGISTRY_PREFIX}/ml-api:latest" python -c "import torch; print('PyTorch version:', torch.__version__)"
    
    # Test worker image  
    log_info "Testing worker image..."
    docker run --rm "${REGISTRY_PREFIX}/worker:latest" python -c "import celery; print('Celery version:', celery.__version__)"
    
    log_info "All image tests passed!"
}

# Parse command line arguments
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -s, --service SERVICE    Build specific service (ml-api, worker, nginx)"
    echo "  -p, --parallel          Build images in parallel"
    echo "  -c, --cleanup           Cleanup old images after build"
    echo "  -t, --test              Test images after build"
    echo "  --security-scan         Run security scan on built images"
    echo "  --build-arg ARG=VALUE   Pass build argument to docker build"
    echo "  -h, --help              Show this help message"
}

# Main script
main() {
    local specific_service=""
    local cleanup_after=false  
    local test_after=false
    local security_scan_after=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -s|--service)
                specific_service="$2"
                shift 2
                ;;
            -p|--parallel)
                PARALLEL_BUILDS=true
                shift
                ;;
            -c|--cleanup)
                cleanup_after=true
                shift
                ;;
            -t|--test)
                test_after=true
                shift
                ;;
            --security-scan)
                security_scan_after=true
                shift
                ;;
            --build-arg)
                BUILD_ARGS="$BUILD_ARGS --build-arg $2"
                shift 2
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    log_info "Starting Docker image build process..."
    log_info "Registry prefix: $REGISTRY_PREFIX"
    
    # Build specific service or all services
    if [ ! -z "$specific_service" ]; then
        case $specific_service in
            ml-api)
                build_image "ml-api" "docker/Dockerfile.api" "."
                ;;
            worker)
                build_image "worker" "docker/Dockerfile.worker" "."
                ;;
            nginx)
                build_image "nginx" "docker/Dockerfile.nginx" "./nginx"
                ;;
            *)
                log_error "Unknown service: $specific_service"
                exit 1
                ;;
        esac
    else
        build_all_images
    fi
    
    # Post-build actions
    if [ "$test_after" = true ]; then
        test_images
    fi
    
    if [ "$security_scan_after" = true ]; then
        for service in ml-api worker nginx; do
            security_scan "${REGISTRY_PREFIX}/${service}:latest"
        done
    fi
    
    if [ "$cleanup_after" = true ]; then
        cleanup_old_images
    fi
    
    log_info "Build process completed successfully!"
    
    # Show final image list
    log_info "Built images:"
    docker images "${REGISTRY_PREFIX}/*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
}

# Check if docker is available
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed or not in PATH"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    log_error "Docker daemon is not running"
    exit 1
fi

# Run main function
main "$@"