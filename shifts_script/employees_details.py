from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
import requests


driver_path = "path\\to\\chrome\\drive.exe"
shiftorgnizer_login_url = 'https://app.shiftorganizer.com/login/?lang=he&previous=homepage&greeting=true'

# # enabling headless chrome
def setting_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('window-size=1920x1080')
    return chrome_options

driver = webdriver.Chrome(executable_path=driver_path, options=setting_chrome_options()) 

employees = {}
usernames = []
def get_employees_details():
    driver.get (shiftorgnizer_login_url)
    driver.implicitly_wait(20)
    driver.find_element_by_id('company').send_keys(entry_company_id.get())
    driver.find_element_by_id ('username').send_keys(entry_username.get())
    driver.find_element_by_id ('password').send_keys(entry_password.get())
    driver.find_element_by_id('log-in').click()
    WebDriverWait(driver, 10).until(EC.title_contains("בית | ShiftOrganizer"))
    # print(driver.get_cookies())
    cookies_before = driver.get_cookies()
    sessionid_name = cookies_before[0]['name']
    sessionid_value = cookies_before[0]['value']
    csrftoken_name = cookies_before[1]['name']
    csrtoken_value = cookies_before[1]['value']
    cookies = {sessionid_name: sessionid_value, csrftoken_name: csrtoken_value}
    result = requests.get('https://app.shiftorganizer.com/api/employees/', cookies = cookies).json()
    
    # Saving Users details
    for user in result:
        user_name = user['user']['username']
        employees[user_name] = {}
        usernames.append(user_name)
        employees[user_name]['employee_id'] = user['id']
        employees[user_name]['user_id'] = user['user']['id']
        employees[user_name]['first_name'] = user['user']['first_name']
        employees[user_name]['last_name'] = user['user']['last_name']
        employees[user_name]['email'] = user['user']['email']
        employees[user_name]['phone_number'] = user['user']['phone_number']
        return usernames
