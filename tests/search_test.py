from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

CHROME_DRIVER_PATH = "chromedriver.exe"

driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))

try:
    # Open Home Page
    driver.get("http://127.0.0.1:5500/frontend/index.html")
    driver.maximize_window()

    time.sleep(1)

    # Find search bar
    search_bar = driver.find_element(By.ID, "searchBar")
    search_bar.send_keys("Avengers")

    # Click Search
    search_button = driver.find_element(By.XPATH, "//button[contains(text(),'Search')]")
    search_button.click()

    time.sleep(2)

    print("🔍 Search Test Completed")

finally:
    driver.quit()
