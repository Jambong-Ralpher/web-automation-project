import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Dict, Optional
from ..utils.logger import setup_logger
from ..utils.helpers import validate_url

class EmailAutomator:
    def __init__(self):
        self.logger = setup_logger('EmailAutomator', 'logs/email_automation.log')
        self.smtp_server = None
        self.connected = False

    def connect(self, host: str, port: int, username: str, password: str, use_tls: bool = True) -> bool:
        """Connect to SMTP server"""
        try:
            self.smtp_server = smtplib.SMTP(host, port)
            if use_tls:
                self.smtp_server.starttls()
            self.smtp_server.login(username, password)
            self.connected = True
            self.logger.info(f"Connected to SMTP server: {host}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to SMTP server: {str(e)}")
            return False

    def send_email(self, 
                  sender: str, 
                  recipient: str, 
                  subject: str, 
                  body: str,
                  attachments: Optional[List[str]] = None) -> bool:
        """Send single email"""
        if not self.connected:
            self.logger.error("Not connected to SMTP server")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject

            # Add body
            msg.attach(MIMEText(body, 'html'))

            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                            msg.attach(part)

            # Send email
            self.smtp_server.send_message(msg)
            self.logger.info(f"Email sent to {recipient}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_bulk_emails(self, config_file_path):
        try:
            with open(config_file_path, 'r') as f:
                config = json.load(f)
                results = {}

                for email_task in config['emails']:
                    recipient = email_task['to']
                    result = self.send_email(
                        sender=config['sender'],
                        recipient=recipient,
                        subject=email_task['subject'],
                        body=email_task['body'],
                        attachments=email_task.get('attachments', [])
                    )
                    results[recipient] = result

                return results
        except Exception as e:
            self.logger.error(f"Bulk email sending failed: {str(e)}")
            return {}

    def close(self):
        """Close SMTP connection"""
        if self.smtp_server:
            try:
                self.smtp_server.quit()
                self.connected = False
                self.logger.info("SMTP connection closed")
            except Exception as e:
                self.logger.error(f"Error closing SMTP connection: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()