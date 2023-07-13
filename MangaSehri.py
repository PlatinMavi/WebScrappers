import pymongo
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
import requests
from bs4 import BeautifulSoup
import datetime
import os

class MangaSehriScrapper():
    def __init__(self) -> None:
        pass

    def GetTotalPages(self):
        options = ChromeOptions()
        options.add_argument('--head')
        # options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("start-maximized")
        options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"')

        with Chrome(options=options) as driver:
           
            driver.get("https://mangasehri.com/manga/?m_orderby=alphabet")

            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "pages")))
            Lastpage = driver.find_element(By.CLASS_NAME, "pages").text
            Lastpage = int(Lastpage.split(" ")[1])
            print(Lastpage,"total pages")

        return Lastpage
    
    def GetAllMangas(self):
        lastpage = self.GetTotalPages()
        options = ChromeOptions()
        options.add_argument('--head')
        mangas = []

        with Chrome(options=options) as driver:
            
            for num in range(1,lastpage+1):
                url = f"https://mangasehri.com/manga/page/{num}/?m_orderby=alphabet"
                driver.get(url)

                WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"item-thumb")))
                elements = driver.execute_script("return document.getElementsByClassName('item-thumb');")
                for element in elements:
                    soup = BeautifulSoup(element.get_attribute("outerHTML"), "html.parser")
                    Tag = soup.find("a")
                    
                    link = Tag.get("href")
                    title = Tag.get("title")
                    image = soup.find("img").get("src")
                    mangas.append({"link":link,"title":title,"image":image})
        return mangas
    
    def InsertMangas(self):
        # data = self.GetAllMangas()
        data = [{"title":"A Way To Protect You, Sweetheart","link":"https://mangasehri.com/manga/a-way-to-protect-you-sweetheart-2/"}]
        options = ChromeOptions()
        options.add_argument('--headless')

        with Chrome(options=options) as driver:
           
            for manga in data:
                driver.get(manga["link"])
                WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"tab-summary")))
                elements = driver.execute_script("return document.getElementsByClassNamr('more')")
                print(elements)
    
# ms = MangaSehriScrapper()
# print(ms.GetTotalPages())

driver = Driver(uc=True)
driver.get("https://mangasehri.com/manga/?m_orderby=alphabet")
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "pages")))