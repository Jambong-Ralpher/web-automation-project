from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup  # For HTML parsing
import requests  # For making HTTP requests (email automation)

def main():
    # User input for target URL and desired actions
    target_url = input("Enter the URL you want to automate: ")
    action_choice = input("Choose an action (1: Scrape data, 2: Fill form, 3: Send email): ")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    if action_choice == "1":
        # Data Extraction (replace with specific logic as needed)
        driver.get(target_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Prompt user for desired data types (text, images, etc.)
        data_type = input("Enter data type to extract (text, images): ")

        if data_type == "text":
            # Extract text from all paragraphs
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                print(paragraph.text.strip())

        elif data_type == "images":
            # Extract image URLs from image tags
            images = soup.find_all('img')
            for image in images:
                image_url = image.get('src')
                print(image_url)

        else:
            print("Invalid data type. Please choose text or images.")

    elif action_choice == "2":
        form_url = input("Enter the form URL: ")
        driver.get(form_url)

        
        name_field = input("Enter the name field ID: ")
        name_value = input("Enter your name: ")
        email_field = input("Enter the email field ID: ")
        email_value = input("Enter your email address: ")

        try:
            name_field = driver.find_element_by_id(name_field)
            name_field.send_keys(name_value)
            email_field = driver.find_element_by_id(email_field)
            email_field.send_keys(email_value)

            submit_button = driver.find_element_by_id("submit_button_id")  
            submit_button.click()
            print("Form submitted successfully!")

        except Exception as e:
            print("Error filling the form:", e)

    elif action_choice == "3":
        # Email Automation 
        sender_email = input("Enter your email address: ")
        sender_password = input("Enter your email password: ")
        recipient_email = input("Enter recipient email address: ")
        subject = input("Enter email subject: ")
        body = input("Enter email body: ")

        # Replace with actual API endpoint or SMTP server details
        url = "https://api.example.com/sendemail"  # Replace with actual API endpoint

        data = {
            "sender": sender_email,
            "password": sender_password,
            "recipient": recipient_email,
            "subject": subject,
            "body": body
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print("Error sending email:", response.text)

    else:
        print("Invalid action choice.")

    driver.quit()

if __name__ == "__main__":
    main()