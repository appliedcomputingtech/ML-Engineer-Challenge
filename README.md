# Machine Learning Engineer Challenge
## Production-Ready MLOps System

Welcome to the ML Engineer challenge at Applied Computing! This is designed to test your skills in building production-ready ML systems that go beyond just model development. You'll be building a complete MLOps pipeline with containerisation, testing, monitoring, and deployment capabilities.

## 🎯 Challenge Overview

You will build a **Multi-Model Computer Vision API** that serves different models for image classification, object detection, and image similarity search. The system must be production-ready with proper testing, monitoring, containerisation, and scalability.

---

## 📋 System Requirements

### Core Architecture
- **Multi-service architecture** using Docker Compose
- **API Gateway** with rate limiting and authentication
- **Model serving service** with multiple model endpoints
- **Background job processing** for batch inference
- **Redis cache** for results and model metadata
- **PostgreSQL database** for storing inference logs and metrics
- **Monitoring stack** with Prometheus and Grafana (optional but preferred)

---

## 🚀 Part 1: Model Development & Optimisation

### Objective
Build a multi-model system that can handle different computer vision tasks with advanced optimisation techniques. **Note** You don't have to build a new architecture, feel free to utilise any pre-built architecture to get your outputs.

### Requirements

1. **Model Selection & Training**
   - Utilise **3 different models**:
     - Image Classification (ViT / ResNet / EfficientNet etc. on CIFAR-100)
     - Object Detection (YOLO / DETR etc. on COCO subset)
   - **For Image classification only**: fine-tune the model with the following techniques: mixed precision, gradient clipping, learning rate scheduling. Use the [tiny-ImageNet dataset](https://www.kaggle.com/datasets/akash2sharma/tiny-imagenet) for this. To download the dataset, use the following utility script:
    ```shell
    python ./scripts/download_datasets.py
    ```
   - Implement custom data augmentation pipeline

2. **Model Optimisation**
   - Apply **quantization** (INT8) to all models
   - Convert models to **ONNX** and **TensorRT** formats
   - Benchmark inference times across all formats

3. **Model Validation**
   - Implement comprehensive model validation pipeline
   - A/B testing framework for model comparison
   - Model drift detection using statistical tests
   - Performance regression testing

### Deliverables
- `models/` directory with training scripts and model artifacts
- `benchmarks/` directory with performance comparison reports
- Comprehensive model cards with metrics and limitations

---

## 🏗️ Part 2: Production API Development

### Objective
Build a robust, scalable API system for serving ML models with proper error handling, validation, and monitoring.

### Requirements

1. **FastAPI Application Structure**
   ```
   api/
   ├── main.py
   ├── routers/
   │   ├── classification.py
   │   └── detection.py
   ├── models/
   │   ├── schemas.py
   │   └── responses.py
   ├── services/
   │   ├── model_service.py
   │   ├── cache_service.py
   │   └── inference_service.py
   ├── middleware/
   │   ├── auth.py
   │   ├── rate_limit.py
   │   └── monitoring.py
   └── utils/
       ├── image_processing.py
       └── validators.py
   ```

2. **API Endpoints**
   - `POST /api/v1/classify` - Image classification
   - `POST /api/v1/detect` - Object detection
   - `POST /api/v1/batch` - Batch processing endpoint
   - `GET /api/v1/models` - Model metadata and health
   - `GET /api/v1/health` - System health check
   - `GET /api/v1/metrics` - Prometheus metrics endpoint

3. **Advanced Features**
   - **Rate limiting**: Different limits per user tier
   - **Input validation**: Comprehensive image validation (size, format, content)
   - **Async processing**: Background jobs for large batch requests
   - **Model versioning**: Support for multiple model versions
   - **Graceful degradation**: Fallback mechanisms when models fail

4. **Error Handling & Logging**
   - Structured logging with correlation IDs
   - Custom exception handling with user-friendly messages
   - Request/response logging for debugging
   - Performance monitoring and alerting

### Deliverables
- Complete FastAPI application with all endpoints
- Comprehensive API documentation (auto-generated + custom)
- Postman collection or OpenAPI spec for testing

---

## 🧪 Part 3: Comprehensive Testing Strategy

### Objective
Implement a complete testing pyramid with unit, integration, and end-to-end tests.

### Requirements

1. **Unit Tests** (target: >90% coverage)
   - Model inference functions
   - Image preprocessing utilities
   - API route handlers
   - Service layer functions
   - Mock external dependencies

2. **Integration Tests**
   - Database operations
   - Model loading and inference
   - API endpoint integration

3. **Performance Tests**
   - Stress testing for model inference
   - Memory usage profiling

4. **Test Infrastructure**
   - Pytest configuration with fixtures
   - Test database setup/teardown
   - Mock services for external dependencies
   - Continuous testing with GitHub Actions or similar

### Deliverables
- `tests/` directory with complete test suite
- Test configuration and fixtures
- Performance test reports
- CI/CD pipeline configuration

---

## 🐳 Part 4: Containerisation & Orchestration

### Objective
Create a production-ready containerised system with proper orchestration.

### Requirements

1. **Docker Images**
   - **Multi-stage builds** for optimal image size
   - **Security best practices** (non-root user, minimal base images)
   - **Optimized for caching** layers
   - Separate images for different services

2. **Docker Compose Setup**
   ```yaml
   services:
     api-gateway:     # Nginx or Traefik
     ml-api:          # FastAPI application
     worker:          # Celery worker for background jobs
     redis:           # Cache and message broker
     postgres:        # Database
     prometheus:      # Metrics collection
     grafana:         # Monitoring dashboard (optional)
   ```

3. **Service Configuration**
   - Environment-based configuration
   - Health checks for all services
   - Proper resource limits
   - Volume management for persistent data
   - Network configuration and service discovery

### Deliverables
- `Dockerfile` for each service
- `docker-compose.yml` for local development
- `docker-compose.prod.yml` for production
- Documentation for deployment and scaling

---

## 📝 Submission Requirements

### Code Organization
```
ml-engineer-challenge/
├── README.md                 # Complete setup and usage guide
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Service orchestration
├── Dockerfile               # Main application container
├── api/                     # FastAPI application
├── models/                  # Model training and artifacts
├── tests/                   # Complete test suite
├── monitoring/              # Prometheus, Grafana configs
├── scripts/                 # Utility scripts
├── docs/                    # Additional documentation
└── .github/workflows/       # CI/CD pipeline
```

### Documentation Requirements
1. **README.md** with:
   - Architecture overview and design decisions
   - Setup and installation instructions
   - API usage examples
   - Performance benchmarks
   - Known limitations and future improvements

2. **API Documentation**
   - Complete endpoint documentation
   - Request/response examples
   - Error handling guide
   - Authentication guide

3. **Technical ReadMe.md** (PDF or Markdown):
   - Model selection and optimization rationale
   - Performance benchmarking results
   - System architecture decisions
   - Scalability considerations

### Quality Standards
- **Code Quality**: PEP 8 compliance, type hints, docstrings
- **Test Coverage**: Minimum 85% for critical paths
- **Documentation**: Comprehensive and clear
- **Performance**: Sub-second inference for single images
- **Security**: No hardcoded secrets, proper input validation
- **Scalability**: Design for horizontal scaling

---

## 🏆 Evaluation Criteria

### Technical Excellence (30%)
- Code quality, architecture, and best practices
- Model optimization and performance
- System scalability and reliability
- Testing coverage and quality

### Production Readiness (30%)
- Containerization and orchestration
- Monitoring and observability
- Error handling and resilience

### ML Engineering Skills (30%)
- Model selection and optimization
- Performance benchmarking
- MLOps pipeline design
- Technical depth and innovation

### Communication (10%)
- Documentation clarity
- Code readability
- Technical explanations
- Design decision rationale

---

## 🚀 Getting Started

1. **Set up your development environment**
   ```bash
   git clone <your-repo>
   cd ml-engineer-challenge
   pip install -r requirements.txt
   ```

2. **Download required datasets**
   ```bash
    # Download just tiny ImageNet
    python scripts/setup/download_datasets.py --dataset tiny_imagenet

    # Download all datasets (including tiny ImageNet)
    python scripts/setup/download_datasets.py --dataset all

    # Specify custom data directory
    python scripts/setup/download_datasets.py --dataset tiny_imagenet --data-dir /custom/path
   ```

3. **Start the development stack**
   ```bash
   docker-compose up -d
   ```

4. **Run the test suite**
   ```bash
   pytest tests/ -v --cov=api
   ```




Good luck! This challenge will test your ability to build production-ready ML systems. Focus on creating a system that could actually be deployed and maintained in a real production environment.

**Questions?** Feel free to make reasonable assumptions and document them in your README. We're looking for engineering judgment as much as technical skills.


