import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from fake_useragent import UserAgent
from bs4 import BeautifulSoup

user_agent = UserAgent()
options = Options()
ua = UserAgent()
user_agent_random = ua.random
options.add_argument(f'user-agent={user_agent_random}')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
url = 'https://auto.ru/cars/bmw/all/'


def parsing_actions(url: str) -> None:
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'confirm-button'))
    )

    confirmation_button = driver.find_element(by=By.ID, value='confirm-button')
    confirmation_button.click()

    car_summaries = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'ListingItem__summary'))
    )

    links_to_visit = [
        summary.find_element(by=By.TAG_NAME, value='a').get_attribute('href') for summary in car_summaries
    ]

    for link in links_to_visit:
        driver.get(link)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        title = soup.select_one('.CardHead__title')
        year = soup.select_one('.CardInfoRow_year .Link')
        body_type = soup.select_one('.CardInfoRow_bodytype .Link')
        color = soup.select_one('.CardInfoRow_color .Link')
        if year is not None:
            print(title.text)
            print(year.text)
            print(body_type.text)
            print(color.text)
    time.sleep(10)


try:
    parsing_actions(url)
except Exception as ex:
    print(ex)
    input("Пожалуйста, введите капчу вручную и нажмите Enter...")
    try:
        parsing_actions(url)
    except Exception as ex2:
        print(ex2)
finally:
    driver.close()
    driver.quit()
