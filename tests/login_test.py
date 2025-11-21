from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Adjust path to your ChromeDriver
CHROME_DRIVER_PATH = "chromedriver.exe"

driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))

try:
    # Open Login Page
    driver.get("http://127.0.0.1:5500/frontend/login.html")
    driver.maximize_window()

    # Wait for page
    time.sleep(1)

    # Fill email
    email_box = driver.find_element(By.ID, "email")
    email_box.send_keys("test@example.com")

    # Fill password
    password_box = driver.find_element(By.ID, "password")
    password_box.send_keys("Test@123")

    # Click login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for redirect
    time.sleep(2)

    print("✅ Login Test Completed")

finally:
    driver.quit()
