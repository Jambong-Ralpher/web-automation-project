import pytest
import json
from unittest.mock import Mock, patch
from src.features.email_automation import EmailAutomator

class TestEmailAutomation:
    @pytest.fixture
    def mock_smtp(self):
        with patch('smtplib.SMTP') as mock:
            server = Mock()
            mock.return_value = server
            yield server

    @pytest.fixture
    def email_automator(self, mock_smtp):
        automator = EmailAutomator()
        automator.smtp_server = mock_smtp
        automator.connected = True
        return automator

    def test_send_email(self, email_automator, mock_smtp):
        result = email_automator.send_email(
            sender="test@example.com",
            recipient="to@example.com",
            subject="Test",
            body="Test body"
        )
        assert result == True
        assert mock_smtp.send_message.called

    def test_bulk_email(self, email_automator, mock_smtp, tmp_path):
        config = {
            "sender": "test@example.com",
            "emails": [
                {"to": "one@example.com", "subject": "Test 1", "body": "Body 1"},
                {"to": "two@example.com", "subject": "Test 2", "body": "Body 2"}
            ]
        }
        config_file = tmp_path / "email_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f)

        results = email_automator.send_bulk_emails(str(config_file))
        assert len(results) == 2
        assert mock_smtp.send_message.call_count == 2

    def test_connection_error(self, email_automator, mock_smtp):
        mock_smtp.send_message.side_effect = Exception("SMTP Error")
        result = email_automator.send_email(
            sender="test@example.com",
            recipient="to@example.com",
            subject="Test",
            body="Test body"
        )
        assert result == False

    def test_attachment_handling(self, email_automator, mock_smtp, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        result = email_automator.send_email(
            sender="test@example.com",
            recipient="to@example.com",
            subject="Test",
            body="Test body",
            attachments=[str(test_file)]
        )
        assert result == True
        assert mock_smtp.send_message.called