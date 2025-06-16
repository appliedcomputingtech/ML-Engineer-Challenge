# scripts/testing/test_helpers.py
"""
Common test utilities and fixtures
"""

import pytest
import torch
import numpy as np
from PIL import Image
from io import BytesIO
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def sample_image():
    """Generate a sample image for testing."""
    # Create a simple RGB image
    image = Image.new('RGB', (224, 224), color='red')
    return image

@pytest.fixture
def sample_image_bytes():
    """Generate sample image as bytes."""
    image = Image.new('RGB', (224, 224), color='blue')
    img_bytes = BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

@pytest.fixture
def sample_batch_tensor():
    """Generate a sample batch tensor."""
    return torch.randn(4, 3, 224, 224)

@pytest.fixture
def temp_model_dir():
    """Create temporary directory for model testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_model_predictions():
    """Mock model prediction responses."""
    return {
        'classification': {
            'class_id': 42,
            'class_name': 'test_class',
            'confidence': 0.95,
            'probabilities': [0.1, 0.2, 0.95, 0.05]
        },
        'detection': {
            'boxes': [[10, 10, 100, 100]],
            'labels': ['person'],
            'scores': [0.9]
        },
        'similarity': {
            'embedding': np.random.rand(512).tolist(),
            'similar_images': [
                {'image_id': 'img1', 'similarity': 0.95},
                {'image_id': 'img2', 'similarity': 0.87}
            ]
        }
    }

class MockModel:
    """Mock model for testing."""
    
    def __init__(self, model_type="classification"):
        self.model_type = model_type
        self.device = "cpu"
    
    def __call__(self, x):
        if self.model_type == "classification":
            batch_size = x.shape[0] if hasattr(x, 'shape') else 1
            return torch.randn(batch_size, 100)  # 100 classes
        elif self.model_type == "detection":
            return {
                'boxes': torch.tensor([[10, 10, 100, 100]]),
                'labels': torch.tensor([1]),
                'scores': torch.tensor([0.9])
            }
        elif self.model_type == "similarity":
            batch_size = x.shape[0] if hasattr(x, 'shape') else 1
            return torch.randn(batch_size, 512)  # 512-dim embeddings
    
    def eval(self):
        return self
    
    def to(self, device):
        self.device = device
        return self

@pytest.fixture
def mock_classification_model():
    return MockModel("classification")

@pytest.fixture
def mock_detection_model():
    return MockModel("detection")

@pytest.fixture
def mock_similarity_model():
    return MockModel("similarity")

def create_test_database():
    """Create test database tables."""
    # This would contain SQL commands to set up test tables
    # Implementation depends on your database choice
    pass

def cleanup_test_database():
    """Clean up test database."""
    pass

def assert_image_valid(image_data, min_size=(224, 224)):
    """Assert that image data is valid."""
    if isinstance(image_data, bytes):
        image = Image.open(BytesIO(image_data))
    else:
        image = image_data
    
    assert image.size[0] >= min_size[0]
    assert image.size[1] >= min_size[1]
    assert image.mode in ['RGB', 'RGBA']

def assert_tensor_shape(tensor, expected_shape):
    """Assert tensor has expected shape."""
    assert isinstance(tensor, torch.Tensor)
    assert tensor.shape == expected_shape

def assert_api_response_valid(response, expected_keys=None):
    """Assert API response is valid."""
    assert response.status_code == 200
    data = response.json()
    
    if expected_keys:
        for key in expected_keys:
            assert key in data
    
    return data

# Utility functions for generating test data
def generate_random_image(size=(224, 224), format='RGB'):
    """Generate random image for testing."""
    if format == 'RGB':
        array = np.random.randint(0, 256, (size[1], size[0], 3), dtype=np.uint8)
    else:
        array = np.random.randint(0, 256, size, dtype=np.uint8)
    
    return Image.fromarray(array, format)

def generate_test_dataset(num_samples=100, size=(224, 224)):
    """Generate test dataset."""
    images = []
    labels = []
    
    for i in range(num_samples):
        image = generate_random_image(size)
        label = i % 10  # 10 classes
        images.append(image)
        labels.append(label)
    
    return images, labels

if __name__ == "__main__":
    # Test the utilities
    image = generate_random_image()
    assert_image_valid(image)
    print("Test utilities working correctly!")