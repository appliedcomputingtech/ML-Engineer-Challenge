# Example usage and model metadata structure
from scripts.models.model_registry import ModelRegistry
from typing import Dict, Any


if __name__ == "__main__":
    registry = ModelRegistry()
    
    # Example of registering a model
    registry.register_model(
        name="efficientnet_classification",
        version="v1.0.0",
        model_path="models/artifacts/efficientnet_b0.pth",
        model_type="classification",
        metrics={
            "accuracy": 0.85,
            "f1_score": 0.83,
            "inference_time_ms": 45.2
        },
        metadata={
            "architecture": "EfficientNet-B0",
            "input_shape": [3, 224, 224],
            "num_classes": 100,
            "optimizer": "AdamW",
            "learning_rate": 0.001,
            "training_epochs": 50
        }
    )
    
    # List all models
    print("Registered models:")
    for model_key, info in registry.list_models().items():
        print(f"  {model_key}: {info['model_type']} - {info['status']}")
