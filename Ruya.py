import requests
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from PIL import Image
import os

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
    
    def GetMangaImage(self):
        # data = self.GetAllMangas()
        data = [{"name": "Reborn Ranker", "link":"https://www.ruyamanga.com/manga/reborn-ranker/"}]

        options = ChromeOptions()
        options.add_argument('--head')
        options.add_argument("start-maximized")

        output_directory = "Temp"  # Directory to save the images
        os.makedirs(output_directory, exist_ok=True)

        returnies = []
        with Chrome(options=options) as driver:
            for manga in data :
                driver.get(manga["link"])
                image_name = manga["link"].split("/")[-2]+"Ruya" + ".png"  # You can customize the image name here
                image_path = os.path.join(output_directory, image_name)

                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_image")))
                image_element = driver.find_element(By.CLASS_NAME, "summary_image").find_element(By.TAG_NAME, "img")

                driver.execute_script("window.scrollTo(0,300)")
                image_location = image_element.location
                image_size = image_element.size
                driver.save_screenshot(image_path)

                viewport_height = driver.execute_script("return window.innerHeight;")
                scroll_position = driver.execute_script("return window.pageYOffset;")

                cropped_top = max(0, image_location['y'] - scroll_position)
                cropped_bottom = min(viewport_height, image_location['y'] + image_size['height'] - scroll_position)

                cropped_image = Image.open(image_path).crop((image_location['x'], cropped_top, 
                                                            image_location['x'] + image_size['width'], 
                                                            cropped_bottom))
                cropped_image.save(image_path)
                print(f"Image saved: {image_path}")

        

    
rs = RuyaScrapper()
# with open("log.txt", "w", errors="replace") as log_file:
#     print(rs.GetAllChapters(), file=log_file)
rs.GetMangaImage()