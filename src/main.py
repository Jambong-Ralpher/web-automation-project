import click
import os
from core.browser import Browser
from features.data_extraction import DataExtractor
from features.form_automation import FormAutomator
from features.web_scraping import WebScraper
from features.email_automation import EmailAutomator
from features.social_media import SocialMediaAutomator
from utils.logger import setup_logger
from utils.helpers import create_directory, save_to_file

logger = setup_logger('main', 'logs/automation.log')

@click.group()
def cli():
    """Web Automation Tool - Automate various web tasks"""
    pass

@cli.command()
@click.option('--url', required=True, help='Target URL to scrape')
@click.option('--output', default='output/data.json', help='Output file path')
@click.option('--selector', default='body', help='CSS selector to extract')
def extract(url, output, selector):
    """Extract data from a webpage"""
    with Browser() as browser:
        extractor = DataExtractor(browser)
        try:
            browser.navigate_to(url)
            data = extractor.extract_text(selector)
            if save_to_file(data, output):
                click.echo(f"Data saved to {output}")
            else:
                click.echo("Failed to save data")
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")

@cli.command()
@click.option('--url', required=True, help='Form URL')
@click.option('--config', required=True, type=click.Path(exists=True), help='Form config file')
def fill_form(url, config):
    """Automate form filling"""
    with Browser() as browser:
        form = FormAutomator(browser)
        try:
            browser.navigate_to(url)
            form.fill_form(config)
            click.echo("Form submitted successfully")
        except Exception as e:
            logger.error(f"Form automation failed: {str(e)}")

@cli.command()
@click.option('--url', required=True, help='Target URL')
@click.option('--email', required=True, help='Email address')
@click.option('--password', required=True, help='Password')
@click.option('--message', help='Message to post')
def social_media(url, email, password, message):
    """Automate social media tasks"""
    with Browser() as browser:
        social = SocialMediaAutomator(browser)
        try:
            social.login(url, email, password)
            if message:
                social.post_message(message)
            click.echo("Social media task completed")
        except Exception as e:
            logger.error(f"Social media automation failed: {str(e)}")

@cli.command()
@click.option('--config', required=True, type=click.Path(exists=True), help='Email config file')
def send_email(config):
    """Send automated emails"""
    email = EmailAutomator()
    try:
        email.send_from_config(config)
        click.echo("Emails sent successfully")
    except Exception as e:
        logger.error(f"Email automation failed: {str(e)}")

@cli.command()
@click.option('--url', required=True, help='URL to test')
@click.option('--test-type', type=click.Choice(['functional', 'performance', 'security']), 
              default='functional', help='Type of test to run')
def test(url, test_type):
    """Run web application tests"""
    with Browser() as browser:
        try:
            browser.navigate_to(url)
            
            click.echo(f"{test_type.capitalize()} test completed")
        except Exception as e:
            logger.error(f"Testing failed: {str(e)}")

if __name__ == '__main__':
    # Create necessary directories
    create_directory('logs')
    create_directory('output')
    
    # Run CLI
    cli()