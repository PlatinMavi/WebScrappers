import requests
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# html = requests.get("https://www.ruyamanga.com/manga/page/1/?m_orderby=alphabet").content.decode("utf-8", errors="ignore")
# soup = BeautifulSoup(html, "html.parser")

def TestRequests():
    url = "https://clover-manga.com"
    html = requests.get(url).content.decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()

def TestSelenium():
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("start-maximized")
    with Chrome(options=options) as driver:
        driver.get("https://www.mangazure.com/search/label/T%C3%BCm%C3%BC")
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "full-page")))
        html = driver.find_element(By.CLASS_NAME, "full-page").get_attribute("innerHTML")

        soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()

logger = TestRequests()

with open("log.txt", "w", errors="replace") as log_file:
    print(logger, file=log_file)