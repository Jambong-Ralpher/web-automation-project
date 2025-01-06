from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os
from typing import Optional, Union
from config.settings import BROWSER_SETTINGS, LOG_DIR

class Browser:
    def __init__(self):
        self.driver = None
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('Browser')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(LOG_DIR, 'browser.log'))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def start(self) -> None:
        """Initialize and start the browser"""
        try:
            chrome_options = webdriver.ChromeOptions()
            if BROWSER_SETTINGS['headless']:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument(f'user-agent={BROWSER_SETTINGS["user_agent"]}')
            chrome_options.add_argument(f'window-size={BROWSER_SETTINGS["window_size"][0]},'
                                      f'{BROWSER_SETTINGS["window_size"][1]}')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(BROWSER_SETTINGS['implicit_wait'])
            self.driver.set_page_load_timeout(BROWSER_SETTINGS['page_load_timeout'])
            
            self.logger.info('Browser started successfully')
        except WebDriverException as e:
            self.logger.error(f'Failed to start browser: {str(e)}')
            raise

    def navigate_to(self, url: str) -> bool:
        """Navigate to specified URL"""
        try:
            self.driver.get(url)
            self.logger.info(f'Navigated to {url}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to navigate to {url}: {str(e)}')
            return False

    def find_element(self, by: By, value: str, timeout: int = 10) -> Optional[webdriver.remote.webelement.WebElement]:
        """Find element with wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f'Element not found: {by}={value}')
            return None

    def take_screenshot(self, filename: str) -> bool:
        """Take screenshot of current page"""
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f'Screenshot saved to {filename}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to take screenshot: {str(e)}')
            return False

    def execute_script(self, script: str, *args) -> Union[None, any]:
        """Execute JavaScript code"""
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            self.logger.error(f'Failed to execute script: {str(e)}')
            return None

    def close(self) -> None:
        """Close browser and cleanup"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info('Browser closed successfully')
            except Exception as e:
                self.logger.error(f'Error closing browser: {str(e)}')
            finally:
                self.driver = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()