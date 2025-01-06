import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional

def setup_logger(
    logger_name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    max_bytes: int = 5_242_880,  # 5MB
    backup_count: int = 3
) -> logging.Logger:
    """Setup and configure logger"""
    
    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler if log_file specified
    if log_file:
        try:
            # Create log directory if doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

            # Setup rotating file handler
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to setup file logging: {str(e)}")

    return logger

def get_log_filename(prefix: str = 'automation') -> str:
    """Generate log filename with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.log"

# Example usage
if __name__ == '__main__':
    log_file = os.path.join('logs', get_log_filename())
    logger = setup_logger('test_logger', log_file)
    
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')