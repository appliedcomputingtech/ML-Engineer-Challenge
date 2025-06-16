# scripts/docker/health_check.py
"""
Generic Health Check Script for Docker Containers
"""

import sys
import time
import requests
import psycopg2
import redis
from pathlib import Path

class HealthChecker:
    def __init__(self):
        self.checks = {
            'api': self.check_api_health,
            'database': self.check_database_health, 
            'redis': self.check_redis_health,
            'models': self.check_models_health
        }

    def check_api_health(self):
        """Check if API is responding."""
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def check_database_health(self):
        """Check database connectivity."""
        try:
            conn = psycopg2.connect(
                host="postgres",
                database="mlchallenge", 
                user="user",
                password="password",
                connect_timeout=5
            )
            conn.close()
            return True
        except psycopg2.Error:
            return False

    def check_redis_health(self):
        """Check Redis connectivity."""
        try:
            r = redis.Redis(host='redis', port=6379, socket_connect_timeout=5)
            r.ping()
            return True
        except redis.RedisError:
            return False

    def check_models_health(self):
        """Check if models are loaded."""
        model_dir = Path("/app/models/artifacts")
        required_models = ["classification.pth", "detection.pth", "similarity.pth"]
        
        return all((model_dir / model).exists() for model in required_models)

    def run_health_check(self, service_type):
        """Run health check for specific service."""
        if service_type not in self.checks:
            print(f"Unknown service type: {service_type}")
            return False
        
        max_retries = 30
        retry_delay = 2
        
        for attempt in range(max_retries):
            if self.checks[service_type]():
                print(f"{service_type} health check passed")
                return True
            
            print(f"{service_type} health check failed (attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay)
        
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python health_check.py <service_type>")
        print("Service types: api, database, redis, models")
        sys.exit(1)
    
    service_type = sys.argv[1]
    checker = HealthChecker()
    
    if checker.run_health_check(service_type):
        sys.exit(0)
    else:
        print(f"Health check failed for {service_type}")
        sys.exit(1)