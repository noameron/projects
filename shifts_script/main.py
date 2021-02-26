from datetime import date, datetime, timedelta
from tkinter import *

import requests
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import calendar_api

driver_path = "path//to//selenium//chromedriver.exe"
shiftorgnizer_login_url = 'https://app.shiftorganizer.com/login/?lang=he&previous=homepage&greeting=true'

# enabling headless chrome
def setting_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('window-size=1920x1080')
    return chrome_options

driver = webdriver.Chrome(executable_path=driver_path, options=setting_chrome_options()) 

# Login GUI

def login_gui():
    
    root = Tk()
    root.title('Shifter')
    root.geometry("450x260")
    root.attributes("-topmost", True)
    global entry_company_id
    global entry_username
    global entry_password
    global checkbox_var
    global label_logged_successfully
    global label_bad_login
    global label_event_complete
    global label_no_shifts_found
    checkbox_var = IntVar()
    
    # Text near text boxes
    # Or other labels
    label_company_id = Label(root, text='Company ID: ')
    label_username = Label(root, text='Username: ')
    label_password = Label(root, text='Password: ')
    label_logged_successfully = Label(root, fg='Green',text = '\nLogged in Successfully!')
    label_welcome = Label(root, text = '\nPlease enter your ShiftOrganizer credentials: \n')
    label_bad_login = Label(root, fg='Red' ,text = 'ERROR! \nEither Company ID is not a number / Username is not characters')
    label_no_shifts_found = Label(root, text = 'No shifts were found for selected week')
    label_event_complete = Label(root, fg='Green', text = 'Shifts Written To Calendar Successfully!')

    # Textboxe entries
    default_compny_id_var = StringVar(root, value='132')
    entry_company_id = Entry(root, textvariable=default_compny_id_var)
    entry_username = Entry(root)
    entry_username.focus()
    entry_password = Entry(root, show = '*')
    
    # Positioning of labels
    label_welcome.grid(row=0, column=1, sticky=W)
    label_company_id.grid(row=1, sticky=E)
    label_username.grid(row=2, sticky=E)
    label_password.grid(row=3, sticky=E)
    
    # Positioning of textboxes
    entry_company_id.grid(row=1, column=1)
    entry_username.grid(row=2, column=1)
    entry_password.grid(row=3, column=1) 

    # Buttons and more
    root.bind('<Return>', site_login)
    b = Button(root, text='Login', command=site_login)
    b.grid(row=6, column=1)
    checkbox = Checkbutton(root, text='Get next week Shifts', variable=checkbox_var)
    checkbox.grid(row=4, column=1)
    root.mainloop()

# Dates for Shifts URL
current_day_date = date.today()
this_sunday_date = current_day_date - timedelta(days = (current_day_date.weekday() + 1) % 7)
next_sunday_date = current_day_date + timedelta( (6 - current_day_date.weekday()) % 7 )
shifts_for_the_week = {}
# Site login with user's credentials
def site_login(*args):
    
    labels_list = []
    # Clear all labels if user retries login
    for label in labels_list:
        label.forget()
    driver.get (shiftorgnizer_login_url)
    driver.implicitly_wait(20)
    driver.find_element_by_id('company').send_keys(entry_company_id.get())
    driver.find_element_by_id ('username').send_keys(entry_username.get())
    driver.find_element_by_id ('password').send_keys(entry_password.get())
    driver.find_element_by_id('log-in').click()
    # Verify login was successfull
    try:
        WebDriverWait(driver, 10).until(EC.title_contains("בית | ShiftOrganizer"))
        label_bad_login.forget()
        label_logged_successfully.grid(row=8, column=1)
        labels_list.append(label_logged_successfully)
    except TimeoutException:
        label_logged_successfully.forget()
        label_bad_login.grid(row=8, column=1)
        labels_list.append(label_bad_login)
    
    # print(driver.get_cookies())
    cookies_before = driver.get_cookies()
    sessionid_name = cookies_before[0]['name']
    sessionid_value = cookies_before[0]['value']
    csrftoken_name = cookies_before[1]['name']
    csrtoken_value = cookies_before[1]['value']
    cookies = {sessionid_name: sessionid_value, csrftoken_name: csrtoken_value}
    
    # Getting employees details
    result = requests.get('https://app.shiftorganizer.com/api/employees/', cookies = cookies).json()
    employees = {}
    usernames = []
    # Saving Users details
    for user in result:
        user_name = user['user']['username']
        employees[user_name] = {}
        usernames.append(user_name)
        employees[user_name]['employee_id'] = user['id']
        employees[user_name]['user_id'] = user['user']['id']


    # Getting next weeek shifts
    if checkbox_var.get() == 1:
        try:
            result = requests.get(f'https://app.shiftorganizer.com/api/rotas/?date={next_sunday_date}', cookies = cookies).json()
            rota_id = result[0]['id']
        except IndexError:
            label_no_shifts_found.grid(row = 9, column = 1)
            labels_list.append(label_no_shifts_found)
    else:
        try:
            result = requests.get(f'https://app.shiftorganizer.com/api/rotas/?date={this_sunday_date}', cookies = cookies).json()
            rota_id = result[0]['id']
        except IndexError:        
            label_no_shifts_found.grid(row = 9, column = 1)
            labels_list.append(label_no_shifts_found)
    user_id = employees[entry_username.get()]['employee_id']
    user_shifts = requests.get(f'https://app.shiftorganizer.com/api/cells/?rota={rota_id}&employee={user_id}', cookies = cookies).json()
    
    for shifts in user_shifts:
        date = shifts['date']
        if shifts_for_the_week.get(date) is None:
            shifts_for_the_week[date] = {}
            shifts_for_the_week[date]['start'] = shifts['planned_start']
            shifts_for_the_week[date]['end'] = shifts['planned_end']
            shifts_for_the_week[date]['notes'] = shifts['notes']
        else:
            new_date = f'{date}_2'
            shifts_for_the_week[new_date] = {}
            shifts_for_the_week[new_date]['start'] = shifts['planned_start']
            shifts_for_the_week[new_date]['end'] = shifts['planned_end']
            shifts_for_the_week[new_date]['notes'] = shifts['notes']
    
    def check_asia_shift_and_convert_to_iso_time(date_str, time_start_str, time_end_str):
        start_time_obj = datetime.strptime(f'{date_str} {time_start_str}', '%Y-%m-%d %H:%M:%S')
        end_time_obj = datetime.strptime(f'{date_str} {time_end_str}', '%Y-%m-%d %H:%M:%S')
        if start_time_obj > end_time_obj:
            start_time_obj = start_time_obj - timedelta(days = 1)
        iso_start_time = start_time_obj.isoformat()
        iso_end_time = end_time_obj.isoformat()
        return iso_start_time, iso_end_time
    
    # Clean up Shifts Dates and create calendar events
    write_to_calendar = calendar_api.PostToGoogleCalendar()
    for date, shift in shifts_for_the_week.items():
        if date.endswith('_2'):
            date = date[:-2]
        iso_start_time, iso_end_time = check_asia_shift_and_convert_to_iso_time(date, shift['start'], shift['end'])
        desc = shift['notes']
        
        event = {
            'summary': 'משמרת',
            'description': desc,
                'start': {
                'dateTime': iso_start_time,
                'timeZone': 'Asia/Jerusalem',
            },
            'end': {
                'dateTime': iso_end_time,
                'timeZone': 'Asia/Jerusalem',
            },
            'reminders': {
                'useDefault': True,
        },
        }
        write_to_calendar.create_event(event)
        label_event_complete.grid(row = 9, column = 1)
        labels_list.append(label_event_complete)

        
login_gui()

