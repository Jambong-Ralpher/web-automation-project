import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class WebAutomationTester:
    def __init__(self, config_file):
        """
        Initializes the WebAutomationTester with configuration data.

        Args:
            config_file (str): Path to the configuration file (JSON format).
        """
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def teardown_method(self):
        """Cleans up after each test by closing the browser."""
        self.browser.quit()

    def _get_element(self, selector, timeout=10):
        """
        Finds and returns a WebElement.

        Args:
            selector (str): CSS selector or XPath.
            timeout (int, optional): Maximum time to wait for the element. Defaults to 10 seconds.

        Returns:
            WebElement: The found element.
        """
        try:
            return WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
        except:
            raise Exception(f"Element not found: {selector}")

    def _enter_text(self, selector, text):
        """
        Enters text into an input field.

        Args:
            selector (str): CSS selector of the input field.
            text (str): Text to enter.
        """
        element = self._get_element(selector)
        element.clear()
        element.send_keys(text)

    def _click_element(self, selector):
        """
        Clicks on an element.

        Args:
            selector (str): CSS selector of the element.
        """
        element = self._get_element(selector)
        element.click()

    def _verify_text_present(self, selector, expected_text):
        """
        Verifies if the expected text is present in the element.

        Args:
            selector (str): CSS selector of the element.
            expected_text (str): Expected text to be present.
        """
        element = self._get_element(selector)
        actual_text = element.text
        assert expected_text in actual_text, f"Expected text '{expected_text}' not found in element: {actual_text}"

    def _perform_login(self):
        """
        Performs login based on configuration.
        """
        username_field = self._get_element(self.config['login']['username_field'])
        self._enter_text(username_field, self.config['login']['username'])
        password_field = self._get_element(self.config['login']['password_field'])
        self._enter_text(password_field, self.config['login']['password'])
        self._click_element(self.config['login']['submit_button'])

    # Add more test methods for specific functionalities
    # e.g., test_search_function, test_add_item, test_delete_item, etc.

    def run_tests(self):
        """
        Runs all defined tests.
        """
        try:
            self._perform_login()
            # Run other test methods here
            print("All tests passed!")
        except Exception as e:
            print(f"Test failed: {str(e)}")



# Run tests
if __name__ == "__main__":
    tester = WebAutomationTester("config/test.config.json")  
    tester.run_tests()