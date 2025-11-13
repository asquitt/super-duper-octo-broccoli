"""Configuration loader and validator."""

import yaml
from pathlib import Path
from typing import Any, Dict
import os


class ConfigLoader:
    """Load and manage configuration from YAML file."""

    def __init__(self, config_path: str = None):
        """Initialize with config file path."""
        if config_path is None:
            # Default to config/config.yaml in project root
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "config.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Override with environment variables if present
        config = self._apply_env_overrides(config)

        return config

    def _apply_env_overrides(self, config: Dict) -> Dict:
        """Apply environment variable overrides."""
        # Example: CLIP_EXTRACTOR_NUM_CLIPS overrides general.num_clips
        env_prefix = "CLIP_EXTRACTOR_"

        if os.getenv(f"{env_prefix}NUM_CLIPS"):
            config['general']['num_clips'] = int(os.getenv(f"{env_prefix}NUM_CLIPS"))

        if os.getenv(f"{env_prefix}MIN_DURATION"):
            config['general']['min_clip_duration'] = int(os.getenv(f"{env_prefix}MIN_DURATION"))

        if os.getenv(f"{env_prefix}MAX_DURATION"):
            config['general']['max_clip_duration'] = int(os.getenv(f"{env_prefix}MAX_DURATION"))

        return config

    def get(self, key_path: str, default=None) -> Any:
        """
        Get configuration value using dot notation.

        Example: config.get('audio.emotion.mfcc_coefficients')
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration dictionary."""
        return self.config

    def validate(self) -> bool:
        """Validate configuration has required fields."""
        required_sections = ['general', 'audio', 'text', 'visual', 'fusion']

        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required config section: {section}")

        # Validate weights sum to 1.0
        weights = self.config['fusion']['weights']
        weight_sum = weights['audio'] + weights['text'] + weights['visual']
        if abs(weight_sum - 1.0) > 0.01:
            raise ValueError(f"Fusion weights must sum to 1.0, got {weight_sum}")

        return True
