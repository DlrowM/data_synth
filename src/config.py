import yaml
import os
from typing import Dict, Any

class Config:
    def __init__(self, config_path: str = None):
        self.config = self._load_default_config()
        if config_path:
            self._update_config(config_path)
    
    def _load_default_config(self) -> Dict[str, Any]:
        default_path = os.path.join(os.path.dirname(__file__), '../configs/default.yaml')
        with open(default_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _update_config(self, config_path: str):
        with open(config_path, 'r') as f:
            custom_config = yaml.safe_load(f)
            self._deep_update(self.config, custom_config)
    
    def _deep_update(self, original: Dict[str, Any], update: Dict[str, Any]):
        for key, value in update.items():
            if isinstance(value, dict) and key in original:
                self._deep_update(original[key], value)
            else:
                original[key] = value
    
    def __getitem__(self, key: str):
        return self.config[key]
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)