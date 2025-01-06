# Web Automation Project

This is a Python-based web automation tool that leverages the power of Selenium to automate various web tasks.

## Features
- Data extraction: Scrape text, images, and structured data.
- Form filling: Automate form filling and submission.
- Testing and monitoring: Perform functional, regression, and performance testing.
- Social media automation: Post content and engage with users.
- Email automation: Send automated emails and scrape email addresses.
- Web scraping and data mining: Extract large amounts of data.
- Web application testing: Test web applications for functionality, performance, and security.

## Requirements
- Python
- Chrome/Firefox browser
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd web-automation-project

python -m venv my_env
.\my_env\Scripts\Activate
pip install -r requirements.txt
```
## Project Structure
web-automation-project/
├── src/
│   ├── core/
│   │   ├── browser.py
│   │   └── config.py
│   ├── features/
│   │   ├── data_extraction.py
│   │   └── email_automation.py
│   └── utils/
│       ├── helpers.py
│       └── logger.py
├── tests/
│   └── test_features/
│       ├── dataex_test.py
│       └── email_test.py
└── config/
    └── test_email_config.json


# Run all tests
```bash
python -m pytest
```
# Run specific test file
```bash
python -m pytest test/test_features/name_test.py
```

## Troubleshooting

### Common Test Errors

1. **Bulk Email Test Failure**
```bash
FAILED test/test_features/email_test.py::TestEmailAutomation::test_send_bulk_emails - assert 0 == 2