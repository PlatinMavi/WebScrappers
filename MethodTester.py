import requests
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# html = requests.get("https://www.ruyamanga.com/manga/page/1/?m_orderby=alphabet").content.decode("utf-8", errors="ignore")
# soup = BeautifulSoup(html, "html.parser")

options = ChromeOptions()
options.add_argument('--headless')
options.add_argument("start-maximized")
with Chrome(options=options) as driver:
    driver.get("https://www.ruyamanga.com/manga/page/1/?m_orderby=alphabet")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "page-item-detail")))
    logger = driver.find_element(By.CLASS_NAME, "c-page").text

# logger = []

# manga = soup.find_all("div",{"class":"page-item-detail"})
# for item in manga:
#     wrapper = item.find("a")
#     title = wrapper.get("title")
#     link = wrapper.get("href")

#     logger.append({"name":title ,"link":link})

with open("log.txt", "w", errors="replace") as log_file:
    # Use the file object as the 'file' parameter in the print function
    print(logger, file=log_file)