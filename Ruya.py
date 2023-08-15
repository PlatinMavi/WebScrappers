import requests
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

class RuyaScrapper:
    def __init__(self) -> None:
        pass

    def GetTotalPages(self):
        url =  "https://www.ruyamanga.com/?m_orderby=alphabet"

        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")
        with Chrome(options=options) as driver:
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "page-item-detail")))
            html = driver.find_element(By.CLASS_NAME, "c-page").get_attribute("innerHTML")
        
            soup = BeautifulSoup(html, "html.parser")

            lastpage = soup.find("a",{"class":"last"}).get("href").split("/")[-2]
            print(lastpage,"Total Pages")
            return lastpage
    
    def GetAllMangas(self):
        lastpage = self.GetTotalPages()
        mangas = []

        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")
        with Chrome(options=options) as driver:
            for page in range(1,int(lastpage)+1):
                url = f"https://www.ruyamanga.com/page/{page}/?m_orderby=alphabet"
                driver.get(url)
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "page-item-detail")))
                html = driver.find_element(By.CLASS_NAME, "c-page").get_attribute("innerHTML").encode("utf-8")

                soup = BeautifulSoup(html,"html.parser")
                manga = soup.find_all("div",{"class":"page-item-detail"})
                
                print("Page",page,"/",lastpage)

                for item in manga:
                    wrapper = item.find("a")
                    title = wrapper.get("title")
                    link = wrapper.get("href")
                    mangas.append({"name":title ,"link":link})

            return mangas
        
    def GetAllMangaData(self):
        data = self.GetAllMangas()
        # data = [{"name": "Reborn Ranker", "link":"https://www.ruyamanga.com/manga/reborn-ranker/"}]
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")

        returnies = []
        with Chrome(options=options) as driver:
            for manga in data :
                driver.get(manga["link"])
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "tab-summary")))
                html = driver.find_element(By.CLASS_NAME, "site-content").get_attribute("innerHTML").encode("utf-8")

                soup = BeautifulSoup(html, "html.parser")
                try:
                    browser = manga["link"].split("/")[-2]
                    title = soup.find("span",{"class":"rate-title"}).get("title")
                    desc = soup.find("div",{"class":"summary__content"}).text
                    category = []
                    genres = soup.find("div",{"class":"genres-content"}).find_all("a")

                    for genre in genres:
                        category.append(genre.text)

                    ins = {"name":title,"image":browser,"desc":desc,"category":category,"browser":browser}
                    returnies.append(ins)
                except:
                    print("Hata",manga["name"])
                
        return returnies
    

    def GetAllChapters(self):
        data = self.GetAllMangas()
        # data = [{"name": "Reborn Ranker", "link":"https://www.ruyamanga.com/manga/reborn-ranker/"}]
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")

        returnies = []
        with Chrome(options=options) as driver:
            for manga in data :
                insert = []
                driver.get(manga["link"])
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "listing-chapters_wrap")))
                html = driver.find_element(By.CLASS_NAME, "listing-chapters_wrap").get_attribute("innerHTML").encode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                try:
                    chapters = soup.find_all("a")
                    for chapter in chapters:

                        link = chapter.get("href")
                        num = chapter.text.strip().split(" ")[-1]
                        current_time = datetime.datetime.now()
                        ins = {"number":int(num),"url":link,"manga":manga["link"],"fansub":"RüyaManga","createdAt":current_time}

                        insert.append(ins)

                    returnies.append(insert)
                except:
                    print("Hata",manga["name"])
        
        return returnies

    
rs = RuyaScrapper()
with open("log.txt", "w", errors="replace") as log_file:
    print(rs.GetAllChapters(), file=log_file)