# scripts/utils/logging_config.py
"""
Structured Logging Configuration for ML Challenge
"""

import logging
import logging.config
import structlog
import sys
import uuid
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

class CorrelationIDProcessor:
    """Add correlation ID to log entries."""
    
    def __init__(self):
        self.correlation_id = None
    
    def set_correlation_id(self, correlation_id: str):
        """Set correlation ID for current context."""
        self.correlation_id = correlation_id
    
    def generate_correlation_id(self) -> str:
        """Generate new correlation ID."""
        self.correlation_id = str(uuid.uuid4())[:8]
        return self.correlation_id
    
    def __call__(self, logger, method_name, event_dict):
        """Add correlation ID to event dict."""
        if self.correlation_id:
            event_dict['correlation_id'] = self.correlation_id
        return event_dict

# Global correlation ID processor
correlation_processor = CorrelationIDProcessor()

def add_request_id(logger, method_name, event_dict):
    """Add request ID if available."""
    # This would typically get the request ID from context
    # For now, generate one if not present
    if 'request_id' not in event_dict and 'correlation_id' not in event_dict:
        event_dict['correlation_id'] = correlation_processor.generate_correlation_id()
    return event_dict

def add_service_context(logger, method_name, event_dict):
    """Add service context information."""
    event_dict.update({
        'service': 'ml-challenge-api',
        'version': '1.0.0',
        'environment': 'development'  # This should come from config
    })
    return event_dict

def configure_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    log_file: str = None,
    enable_structlog: bool = True
) -> None:
    """Configure application logging."""
    
    # Ensure logs directory exists
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configure standard logging
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
                'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
            },
            'verbose': {
                'format': '{asctime} {name} {levelname} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {name}: {message}',
                'style': '{',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': log_format,
                'stream': sys.stdout
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console'],
                'level': log_level,
                'propagate': False
            },
            'uvicorn': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False
            },
            'uvicorn.access': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False
            }
        }
    }
    
    # Add file handler if specified
    if log_file:
        logging_config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_file,
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': log_format
        }
        # Add file handler to all loggers
        for logger_config in logging_config['loggers'].values():
            logger_config['handlers'].append('file')
    
    logging.config.dictConfig(logging_config)
    
    # Configure structlog if enabled
    if enable_structlog:
        configure_structlog(log_level)

def configure_structlog(log_level: str = "INFO") -> None:
    """Configure structured logging with structlog."""
    
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            add_service_context,
            correlation_processor,
            add_request_id,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )

class MLLogger:
    """Enhanced logger for ML operations."""
    
    def __init__(self, name: str):
        self.logger = structlog.get_logger(name)
        self.name = name
    
    def log_model_inference(self, 
                           model_name: str,
                           input_shape: tuple,
                           inference_time: float,
                           success: bool = True,
                           error: str = None):
        """Log model inference details."""
        log_data = {
            'event': 'model_inference',
            'model_name': model_name,
            'input_shape': input_shape,
            'inference_time_ms': inference_time * 1000,
            'success': success
        }
        
        if error:
            log_data['error'] = error
            self.logger.error("Model inference failed", **log_data)
        else:
            self.logger.info("Model inference completed", **log_data)
    
    def log_api_request(self, 
                       endpoint: str, 
                       method: str, 
                       status_code: int,
                       response_time: float,
                       user_id: str = None):
        """Log API request details."""
        self.logger.info(
            "API request processed",
            event='api_request',
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time_ms=response_time * 1000,
            user_id=user_id
        )
    
    def log_batch_job(self, 
                     job_id: str,
                     job_type: str,
                     items_processed: int,
                     duration: float,
                     success: bool = True):
        """Log batch job execution."""
        self.logger.info(
            "Batch job completed",
            event='batch_job',
            job_id=job_id,
            job_type=job_type,
            items_processed=items_processed,
            duration_seconds=duration,
            success=success
        )
    
    def log_model_metrics(self, 
                         model_name: str, 
                         metrics: Dict[str, Any]):
        """Log model performance metrics."""
        self.logger.info(
            "Model metrics updated",
            event='model_metrics',
            model_name=model_name,
            **metrics
        )

def get_logger(name: str) -> MLLogger:
    """Get an ML logger instance."""
    return MLLogger(name)

# Usage examples and testing
if __name__ == "__main__":
    # Configure logging
    configure_logging(
        log_level="INFO",
        log_format="json",
        log_file="logs/ml-challenge.log"
    )
    
    # Test the logger
    logger = get_logger("test")
    
    # Set correlation ID
    correlation_processor.set_correlation_id("test-123")
    
    # Test different log types
    logger.log_model_inference(
        model_name="efficientnet_b0",
        input_shape=(1, 3, 224, 224),
        inference_time=0.045,
        success=True
    )
    
    logger.log_api_request(
        endpoint="/api/v1/classify",
        method="POST",
        status_code=200,
        response_time=0.123,
        user_id="user123"
    )
    
    logger.log_batch_job(
        job_id="batch-456",
        job_type="image_classification",
        items_processed=100,
        duration=45.2,
        success=True
    )
    
    logger.log_model_metrics(
        model_name="efficientnet_b0",
        metrics={
            "accuracy": 0.95,
            "f1_score": 0.87,
            "precision": 0.92,
            "recall": 0.83
        }
    )
    
    print("Logging configuration and test completed!")