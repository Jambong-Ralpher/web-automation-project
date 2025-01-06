import os
import json
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import logging
from pathlib import Path

class Configuration:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.settings = {}
        self.logger = self._setup_logger()
        self._load_environment()
        self._load_default_settings()
        if config_path:
            self._load_config_file()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('Config')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_environment(self) -> None:
        """Load environment variables"""
        load_dotenv()
        self.settings['env'] = {
            'SMTP_SERVER': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'SMTP_PORT': int(os.getenv('SMTP_PORT', 587)),
            'SMTP_USERNAME': os.getenv('SMTP_USERNAME'),
            'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD'),
            'TWITTER_API_KEY': os.getenv('TWITTER_API_KEY'),
            'TWITTER_API_SECRET': os.getenv('TWITTER_API_SECRET'),
            'FACEBOOK_TOKEN': os.getenv('FACEBOOK_TOKEN')
        }

    def _load_default_settings(self) -> None:
        """Load default settings"""
        self.settings.update({
            'browser': {
                'headless': False,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'window_size': (1920, 1080),
                'implicit_wait': 10,
                'page_load_timeout': 30
            },
            'scraping': {
                'request_timeout': 30,
                'retry_attempts': 3,
                'delay_between_requests': 2,
                'max_concurrent_requests': 5
            },
            'output': {
                'base_dir': str(Path.home() / 'web_automation_output'),
                'log_dir': str(Path.home() / 'web_automation_output' / 'logs'),
                'screenshots_dir': str(Path.home() / 'web_automation_output' / 'screenshots')
            }
        })

    def _load_config_file(self) -> None:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                file_config = json.load(f)
                self.settings.update(file_config)
                self.logger.info(f'Loaded configuration from {self.config_path}')
        except Exception as e:
            self.logger.error(f'Failed to load config file: {str(e)}')

    def save_config(self, path: Optional[str] = None) -> bool:
        """Save current configuration to file"""
        save_path = path or self.config_path
        if not save_path:
            self.logger.error('No config path specified')
            return False

        try:
            with open(save_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
            self.logger.info(f'Configuration saved to {save_path}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to save config: {str(e)}')
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.settings
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        keys = key.split('.')
        target = self.settings
        for k in keys[:-1]:
            target = target.setdefault(k, {})
        target[keys[-1]] = value
        self.logger.info(f'Updated configuration: {key} = {value}')

    def create_directories(self) -> None:
        """Create necessary directories"""
        for dir_path in [
            self.settings['output']['base_dir'],
            self.settings['output']['log_dir'],
            self.settings['output']['screenshots_dir']
        ]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            self.logger.info(f'Created directory: {dir_path}')