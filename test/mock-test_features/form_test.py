import pytest
import json
from unittest.mock import Mock, patch
from src.features.form_automation import FormAutomator
from src.core.browser import Browser

class TestFormAutomation:
    @pytest.fixture
    def mock_browser(self):
        with patch('src.core.browser.Browser') as mock:
            browser = Mock()
            browser.find_element.return_value = Mock()
            yield browser

    @pytest.fixture
    def form_automator(self, mock_browser):
        return FormAutomator(mock_browser)

    def test_fill_input(self, form_automator, mock_browser):
        # Mock element
        mock_element = Mock()
        mock_browser.find_element.return_value = mock_element

        result = form_automator.fill_input("#username", "testuser")
        
        assert result == True
        mock_element.clear.assert_called_once()
        mock_element.send_keys.assert_called_once_with("testuser")

    def test_fill_form(self, form_automator, mock_browser, tmp_path):
        # Create test config
        config = {
            "fields": [
                {
                    "type": "input",
                    "selector": "#username",
                    "value": "testuser"
                },
                {
                    "type": "input",
                    "selector": "#password",
                    "value": "testpass"
                }
            ],
            "submit": "#submit-btn"
        }
        
        config_path = tmp_path / "form_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)

        result = form_automator.fill_form(str(config_path))
        assert result == True