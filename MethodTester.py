import requests
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests_html import HTMLSession

# html = requests.get("https://www.ruyamanga.com/manga/page/1/?m_orderby=alphabet").content.decode("utf-8", errors="ignore")
# soup = BeautifulSoup(html, "html.parser")

def TestRequests():
    url = "https://mangaokutr.com/manga/list-mode/"
    html = requests.get(url).content.decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()

def TestSelenium():
    options = ChromeOptions()
    options.add_argument('--head')
    options.add_argument("start-maximized")
    with Chrome(options=options) as driver:
        driver.get("https://mangaokutr.com/manga/list-mode/")
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "soralist")))
        html = driver.find_element(By.CLASS_NAME, "soralist").get_attribute("innerHTML")

        soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()


def TestRequestsHTML():
    session = HTMLSession()
    url = "https://mangaokutr.com/manga/list-mode/"
    response = session.get(url)
    response.html.render()
    return response.html.html

logger = TestSelenium()

with open("log.txt", "w", errors="replace") as log_file:
    print(logger, file=log_file)