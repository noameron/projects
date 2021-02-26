import os
import time
import datetime
import pandas as pd
from tkinter import *
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


download_dir = "C:\\Users\\Noam\\Documents\\Python Scripts\\projects\\shifts_script"
driver_path = "C:\\Users\\Noam\\Documents\\Python Scripts\\projects\\shifts_script\\chromedriver.exe"
shiftorgnizer_login_url = 'https://app.shiftorganizer.com/login/?lang=he&previous=homepage&greeting=true'
excel_download_url = 'https://app.shiftorganizer.com/app/rota'

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
    global label_file_success
    # global bad_input
    checkbox_var = IntVar()
    
    # Text near text boxes
    # Or other labels
    label_company_id = Label(root, text='Company ID: ')
    label_username = Label(root, text='Username: ')
    label_password = Label(root, text='Password: ')
    label_file_success = Label(root, text='\nFile Downloaded Successfully!')
    label_welcome = Label(root, text='\nPlease enter your ShiftOrganizer credentials: \n')
    # bad_input = Label(root, text='ERROR! \nEither Company ID is not a number / Username is not characters')
    
    # Textboxe entries
    default_compny_id_var = StringVar(root, value='132')
    entry_company_id = Entry(root, textvariable=default_compny_id_var)
    entry_username = Entry(root)
    entry_username.focus()
    entry_password = Entry(root)

    # Positioning of labels
    label_welcome.grid(row=0, column=1, sticky=W)
    label_company_id.grid(row=1, sticky=E)
    label_username.grid(row=2, sticky=E)
    label_password.grid(row=3, sticky=E)
    
    # Positioning of textboxes
    entry_company_id.grid(row=1, column=1)
    entry_username.grid(row=2, column=1)
    entry_password.grid(row=3, column=1) 

    # Login button
    root.bind('<Return>', site_login)
    b = Button(root, text='Login', command=site_login)
    b.grid(row=6, column=1)
    checkbox = Checkbutton(root, text='Get next week Shifts', variable=checkbox_var)
    checkbox.grid(row=4, column=1)
    root.mainloop()

# Site login with user's credentials
current_day_date = datetime.date.today()
next_sunday_date = current_day_date + datetime.timedelta( (6 - current_day_date.weekday()) % 7 )
next_sunday = str(next_sunday_date)
def site_login():

    driver.get (shiftorgnizer_login_url)
    driver.implicitly_wait(20)
    driver.find_element_by_id('company').send_keys(entry_company_id.get())
    driver.find_element_by_id ('username').send_keys(entry_username.get())
    driver.find_element_by_id ('password').send_keys(entry_password.get())
    driver.find_element_by_id('log-in').click()
    
    try:
        if WebDriverWait(driver, 10).until(EC.title_contains("בית | ShiftOrganizer")):
            enable_download(driver)
            driver.get(excel_download_url)
            if checkbox_var.get() == 1:
                driver.get(excel_download_url+'?date='+next_sunday)
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.btn-block"))).click()
            else:
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.btn-block"))).click()
            if isFileDownloaded():
                # bad_input.grid_forget()
                label_file_success.grid(row=8, column=1)
    except TimeoutException as EX:
        messagebox.showerror("Error", 'Wrong combination of Username / Password / Company ID')
        # driver.find_element_by_css_selector("#alert #alert-message")
        # bad_input.grid(row=8, column=1)

# permission to download file via Selenium
def enable_download(driver):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.execute("send_command", params)

# check if file has been downloaded
def isFileDownloaded():
    file_path = download_dir+"\\schedule.xlsx"
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.isfile(file_path):
        return True

login_gui()

# if __name__ == '__main__':
#     enable_download(driver)
#     WebDriverWait(driver, 10).until(EC.title_contains("בית | ShiftOrganizer"))
#     driver.get('https://app.shiftorganizer.com/app/rota')
#     WebDriverWait(driver, 10).until(EC.title_contains("סידור | ShiftOrganizer"))
#     driver.get(excel_shifts_download_url)
#     isFileDownloaded()


df = pd.read_excel(r'C:\Users\Noam\Downloads\schedule.xlsx', header=3, usecols="B:M")

# name columns by dates only
header_list = []
for coulmn_header, column_data in df.iteritems():
    header_list.append(coulmn_header[3:16])
# add START to columns with shift's start time
for index, value in enumerate(header_list):
    if index % 2 != 0:
        header_list[index] = header_list[index-1] + ' START'
# add END to columns with shift's start time
for index, value in enumerate(header_list):
    if index % 2 == 0:
        header_list[index] += ' END'
# Create a list of all column with current weeks dates
df.columns = header_list

# Fill names on 'dd/mm/yyyy START' columns, and fill NaN values
for index, value in enumerate(header_list[:-1]):
    df[header_list[index+1]] = df[header_list[index+1]].fillna(value=df[header_list[index]])
df = df.fillna('--')

# Appending users shifts for the week to shifts_for_the_week dict

shifts_for_the_week = {}
shifts_for_the_week_no_duplicates = {}
for column, value in df.iteritems():
    date, start_or_end = column.split(' ')
    
    for index, cell in enumerate(value):
        if cell == 'עדי הלר':   
            
            if shifts_for_the_week.get(date) is None:
                shifts_for_the_week[date] = {}
            
            if shifts_for_the_week[date].get(start_or_end) is not None:
                new_date = f'{date}_2'
                if shifts_for_the_week.get(new_date) is None:
                    shifts_for_the_week[new_date] = {}
                shifts_for_the_week[new_date][start_or_end] = value[index + 1]
            
            else:
                shifts_for_the_week[date][start_or_end] = value[index + 1]

    # Remove events with same start and end time
    # This is used due to appending Name to END and START columns (line 155)
    for date, time in shifts_for_the_week.items():
        if time['END'] != time['START']:
            shifts_for_the_week_no_duplicates[date] = time

print(shifts_for_the_week_no_duplicates)



