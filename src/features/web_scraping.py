from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import time


def get_user_input(prompt):
  """Gets user input from the console."""
  return input(prompt)

driver = webdriver.Chrome() 
url = get_user_input("Enter the URL of the login page: ")

# 1. Functionality Tests

# 1.1 Login Test
def test_login():
    driver.get(url) 
    driver.find_element(By.ID, "username").send_keys("your_username")
    driver.find_element(By.ID, "password").send_keys("your_password")
    driver.find_element(By.ID, "login_button").click()
    # Assert that the user is logged in successfully 
    assert "Welcome, User" in driver.page_source 


# 1.2 Product Search Test
def test_product_search():
  """Tests product search functionality."""
  url = get_user_input("Enter the URL of the homepage: ")
  driver.get(url)

  search_term = get_user_input("Enter the product name to search for: ")
  search_box = driver.find_element(By.ID, "search_bar")
  search_box.send_keys(search_term)
  search_box.submit()

  # Get assertion criteria from user
  expected_title_fragment = get_user_input("Enter the expected title fragment for search results: ")
  assert expected_title_fragment in driver.title, f"Expected title to contain '{expected_title_fragment}' but got {driver.title}"
# 2. Performance Tests (Basic)

def test_page_load_time():
    """Tests load time of Web Appplication"""
    url = get_user_input("Enter the URL of the web application:")
    driver.get(url)
    start_time = time.time()
    driver.refresh()
    end_time = time.time()
    load_time = end_time - start_time

    # Get acceptable load time from user
    acceptable_load_time = float(get_user_input("Enter the acceptable load time in seconds: ")) 
    assert load_time < acceptable_load_time, f"Load time exceeded acceptable limit. Expected under {acceptable_load_time} seconds, but took {load_time} seconds."

# 3. Security Tests (Basic)

def test_xss_protection():
  """Tests XSS protection of the web application."""
  url = get_user_input("Enter the URL of the page to test: ")
  driver.get(url)

  # Get input field details from user
  input_field_id = get_user_input("Enter the ID of the input field to test (if known): ")
  if not input_field_id:
    input_field_id = get_user_input("Enter a description of the input field to locate (e.g., 'search bar'): ")

  # Find the input field
  try:
    input_field = driver.find_element(By.ID, input_field_id)
  except:
    try:
      input_field = driver.find_element(By.NAME, input_field_id)  # Try by name if ID fails
    except:
      print(f"Could not find input field using ID or name: '{input_field_id}'.")
      return  # Skip the test if element not found

  # Get malicious script from user
  malicious_script = get_user_input("Enter the XSS test script to inject (e.g., '<script>alert('XSS')</script>'): ")

  input_field.send_keys(malicious_script)

  # Assertion (replace with more robust checks)
  print("WARNING: Due to limitations, this test might not definitively prove XSS protection. Inspect the page source or browser console for signs of script execution.")
  print(f"Injected script: {malicious_script}")


driver.quit()