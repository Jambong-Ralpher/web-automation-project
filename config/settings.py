import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Create necessary directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Browser Settings
BROWSER_SETTINGS = {
    'headless': False,  # Set to True for headless mode
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'window_size': (1920, 1080),
    'implicit_wait': 10,
    'page_load_timeout': 30
}

# Logging Configuration
LOG_CONFIG = {
    'filename': os.path.join(LOG_DIR, 'automation.log'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'level': 'INFO'
}

# API Credentials (from environment variables)
SOCIAL_MEDIA = {
    'twitter_api_key': os.getenv('TWITTER_API_KEY'),
    'twitter_api_secret': os.getenv('TWITTER_API_SECRET'),
    'facebook_token': os.getenv('FACEBOOK_TOKEN')
}

# Email Settings
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'smtp_username': os.getenv('SMTP_USERNAME'),
    'smtp_password': os.getenv('SMTP_PASSWORD')
}

# Scraping Settings
SCRAPING_CONFIG = {
    'request_timeout': 30,
    'retry_attempts': 3,
    'delay_between_requests': 2,
    'max_concurrent_requests': 5
}

# Form Automation Settings
FORM_CONFIG = {
    'default_timeout': 10,
    'screenshot_on_error': True,
    'screenshot_dir': os.path.join(OUTPUT_DIR, 'screenshots')
}

# Testing Configuration
TEST_CONFIG = {
    'screenshot_on_failure': True,
    'video_capture': False,
    'report_dir': os.path.join(OUTPUT_DIR, 'test_reports')
}