# scripts/testing/load_test.py
"""
Load Testing Script for ML API
Using locust for load testing with realistic ML workloads
"""

import time
import random
import io
import base64
from PIL import Image
from locust import HttpUser, task, between
import json

class MLAPIUser(HttpUser):
    """Simulate user behavior for ML API load testing."""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Setup for each user session."""
        # Generate test images of different sizes
        self.test_images = self.generate_test_images()
        
        # Authenticate user (if auth is implemented)
        self.authenticate()
    
    def generate_test_images(self):
        """Generate test images for different scenarios."""
        images = {}
        
        # Small image
        small_img = Image.new('RGB', (224, 224), color=(255, 0, 0))
        images['small'] = self.image_to_base64(small_img)
        
        # Medium image
        medium_img = Image.new('RGB', (512, 512), color=(0, 255, 0))
        images['medium'] = self.image_to_base64(medium_img)
        
        # Large image
        large_img = Image.new('RGB', (1024, 1024), color=(0, 0, 255))
        images['large'] = self.image_to_base64(large_img)
        
        return images
    
    def image_to_base64(self, image):
        """Convert PIL image to base64 string."""
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode()
    
    def authenticate(self):
        """Authenticate user if required."""
        # Mock authentication - replace with actual auth logic
        login_data = {
            "username": f"user_{random.randint(1, 1000)}",
            "password": "testpassword"
        }
        
        response = self.client.post("/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            self.client.headers.update({"Authorization": f"Bearer {token}"})
    
    @task(5)  # Weight: 5 (most common operation)
    def classify_image(self):
        """Test image classification endpoint."""
        image_size = random.choice(['small', 'medium', 'large'])
        image_data = self.test_images[image_size]
        
        payload = {
            "image": image_data,
            "model": "efficientnet_b0"
        }
        
        with self.client.post(
            "/api/v1/classify",
            json=payload,
            name=f"classify_{image_size}",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                result = response.json()
                if 'class_id' in result and 'confidence' in result:
                    response.success()
                else:
                    response.failure("Missing required fields in response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(3)  # Weight: 3
    def detect_objects(self):
        """Test object detection endpoint."""
        image_size = random.choice(['medium', 'large'])  # Detection works better on larger images
        image_data = self.test_images[image_size]
        
        payload = {
            "image": image_data,
            "model": "yolov5s",
            "confidence_threshold": 0.5
        }
        
        with self.client.post(
            "/api/v1/detect",
            json=payload,
            name=f"detect_{image_size}",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                result = response.json()
                if 'detections' in result:
                    response.success()
                else:
                    response.failure("Missing detections in response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)  # Weight: 2
    def similarity_search(self):
        """Test similarity search endpoint."""
        image_size = random.choice(['small', 'medium'])
        image_data = self.test_images[image_size]
        
        payload = {
            "image": image_data,
            "model": "clip_vit_b32",
            "top_k": 5
        }
        
        with self.client.post(
            "/api/v1/similarity",
            json=payload,
            name=f"similarity_{image_size}",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                result = response.json()
                if 'similar_images' in result:
                    response.success()
                else:
                    response.failure("Missing similar_images in response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)  # Weight: 1 (least common)
    def batch_inference(self):
        """Test batch inference endpoint."""
        # Create batch of small images
        batch_images = [self.test_images['small'] for _ in range(random.randint(2, 5))]
        
        payload = {
            "images": batch_images,
            "model": "efficientnet_b0",
            "task": "classification"
        }
        
        with self.client.post(
            "/api/v1/batch",
            json=payload,
            name="batch_inference",
            catch_response=True
        ) as response:
            if response.status_code == 202:  # Async processing
                job_id = response.json().get("job_id")
                if job_id:
                    response.success()
                    # Optionally check job status
                    self.check_batch_status(job_id)
                else:
                    response.failure("Missing job_id in response")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    def check_batch_status(self, job_id):
        """Check status of batch job."""
        with self.client.get(
            f"/api/v1/batch/{job_id}/status",
            name="batch_status",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                status = response.json().get("status")
                if status in ["pending", "processing", "completed", "failed"]:
                    response.success()
                else:
                    response.failure(f"Unknown status: {status}")
    
    @task(1)
    def health_check(self):
        """Test health check endpoint."""
        with self.client.get("/api/v1/health", name="health_check") as response:
            if response.status_code == 200:
                response.success()
    
    @task(1)
    def get_model_info(self):
        """Test model info endpoint."""
        with self.client.get("/api/v1/models", name="model_info") as response:
            if response.status_code == 200:
                response.success()

class StressTestUser(HttpUser):
    """Stress testing with aggressive load patterns."""
    
    wait_time = between(0.1, 0.5)  # Very short wait times
    
    def on_start(self):
        # Generate larger test images
        large_img = Image.new('RGB', (2048, 2048), color=(128, 128, 128))
        buffer = io.BytesIO()
        large_img.save(buffer, format='JPEG')
        buffer.seek(0)
        self.large_image = base64.b64encode(buffer.getvalue()).decode()
    
    @task
    def stress_classify(self):
        """Stress test classification with large images."""
        payload = {
            "image": self.large_image,
            "model": "efficientnet_b0"
        }
        
        self.client.post("/api/v1/classify", json=payload, name="stress_classify")

# Custom load test scenarios
class LoadTestScenarios:
    """Different load testing scenarios."""
    
    @staticmethod
    def run_peak_traffic_test():
        """Simulate peak traffic conditions."""
        import subprocess
        import os
        
        # Run locust with specific parameters for peak traffic
        cmd = [
            "locust",
            "-f", __file__,
            "--users", "100",
            "--spawn-rate", "10",
            "--run-time", "300s",  # 5 minutes
            "--host", "http://localhost:8000",
            "--html", "reports/peak_traffic_report.html"
        ]
        
        subprocess.run(cmd)
    
    @staticmethod
    def run_endurance_test():
        """Run long-duration test to check for memory leaks."""
        import subprocess
        
        cmd = [
            "locust",
            "-f", __file__,
            "--users", "50",
            "--spawn-rate", "5",
            "--run-time", "1800s",  # 30 minutes
            "--host", "http://localhost:8000",
            "--html", "reports/endurance_report.html"
        ]
        
        subprocess.run(cmd)
    
    @staticmethod
    def run_stress_test():
        """Run stress test to find breaking point."""
        import subprocess
        
        cmd = [
            "locust",
            "-f", __file__,
            "--users", "200",
            "--spawn-rate", "20",
            "--run-time", "600s",  # 10 minutes
            "--host", "http://localhost:8000",
            "--html", "reports/stress_test_report.html",
            "--user-classes", "StressTestUser"
        ]
        
        subprocess.run(cmd)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run ML API load tests")
    parser.add_argument("--scenario", choices=["peak", "endurance", "stress"], 
                       default="peak", help="Load test scenario")
    
    args = parser.parse_args()
    
    scenarios = LoadTestScenarios()
    
    if args.scenario == "peak":
        scenarios.run_peak_traffic_test()
    elif args.scenario == "endurance":
        scenarios.run_endurance_test()
    elif args.scenario == "stress":
        scenarios.run_stress_test()
    
    print(f"Load test scenario '{args.scenario}' completed!")
    print("Check the reports/ directory for detailed results.")