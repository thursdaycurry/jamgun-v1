# Jumpit Agent

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
# Jumpit option : 경력 ~3년 / 서버/백엔드 개발자, 웹 풀스택 개발, 블록체인 / Node.js/Python/JS/BlockChain/Golang
web = 'https://www.jumpit.co.kr/positions?jobCategory=1&jobCategory=3&jobCategory=22&career=3&techStack=Node.js&techStack=Python&techStack=JavaScript&techStack=Golang&techStack=Blockchain'
path = "./chromedriver_mac_arm64/chromedriver"
driver = webdriver.Chrome(path)
driver.get(web)
driver.maximize_window()
time.sleep(4)
#
# 🦎 Login Stage ----------------------------------------
# Click login button
login_btn = driver.find_element_by_xpath("//button[contains(text(), '로그인')]")
login_btn.click()
WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@name='email']")))
# time.sleep(4)
print('🦎 Success: click button - login')


# Insert Email
email_input = driver.find_element_by_xpath("//input[@name='email']")
email_input.send_keys(os.environ.get('JUMPIT_ID'))
time.sleep(2)
print('🦎 Success: Inserted EMAIL')

# Click Next for password
next_btn = driver.find_element_by_xpath("//button[@type='submit']")
next_btn.click()
time.sleep(2)
print('🦎 Success: Click next')

# Insert Password
password_input = driver.find_element_by_xpath('//input[@type="password"]')
password_input.send_keys(os.environ.get('JUMPIT_PASSWORD'))
time.sleep(4)
print('🦎 Success: Inserted PASSWORD')

# Click to login
next_btn = driver.find_element_by_xpath("//button[@type='submit']")
next_btn.click()
time.sleep(5)
print('🦎 Success: Click next')


# 🦉 Listening Stage ----------------------------------------

# Infinite Scroll until touch down to the bottom
last_height = driver.execute_script("return document.body.scrollHeight")
scrolling = True

while scrolling:
# for test
# for x in range(3):

    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('🦉 Moved to next scroll')
    time.sleep(3)

    # Get current height
    new_height = driver.execute_script("return document.body.scrollHeight")

    # Compare current and last height
    # If no difference, break loop because it is the bottom line
    if new_height == last_height:
        scrolling = False
        break
    else:
        last_height = new_height

# Get url resources and convert into url strings
url_resources = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/position/')]")))
url_list = [url.get_attribute('href') for url in url_resources]
print('🦉 All urls are extracted')
print(f'url_list len : {len(url_list)}')
print(url_list)

# Initialize data list
company_data = []
job_title_data = []
appliedToday_data = []

# job_contract_data = []
# location_data = []
# application_data = []


# counter
counter_basic = 0
counter_apply = 0

for url in url_list:

    if counter_apply == 30 :
        break

    # Counter check
    counter_basic += 1
    print(f'no.{counter_basic} ---------------------------')

    driver.get(url)
    time.sleep(4)
    profile_section = driver.find_elements_by_xpath("//div[@class='position_wing_con']")

    result = profile_section[0].text.split('\n')
    print(f'result len: {len(result)}')
    print(result)

    company_text = result[1]
    job_title_text = result[0]
    application_text = result[-3] # 버튼 내 지원하기/지원완료 여부 텍스트
    isApplided = 0 # 지원여부 0 falsy, 1 truthy

    print(company_text)
    print(job_title_text)

    company_data.append(company_text)
    job_title_data.append(job_title_text)


    """
    target button types (JUMPIT)
    - 지원하기 : Green signal. click -> modal pop up -> '지원하기' click -> (moved to main page(auto))
    - 지원 완료 : Red signal. button attr 'disabled' status
    """
    # In case of '지원하기' which is applicable directly by single click(for JUMPIT)
    try:
        if application_text == '지원하기':
            apply_modal_btn = driver.find_element_by_xpath("//button[contains(text(), '지원하기')]")
            apply_modal_btn.click()
            time.sleep(2)

            # 첨부한 이력서 보내기 옵션 활성화
            input_box = driver.find_element_by_xpath('//input[@type="checkbox"]')
            input_box.click()
            time.sleep(2)

            # 지원하기 버튼
            apply_btn = driver.find_element_by_xpath("//button[@type='submit']")
            apply_btn.click()
            time.sleep(6)

            # appliedToday_data.append([company_text, job_title_text])
            isApplided = 1
            counter_apply += 1
            print('🔖 Your job application was send successfully!')
    except:
        print('입사 지원 불가')

    appliedToday_data.append(isApplided)
    time.sleep(2)

print('✅ Scraping tasks are completed')

print(len(company_data))
print(len(job_title_data))
print(len(appliedToday_data))

print('---------------------')

# make pandas df
df_jobPosts = pd.DataFrame({
    'company': company_data,
    'job_title': job_title_data,
    'appliedToday': appliedToday_data
})


# convert df into csv file
df_jobPosts.to_csv('data/' + str(date.today()) + '-jumpit.csv', index=False)
print(df_jobPosts)