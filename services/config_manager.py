"""
Configuration management service
"""

import json
import os
import logging
from typing import Dict, Any
from pathlib import Path
import constants

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_file: str = constants.CONFIG_FILE):
        self.config_file = config_file
        self.config = {}
        self.default_config = {
            "pdf_settings": {
                "default_theme_color": "#1f2937",
                "default_font_family": "OpenSans",
                "default_font_size": "11",
                "default_document_size": "Letter",
                "max_file_size_mb": 10,
                "output_directory": constants.OUTPUT_DIR,
                "temp_directory": constants.TEMP_DIR
            },
            "api_settings": {
                "max_request_size": "10MB",
                "rate_limit_per_minute": 60,
                "enable_cors": True,
                "debug_mode": False
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "app.log"
            },
            "fonts": {
                "opensans_regular": constants.OPENSANS_REGULAR_FONT,
                "opensans_bold": constants.OPENSANS_BOLD_FONT
            },
            "validation": {
                "max_work_experiences": 10,
                "max_educations": 5,
                "max_projects": 10,
                "max_skills_categories": 10,
                "max_description_length": 200,
                "required_fields": ["name", "email"]
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self.config = self._merge_configs(self.default_config, file_config)
                    logger.info(f"Configuration loaded from {self.config_file}")
            else:
                self.config = self.default_config.copy()
                self.save_config()
                logger.info(f"Created default configuration file: {self.config_file}")
            
            # Create necessary directories
            self._create_directories()
            
            return self.config
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            logger.info("Using default configuration")
            self.config = self.default_config.copy()
            return self.config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            logger.info("Using default configuration")
            self.config = self.default_config.copy()
            return self.config
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        try:
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
            return True
        except Exception as e:
            logger.error(f"Error setting config value {key}: {e}")
            return False
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration with new values"""
        try:
            self.config = self._merge_configs(self.config, updates)
            return self.save_config()
        except Exception as e:
            logger.error(f"Error updating config: {e}")
            return False
    
    def _merge_configs(self, base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge configuration dictionaries"""
        result = base.copy()
        
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _create_directories(self):
        """Create necessary directories"""
        try:
            output_dir = self.get('pdf_settings.output_directory', 'output')
            temp_dir = self.get('pdf_settings.temp_directory', 'temp')
            
            Path(output_dir).mkdir(exist_ok=True)
            Path(temp_dir).mkdir(exist_ok=True)
            Path('static/fonts').mkdir(parents=True, exist_ok=True)
            
            logger.info("Required directories created/verified")
        except Exception as e:
            logger.error(f"Error creating directories: {e}")
    
    def get_pdf_settings(self) -> Dict[str, Any]:
        """Get PDF-specific settings"""
        return self.get('pdf_settings', {})
    
    def get_api_settings(self) -> Dict[str, Any]:
        """Get API-specific settings"""
        return self.get('api_settings', {})
    
    def get_validation_settings(self) -> Dict[str, Any]:
        """Get validation settings"""
        return self.get('validation', {})
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled"""
        return self.get('api_settings.debug_mode', False)
    
    def get_font_paths(self) -> Dict[str, str]:
        """Get font file paths"""
        return self.get('fonts', {})
