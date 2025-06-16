# scripts/models/model_registry.py
"""
Model Registry - Manages model metadata and loading
"""

import json
import torch
import pickle
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class ModelRegistry:
    def __init__(self, registry_path: str = "models/registry.json"):
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        """Load registry from disk."""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_registry(self):
        """Save registry to disk."""
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2, default=str)

    def register_model(self, 
                      name: str,
                      version: str,
                      model_path: str,
                      model_type: str,
                      metrics: Dict[str, float],
                      metadata: Optional[Dict[str, Any]] = None):
        """Register a new model version."""
        
        model_info = {
            'name': name,
            'version': version,
            'model_path': model_path,
            'model_type': model_type,
            'metrics': metrics,
            'metadata': metadata or {},
            'registered_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        model_key = f"{name}:{version}"
        self.registry[model_key] = model_info
        self._save_registry()
        
        print(f"Registered model {model_key}")

    def get_model_info(self, name: str, version: str = "latest") -> Optional[Dict[str, Any]]:
        """Get model information."""
        if version == "latest":
            # Find latest version
            model_versions = [k for k in self.registry.keys() if k.startswith(f"{name}:")]
            if not model_versions:
                return None
            # Sort by registration time
            latest_key = max(model_versions, 
                           key=lambda k: self.registry[k]['registered_at'])
            return self.registry[latest_key]
        else:
            model_key = f"{name}:{version}"
            return self.registry.get(model_key)

    def list_models(self) -> Dict[str, Any]:
        """List all registered models."""
        return self.registry

    def load_model(self, name: str, version: str = "latest", device: str = "cpu"):
        """Load a registered model."""
        model_info = self.get_model_info(name, version)
        if not model_info:
            raise ValueError(f"Model {name}:{version} not found in registry")
        
        model_path = Path(model_info['model_path'])
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load based on file extension
        if model_path.suffix == '.pth':
            model = torch.load(model_path, map_location=device)
        elif model_path.suffix == '.pkl':
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
        else:
            raise ValueError(f"Unsupported model format: {model_path.suffix}")
        
        return model

    def update_model_status(self, name: str, version: str, status: str):
        """Update model status (active, deprecated, archived)."""
        model_key = f"{name}:{version}"
        if model_key in self.registry:
            self.registry[model_key]['status'] = status
            self._save_registry()