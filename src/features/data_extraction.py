from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import logging
import os
import time
from typing import List, Dict, Optional, Union
from ..core.browser import Browser
from ..utils.helpers import create_directory
from ..utils.logger import setup_logger

class DataExtractor:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.logger = setup_logger('DataExtractor')

    def extract_text(self, selector: str, by: By = By.CSS_SELECTOR) -> Optional[str]:
        """Extract text content from element"""
        try:
            element = self.browser.find_element(by, selector)
            return element.text if element else None
        except Exception as e:
            self.logger.error(f"Failed to extract text: {str(e)}")
            return None

    def extract_multiple_texts(self, selector: str, by: By = By.CSS_SELECTOR) -> List[str]:
        """Extract text from multiple elements"""
        texts = []
        try:
            elements = self.browser.driver.find_elements(by, selector)
            texts = [element.text for element in elements if element.text]
        except Exception as e:
            self.logger.error(f"Failed to extract multiple texts: {str(e)}")
        return texts

    def extract_table(self, table_selector: str) -> List[Dict[str, str]]:
        """Extract table data into list of dictionaries"""
        try:
            table = self.browser.find_element(By.CSS_SELECTOR, table_selector)
            html = table.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Get headers
            headers = []
            for th in soup.find_all('th'):
                headers.append(th.text.strip())
            
            # Get rows
            table_data = []
            for row in soup.find_all('tr')[1:]:  # Skip header row
                row_data = {}
                for index, cell in enumerate(row.find_all('td')):
                    if index < len(headers):
                        row_data[headers[index]] = cell.text.strip()
                if row_data:
                    table_data.append(row_data)
            
            return table_data
        except Exception as e:
            self.logger.error(f"Failed to extract table: {str(e)}")
            return []

    def download_images(self, selector: str, output_dir: str) -> List[str]:
        """Download images from webpage"""
        downloaded_files = []
        try:
            create_directory(output_dir)
            images = self.browser.driver.find_elements(By.CSS_SELECTOR, selector)
            
            for index, img in enumerate(images):
                src = img.get_attribute('src')
                if src:
                    try:
                        response = requests.get(src, timeout=10)
                        if response.status_code == 200:
                            file_name = f"image_{index}.{src.split('.')[-1]}"
                            file_path = os.path.join(output_dir, file_name)
                            
                            with open(file_path, 'wb') as f:
                                f.write(response.content)
                            downloaded_files.append(file_path)
                            time.sleep(1)  # Rate limiting
                    except Exception as e:
                        self.logger.error(f"Failed to download image {src}: {str(e)}")
                        
        except Exception as e:
            self.logger.error(f"Failed to process images: {str(e)}")
        
        return downloaded_files

    def extract_links(self, selector: str = 'a') -> List[Dict[str, str]]:
        """Extract all links and their text"""
        links = []
        try:
            elements = self.browser.driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                href = element.get_attribute('href')
                text = element.text
                if href:
                    links.append({
                        'url': href,
                        'text': text or href
                    })
        except Exception as e:
            self.logger.error(f"Failed to extract links: {str(e)}")
        return links

    def extract_structured_data(self, selectors: Dict[str, str]) -> Dict[str, str]:
        """Extract multiple elements using a dictionary of selectors"""
        data = {}
        for key, selector in selectors.items():
            try:
                element = self.browser.find_element(By.CSS_SELECTOR, selector)
                if element:
                    data[key] = element.text
            except Exception as e:
                self.logger.error(f"Failed to extract {key}: {str(e)}")
                data[key] = None
        return data