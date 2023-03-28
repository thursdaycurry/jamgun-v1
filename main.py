# Selenium version 3.141.0
# pip install selenium==3.141.0

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# Load env vars from .env
from dotenv import load_dotenv
load_dotenv()

# Set up driver
web_intelliPick = 'https://intellipick.spartacodingclub.kr/'
# path = "/Users/thursdaycurry/Desktop/chromedriver_mac_arm64/chromedriver"
path = "./chromedriver_mac_arm64/chromedriver"
driver = webdriver.Chrome(path)
driver.get(web_intelliPick)
driver.maximize_window()
time.sleep(4)

# 🦎 Login Stage ----------------------------------------
# Click login button
login_btn = driver.find_element_by_xpath('//a[@href="/login"]')
login_btn.click()
WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), '이메일로')]")))
# time.sleep(4)
print('🦎 Success: click button - login')

# Click Start with Mail
email_start_btn = driver.find_element_by_xpath("//button[contains(text(), '이메일로')]")
email_start_btn.click()
time.sleep(4)
print('🦎 Success: click button - start with email')

# Insert Email
email_input = driver.find_element_by_xpath('//input[@type="email"]')
email_input.send_keys(os.environ.get('SPARTA_ID'))
time.sleep(2)
print('🦎 Success: Inserted EMAIL')

# Click Next for password
next_btn = driver.find_element_by_xpath('//button[@role="button"]')
next_btn.click()
time.sleep(2)
print('🦎 Success: Click next')

# Insert Password
password_input = driver.find_element_by_xpath('//input[@type="password"]')
password_input.send_keys(os.environ.get('SPARTA_PASSWORD'))
time.sleep(4)
print('🦎 Success: Inserted PASSWORD')

# Click final Login btn
final_login_btn = driver.find_element_by_xpath("//button[contains(text(), '로그인')]")
final_login_btn.click()
time.sleep(4)
print('🦎 Success: final login button clicked')


# 🦉 Listening Stage ----------------------------------------

# Create List


company_data = []
job_title_data = []
job_contract_data = []
location_data = []

# Infinite Scroll until touch down to the bottom
last_height = driver.execute_script("return document.body.scrollHeight")
scrolling = True
while scrolling:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('🦉 Moved to next scroll')
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        scrolling = False
        break
    else:
        last_height = new_height

# Get all urls
# url_resources = driver.find_elements_by_xpath("//a[contains(@href, '/companies-to-app')]")
url_resources = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/companies-to-app')]")))

for url in url_resources:
    print(url.get_attribute("href"))
