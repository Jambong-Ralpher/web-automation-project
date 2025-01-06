import os
import re
import time
from datetime import datetime
from typing import Optional, Union
from urllib.parse import urlparse
import json

def create_directory(directory_path: str) -> bool:
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
            return True
        except OSError as error:
            print(f"Error creating directory: {error}")
            return False
    else:
        print(f"Directory already exists: {directory_path}")
        return True

def save_to_file(data: Union[str, dict, list], filepath: str, mode: str = 'w') -> bool:
    """Save data to file"""
    try:
        directory = os.path.dirname(filepath)
        if directory:
            create_directory(directory)
            
        if isinstance(data, (dict, list)):
            with open(filepath, mode) as f:
                json.dump(data, f, indent=4)
        else:
            with open(filepath, mode) as f:
                f.write(str(data))
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def generate_timestamp() -> str:
    """Generate timestamp string"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def clean_filename(filename: str) -> str:
    """Clean string for use as filename"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def wait_with_timeout(seconds: int, condition_func, interval: float = 0.5) -> bool:
    """Wait for condition with timeout"""
    start_time = time.time()
    while time.time() - start_time < seconds:
        if condition_func():
            return True
        time.sleep(interval)
    return False

def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL"""
    try:
        return urlparse(url).netloc
    except:
        return None

def format_bytes(size: int) -> str:
    """Format bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def create_filename(prefix: str, extension: str) -> str:
    """Create filename with timestamp"""
    timestamp = generate_timestamp()
    return f"{prefix}_{timestamp}.{extension.lstrip('.')}"

def ensure_suffix(text: str, suffix: str) -> str:
    """Ensure text ends with suffix"""
    return text if text.endswith(suffix) else text + suffix