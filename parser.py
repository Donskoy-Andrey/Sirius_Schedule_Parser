import time
import pandas as pd
from typing import Optional
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


LOGIN_PAGE = "https://lks.siriusuniversity.ru/login"
SCHEDULE_PAGE = "https://lks.siriusuniversity.ru/schedule/groups/list"
LOGIN = "donskoi.com@gmail.com"
PASSWORD = "i9fdf>5/3B>/O(=8OIpx!"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": "./",
    "download.prompt_for_download": True,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": False
})

driver = webdriver.Chrome(options=chrome_options)


def login():
    driver.get(LOGIN_PAGE)

    # Login input
    username_input = driver.find_element(By.NAME, "email")
    username_input.clear()
    username_input.send_keys(LOGIN)

    # Password input
    password_input = driver.find_element(By.NAME, 'password')
    password_input.clear()
    password_input.send_keys(PASSWORD)

    # Click
    button = driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]")
    button.click()


def page(prev_month: bool = False, next_month: bool = False) -> Optional[str]:
    prev_page, next_page = driver.find_elements(
        By.XPATH,
        '//div[@class="mt-2 cursor-pointer"]/*[name()="svg"]'
    )

    if prev_month:
        prev_page.click()
        time.sleep(2)
        html = driver.page_source
        return html

    if next_month:
        next_page.click()
        time.sleep(2)
        html = driver.page_source
        return html


def parse_month(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find('div', class_='text-sm font-semibold text-indigo-600 ml-3 mt-2')
    text = element.get_text(strip=True)
    return text


login()
driver.get(SCHEDULE_PAGE)
time.sleep(2)
dfs = []

while True:
    html = page(next_month=True)
    month, year = parse_month(html).split()
    print(month, year)
    if (month == "Январь") and (year == "2024"):
        break

    if "Расписание на данный период отсутствует" in html:
        continue

    soup = BeautifulSoup(html, 'html.parser')

    all_date = [
        date.text.strip()
        for date in soup.find_all("div", class_="rasp-list-date flex")
    ]

    date_days = []
    date_months = []
    date_years = []
    for date in all_date:
        day, month, year = [int(i) for i in date.split(".")]
        date_days.append(day)
        date_months.append(month)
        date_years.append(year)

    all_day = [
        day.text.strip()
        for day in soup.find_all("div", class_="rasp-list-day flex")
    ]
    all_start = [
        start.text.strip()
        for start in soup.find_all("div", class_="rasp-list-start flex")
    ]
    all_end = [
        end.text.strip()
        for end in soup.find_all("div", class_="rasp-list-end flex")
    ]
    all_description = [
        description.text.strip()
        for description in soup.find_all("div", class_="rasp-list-discp flex")
    ]
    all_address = [
        address.text.strip()
        for address in soup.find_all("div", class_="rasp-list-address flex")
    ]
    all_room = [
        room.text.strip()
        for room in soup.find_all("div", class_="rasp-list-room flex")
    ]
    all_teachers = [
        teacher.text.strip()
        for teacher in soup.find_all("div", class_="rasp-list-teachers flex")
    ]

    df = pd.DataFrame({
        "День": date_days,
        "Месяц": date_months,
        "Год": date_years,
        "День недели": all_day,
        "Начало": all_start,
        "Окончание": all_end,
        "Дисциплина": all_description,
        "Адрес": all_address,
        "Аудитория": all_room,
        "Преподаватель": all_teachers,
    })
    dfs.append(df)

df = pd.concat(dfs)
df.to_csv("schedule.csv")