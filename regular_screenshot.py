from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')

chrome_service = Service(executable_path='/usr/bin/chromedriver')

driver_options = Options()
driver_options.add_argument("--headless=new")
driver_options.add_argument("--no-sandbox")
driver_options.add_argument("--disable-dev-shm-usage")
driver_options.add_argument("--user-data-dir=selenium")

driver_options.add_argument("--window-size=1366,1000")

driver = webdriver.Chrome(service=chrome_service, options=driver_options)

driver.get("http://10.0.5.78/")
driver.save_screenshot(f'screenshots/{date}.png')
driver.quit()