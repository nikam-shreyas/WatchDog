from selenium import webdriver
from selenium.webdriver.common.by import By

from pywebio.input import *
import ssl
from mailjet_rest import Client

# Get your credentials from mailjet
API_KEY = '<YOUR_API_KEY>'
API_SECRET = '<YOUR_API_SECRET>'
CONTEXT = ssl.create_default_context()
URL = 'https://searchneu.com/NEU/202330/search/7150'
DRIVER_PATH = 'chromedriver'
FILEPATH = 'state.txt'
ACCESS_TOKEN = '<YOUR_ACCESS_TOKEN>'


def send_mail():
    mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "nik4m.5hreyas@gmail.com",
                    "Name": "SHREYAS"
                },
                "To": [
                    {
                        "Email": "adityamkawale@gmail.com",
                        "Name": "SHREYAS"
                    }
                ],
                "Subject": "Course Seat Update Notification.",
                "TextPart": "The course seats have changed",
                "HTMLPart": "Check your course registration stats at <a href='" + URL + "'>Course Update</a>",
                "CustomID": "WatchDogTest"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print('Mail sent')
    # print(result.status_code)
    # print(result.json())


def get_new_state():
    driver = webdriver.Chrome()
    driver.get(URL)
    seats = driver.find_element(By.XPATH,
                                '//*[@id="__next"]/div/div[3]/div[3]/div[2]/div/div/div/div[1]/table/tbody/tr/td[5]')
    return seats.text


def did_state_change(old_state, new_state):
    return old_state != new_state


def get_old_state(filepath):
    with open(filepath, 'r') as file:
        content = file.readlines()
    return '\n'.join([i.strip() for i in content])


def update_old_state(new_state, filepath):
    with open(filepath, 'w') as file:
        file.write(new_state)


def run_watchdog():
    old_state = get_old_state(FILEPATH)
    new_state = get_new_state()
    print(new_state, old_state)
    # print(did_state_change(old_state, new_state))
    if did_state_change(old_state, new_state):
        update_old_state(new_state, FILEPATH)
        send_mail()
