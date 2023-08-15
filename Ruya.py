import requests
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
rs = RuyaScrapper()
with open("log.txt", "w", errors="replace") as log_file:
    print(rs.GetAllMangas(), file=log_file)