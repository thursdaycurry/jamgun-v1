# Selenium version 3.141.0
# pip install selenium==3.141.0

from selenium import webdriver
import os
import time

# Load env vars from .env
from dotenv import load_dotenv
load_dotenv()

web_intelliPick = 'https://intellipick.spartacodingclub.kr/'
path = "/Users/thursdaycurry/Desktop/chromedriver_mac_arm64/chromedriver"
driver = webdriver.Chrome(path)
driver.get(web_intelliPick)
driver.maximize_window()
time.sleep(4)

# 🦎 Login Stage ----------------------------------------

# Click login button
login_btn = driver.find_element_by_xpath('//a[@href="/login"]')
login_btn.click()
time.sleep(4)
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

