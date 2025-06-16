# scripts/setup/setup_project.py
"""
Project Setup Script
Initializes the project structure and configuration files.
"""

import os
import json
from pathlib import Path
from datetime import datetime

class ProjectSetup:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        
        # Directory structure
        self.directories = [
            "api",
            "api/routers",
            "api/models", 
            "api/services",
            "api/middleware",
            "api/utils",
            "models",
            "models/training",
            "models/artifacts",
            "models/configs",
            "tests",
            "tests/unit",
            "tests/integration", 
            "tests/e2e",
            "scripts",
            "scripts/setup",
            "scripts/docker",
            "scripts/monitoring",
            "monitoring",
            "monitoring/prometheus",
            "monitoring/grafana",
            "docs",
            "data",
            "logs"
        ]
        
        # Configuration files
        self.config_files = {
            "api/config.py": self.generate_api_config(),
            "models/model_config.yaml": self.generate_model_config(),
            "monitoring/prometheus/prometheus.yml": self.generate_prometheus_config(),
            "pytest.ini": self.generate_pytest_config(),
            ".env.example": self.generate_env_example(),
            "requirements.txt": self.generate_requirements(),
            ".gitignore": self.generate_gitignore()
        }

    def create_directories(self):
        """Create project directory structure."""
        for directory in self.directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py for Python packages
            if directory.startswith(("api", "models", "tests")):
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
        
        print(f"Created {len(self.directories)} directories")

    def create_config_files(self):
        """Create configuration files."""
        for filepath, content in self.config_files.items():
            file_path = self.project_root / filepath
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    f.write(content)
        
        print(f"Created {len(self.config_files)} configuration files")

    def generate_api_config(self):
        return '''"""API Configuration Module"""
import os
from typing import List

class Settings:
    # API Configuration
    API_TITLE: str = "ML Engineer Challenge API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/mlchallenge")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Model Configuration
    MODEL_CACHE_TTL: int = 3600  # 1 hour
    MAX_BATCH_SIZE: int = 32
    
    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]

settings = Settings()
'''

    def generate_model_config(self):
        return '''# Model Configuration
models:
  classification:
    name: "efficientnet_b0"
    input_size: [224, 224]
    num_classes: 100
    batch_size: 32
    device: "cuda"
    
  detection:
    name: "yolov5s"
    input_size: [640, 640]
    confidence_threshold: 0.5
    iou_threshold: 0.45
    
  similarity:
    name: "clip_vit_b32"
    input_size: [224, 224]
    embedding_dim: 512

optimization:
  quantization:
    enabled: true
    method: "dynamic"
  
  pruning:
    enabled: false
    sparsity: 0.2
  
  tensorrt:
    enabled: false
    precision: "fp16"
'''

    def generate_prometheus_config(self):
        return '''global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ml-api'
    static_configs:
      - targets: ['ml-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
'''

    def generate_pytest_config(self):
        return '''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --strict-config
    --cov=api
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=85

markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
'''

    def generate_env_example(self):
        return '''# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/mlchallenge

# Redis Configuration  
REDIS_URL=redis://localhost:6379

# API Configuration
SECRET_KEY=your-secret-key-here
DEBUG=true
LOG_LEVEL=INFO

# Model Configuration
MODEL_CACHE_DIR=/app/models/cache
GPU_ENABLED=true

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ADMIN_PASSWORD=admin
'''

    def generate_requirements(self):
        return '''# Core ML Libraries
torch>=2.0.0
torchvision>=0.15.0
transformers>=4.20.0
onnx>=1.14.0
onnxruntime>=1.15.0

# API Framework
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0

# Database & Cache
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
redis>=4.5.0
alembic>=1.11.0

# Background Tasks
celery>=5.3.0

# Monitoring & Logging
prometheus-client>=0.17.0
structlog>=23.1.0

# Image Processing
Pillow>=10.0.0
opencv-python>=4.8.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
httpx>=0.24.0

# Development
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.5.0

# Utilities
python-multipart>=0.0.6
python-dotenv>=1.0.0
requests>=2.31.0
tqdm>=4.65.0
'''

    def generate_gitignore(self):
        return '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project Specific
data/
logs/
models/artifacts/
*.log
.env
.coverage
htmlcov/

# Docker
.dockerignore

# Model files
*.pth
*.onnx
*.trt
*.bin
'''

    def setup_project(self):
        """Run complete project setup."""
        print("Setting up ML Engineer Challenge project...")
        self.create_directories()
        self.create_config_files()
        print("Project setup complete!")
        print("\nNext steps:")
        print("1. Copy .env.example to .env and configure")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Download datasets: python scripts/setup/download_datasets.py")
        print("4. Start development: docker-compose up -d")

if __name__ == "__main__":
    setup = ProjectSetup()
    setup.setup_project()