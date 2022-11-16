from WatchDog import send_mail, update_old_state, get_old_state
import requests
from bs4 import BeautifulSoup
from lxml import etree

CRN = '36519'
URL = "http://nb5840.neu.edu:9430/udcprod8/bwckschd.p_disp_detail_sched?term_in=####&crn_in=$$$$"
SPRING = "30"
FALL = "10"
SUMMER_2 = "60"
YEAR = "2023"
SUMMER_1 = "40"
SUMMER_FULL = "50"
TERM_CODES = {"FALL": "10", "SPRING": "30", "SUMMER_1": "40", "SUMMER_2": "60", "SUMMER_FULL": "50"}
FILEPATH = "state.txt"


def get_new_state(crn=CRN, year=YEAR, term=SPRING):
    term_code = year + term
    url = URL.replace("####", term_code).replace("$$$$", crn)
    # print(url)
    response = requests.get(url)
    assert response.status_code == 200, "Website Down!"
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    dom = etree.HTML(str(soup))
    # print(soup)
    tables = soup.find_all('table')[2].find('table')
    table_content = tables.text
    return table_content


def is_state_same(old_state, new_state):
    # print(new_state, old_state)
    # old_state = ' '.join([i.strip() for i in old_state])
    # print(old_state, new_state)
    old_state = old_state.replace('\n', ' ').replace(' ', '')
    new_state = new_state.replace('\n', ' ').replace(' ', '').replace(' ', '')
    # print(new_state)
    # print(old_state)
    return old_state == new_state


def run_watchdog(crn=CRN, year=YEAR, term=SPRING):
    new_state = get_new_state(crn, year, term)
    old_state = get_old_state(FILEPATH)
    if not is_state_same(old_state, new_state):
        send_mail()
        update_old_state(new_state, FILEPATH)
