import pytest
import os
from unittest.mock import Mock, patch
from src.features.email_automation import EmailAutomator

class TestEmailAutomation:
    @pytest.fixture
    def email_automator(self):
        return EmailAutomator()

    @pytest.fixture
    def mock_smtp(self):
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = Mock()
            mock_smtp.return_value = mock_server
            yield mock_server

    def test_connect_success(self, email_automator, mock_smtp):
        # Test successful connection
        result = email_automator.connect("smtp.test.com", 587, "user", "pass")
        assert result == True
        assert email_automator.connected == True
        mock_smtp.login.assert_called_once_with("user", "pass")

    def test_connect_failure(self, email_automator, mock_smtp):
        # Test connection failure
        mock_smtp.login.side_effect = Exception("Connection failed")
        result = email_automator.connect("smtp.test.com", 587, "user", "pass")
        assert result == False
        assert email_automator.connected == False

    def test_send_email_success(self, email_automator, mock_smtp):
        # Setup
        email_automator.connected = True
        email_automator.smtp_server = mock_smtp

        # Test
        result = email_automator.send_email(
            sender="test@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            body="Test Body"
        )
        
        assert result == True
        assert mock_smtp.send_message.called

    def test_send_email_with_attachment(self, email_automator, mock_smtp, tmp_path):
        # Setup
        email_automator.connected = True
        email_automator.smtp_server = mock_smtp
        
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")

        # Test
        result = email_automator.send_email(
            sender="test@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            body="Test Body",
            attachments=[str(test_file)]
        )
        
        assert result == True
        assert mock_smtp.send_message.called

    def test_send_bulk_emails(self, email_automator, mock_smtp, tmp_path):
        # Setup
        email_automator.connected = True
        email_automator.smtp_server = mock_smtp
        
        # Create test config file
        config = {
            "sender": "test@example.com",
            "emails": [
                {
                    "to": "recipient1@example.com",
                    "subject": "Test 1",
                    "body": "Body 1"
                },
                {
                    "to": "recipient2@example.com",
                    "subject": "Test 2",
                    "body": "Body 2"
                }
            ]
        }
        
        config_file = tmp_path / "email_config.json"
        config_file.write_text(str(config))

        # Test
        results = email_automator.send_bulk_emails(str(config_file))
        
        assert len(results) == 2
        assert all(results.values())
        assert mock_smtp.send_message.call_count == 2

    def test_close_connection(self, email_automator, mock_smtp):
        # Setup
        email_automator.connected = True
        email_automator.smtp_server = mock_smtp

        # Test
        email_automator.close()
        
        assert email_automator.connected == False
        assert mock_smtp.quit.called