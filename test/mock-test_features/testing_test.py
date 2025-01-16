import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.exceptions import TimeoutException

# Replace with the path to your configuration file
CONFIG_FILE_PATH = "config/test.config.json"


@pytest.fixture
def tester():
    """Provides a fixture for a WebAutomationTester instance"""
    tester = WebAutomationTester(CONFIG_FILE_PATH)
    yield tester
    tester.teardown_method()  # Close the browser after each test


def test_login_success(tester):
    """Tests successful login"""
    tester._perform_login()
    # Add assertions to verify successful login (e.g., check for presence of specific elements after login)


def test_login_invalid_credentials(tester):
    """Tests login failure with invalid credentials"""
    # Modify username or password in the configuration file for this test
    tester._perform_login()
    with pytest.raises(AssertionError):
        # Assert for an element indicating login failure (adjust selector based on your application)
        tester._verify_text_present("#login-error", "Invalid username or password")


def test_get_element_not_found(tester):
    """Tests handling of element not found exception"""
    with pytest.raises(Exception) as excinfo:
        tester._get_element("#invalid-selector")
    assert "Element not found: #invalid-selector" in str(excinfo.value)


def test_click_element_timeout(tester):
    """Tests handling of timeout exception during element click"""
    # Simulate a slow loading element by waiting for a short duration before making it clickable
    time.sleep(2)  # Replace with actual logic to make the element clickable after some delay
    with pytest.raises(TimeoutException):
        tester._click_element("#slow-loading-element")