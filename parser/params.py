import os
from dotenv import load_dotenv
from selenium import webdriver


load_dotenv()
LOGIN_PAGE = "https://lks.siriusuniversity.ru/login"
SCHEDULE_PAGE = "https://lks.siriusuniversity.ru/schedule/groups/list"
CSV_FILE_NAME = "data/schedule.csv"
HTML_FILE_NAME = "data/sirius.html"
LOGIN = os.environ.get("LOGIN")
PASSWORD = os.environ.get("PASSWORD")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": "./",
    "download.prompt_for_download": True,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": False
})

driver = webdriver.Chrome(options=chrome_options)