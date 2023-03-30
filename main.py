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
from datetime import date

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

# Infinite Scroll until touch down to the bottom
last_height = driver.execute_script("return document.body.scrollHeight")
scrolling = True

# while scrolling:

# for test
for x in range(2):

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('🦉 Moved to next scroll')
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        scrolling = False
        break
    else:
        last_height = new_height

# Get url resources and convert into url strings
url_resources = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/companies-to-app')]")))
url_list = [url.get_attribute('href') for url in url_resources]
print('🦉 All urls are extracted')
print(f'url_list len : {len(url_list)}')

# Initialize data list
company_data = []
job_title_data = []
job_contract_data = []
location_data = []
application_data = []
appliedToday_data = []

for url in url_list:

    driver.get(url)
    profile_section = driver.find_elements_by_xpath("//aside")
    time.sleep(5)

    result = profile_section[0].text.split('\n')
    print(f'result len: {len(result)}')
    print(result)

    company_text = result[0]
    job_title_text = result[-5]
    job_contract_text = result[-4]
    location_text = result[-3]
    application_text = result[-1]

    company_data.append(company_text)
    job_title_data.append(job_title_text)
    job_contract_data.append(job_contract_text)
    location_data.append(location_text)
    application_data.append(application_text)

    """
    target button types
    - 입사 지원하기 : Green signal. click -> modal pop up -> '지원하기' click -> (moved to main page(auto))
    - 지원 완료 : Red signal. button attr 'disabled' status
    - 지원하러 가기 : Orange. You should go to another site
    """
    # In case of '입사 지원하기' which is applicable directly by single click
    try:
        if application_text == '입사 지원하기':
            apply_modal_btn = driver.find_element_by_xpath("//button[contains(text(), '지원하기')]")
            apply_modal_btn.click()
            time.sleep(3)

            apply_btn = driver.find_element_by_xpath("//button[text()='지원하기']")
            apply_btn.click()
            time.sleep(3)

            appliedToday_data.append([company_text, job_title_text])
            print('🔖 Your job application was send successfully!')
    except:
        print('입사 지원 불가')

    print('---------------------')
    time.sleep(5)

print('✅ Scraping tasks are completed')

print(len(company_data))
print(len(job_title_data))
print(len(job_contract_data))
print(len(location_data))
print(len(application_data))

print('---------------------')

company_data = []
job_title_data = []
job_contract_data = []
location_data = []
application_data = []
appliedToday_data = []

df_jobPosts = pd.DataFrame({
    'company': company_data,
    'job_title': job_title_data,
    'job_contract': job_contract_data,
    'location': location_data,
    'application type': application_data,
    'appliedToday': appliedToday_data
})
df_jobPosts.to_csv('data.csv', index=False)
print(df_jobPosts)