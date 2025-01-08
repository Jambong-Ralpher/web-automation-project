from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from typing import Dict, Any, Optional
from ..utils.logger import setup_logger
from ..core.browser import Browser

class FormAutomator:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.logger = setup_logger('FormAutomator', 'logs/form_automation.log')

    def fill_input(self, selector: str, value: str, by: By = By.CSS_SELECTOR) -> bool:
        """Fill input field"""
        try:
            element = self.browser.find_element(by, selector)
            element.clear()
            element.send_keys(value)
            return True
        except Exception as e:
            self.logger.error(f"Failed to fill input {selector}: {str(e)}")
            return False

    def select_dropdown(self, selector: str, value: str, by: By = By.CSS_SELECTOR) -> bool:
        """Select dropdown option"""
        try:
            element = Select(self.browser.find_element(by, selector))
            element.select_by_visible_text(value)
            return True
        except Exception as e:
            self.logger.error(f"Failed to select dropdown {selector}: {str(e)}")
            return False

    def click_button(self, selector: str, by: By = By.CSS_SELECTOR) -> bool:
        """Click button element"""
        try:
            element = self.browser.find_element(by, selector)
            element.click()
            return True
        except Exception as e:
            self.logger.error(f"Failed to click button {selector}: {str(e)}")
            return False

    def fill_form(self, config_path: str) -> bool:
        """Fill form using configuration file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            for field in config['fields']:
                field_type = field['type']
                selector = field['selector']
                value = field['value']

                if field_type == 'input':
                    success = self.fill_input(selector, value)
                elif field_type == 'select':
                    success = self.select_dropdown(selector, value)
                elif field_type == 'button':
                    success = self.click_button(selector)
                
                if not success:
                    return False
                time.sleep(0.5)  
            # Submit form if submit selector provided
            if 'submit' in config:
                return self.click_button(config['submit'])
            
            return True

        except Exception as e:
            self.logger.error(f"Form automation failed: {str(e)}")
            return False

    def wait_for_element(self, selector: str, timeout: int = 10) -> Optional[Any]:
        """Wait for element to be present"""
        try:
            element = WebDriverWait(self.browser.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except Exception as e:
            self.logger.error(f"Timeout waiting for element {selector}: {str(e)}")
            return None