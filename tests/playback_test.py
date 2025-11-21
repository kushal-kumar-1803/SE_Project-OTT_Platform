from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

CHROME_DRIVER_PATH = "chromedriver.exe"

driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))

try:
    # Open Index Page
    driver.get("http://127.0.0.1:5500/frontend/index.html")
    driver.maximize_window()

    time.sleep(2)

    # Click first movie in list (dynamic)
    first_movie = driver.find_element(By.CSS_SELECTOR, ".movie-card")
    first_movie.click()

    time.sleep(2)

    print("🎬 Playback Test Completed")

finally:
    driver.quit()
