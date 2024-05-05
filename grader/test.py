from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
service = Service("/usr/lib/chromium/chromedriver")
options.binary_location = "/usr/lib/chromium/chromium"
driver = webdriver.Chrome(options=options, service=service)
driver.get("http://google.com")
print(driver.find_element(By.CSS_SELECTOR, "input"))
driver.quit()
