from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import datetime
from PIL import Image

class MangazureScrapper():
    def __init__(self) -> None:
        pass

    def GetLastPage(self):
        url = "https://www.mangazure.com/search/label/T%C3%BCm%C3%BC"

        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")
        with Chrome(options=options) as driver:
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "content-out")))
            html = driver.find_element(By.CLASS_NAME, "content-out").get_attribute("innerHTML")

            soup = BeautifulSoup(html, "html.parser")
            lastpage = soup.find("div", {"class":"p-nav-right"}).text.strip().split(" ")[1]
        return int(lastpage)
    
    def GetAllMangas(self):
        data = self.GetLastPage()
        # data = 1

        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")

        returnies = []
        with Chrome(options=options) as driver:
            for page in range(1,data+1):
                url = f"https://www.mangazure.com/search/label/T%C3%BCm%C3%BC?p={page}"
                driver.get(url)
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "content-out")))
                html = driver.find_element(By.CLASS_NAME, "content-out").get_attribute("innerHTML")
                soup = BeautifulSoup(html, "html.parser")

                mangas = soup.find_all("div",{"class":"item-box"})
                for manga in mangas:
                    title = manga.text
                    link = "https://www.mangazure.com"+manga.find("a").get("href")
                    returnies.append({"name":title ,"link":link})
        return returnies
    
    def GetAllMangaData(self):
        data = self.GetAllMangas()
        # data = [{"name":"Dragon-Devouring Mage","link":"https://www.mangazure.com/dragondevouring-mage"}]

        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")

        returnies = []
        with Chrome(options=options) as driver:
            for manga in data:
                driver.get(manga["link"])
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "manga-detail")))
                html = driver.find_element(By.CLASS_NAME, "manga-detail").get_attribute("innerHTML")
                soup = BeautifulSoup(html, "html.parser")

                browser = manga["link"].split("/")[-1]
                desc = soup.find("div",{"class":"mdr-desc"}).text
                category= []
                genres = soup.find("span",{"class":"mdl-tur"}).find_all("a")
                for genre in genres:
                    category.append(genre.text)

                returnies.append({"name":manga["name"],"image":browser,"desc":desc,"category":category,"browser":browser})
        return returnies
    
    def GetAllChapters(self):
        data = self.GetAllMangas()
        # data = [{"name":"Dragon-Devouring Mage","link":"https://www.mangazure.com/dragondevouring-mage"}]

        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")

        returnies = []
        with Chrome(options=options) as driver:
            for manga in data:
                driver.get(manga["link"])
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "mdr-list")))
                html = driver.find_element(By.CLASS_NAME, "mdr-list").get_attribute("innerHTML")
                soup = BeautifulSoup(html, "html.parser")
                insert = []

                chapters = soup.find_all("li")
                for chapter in chapters:
                    anchor = chapter.find("a")
                    link = anchor.get("href")
                    num = anchor.text.strip().split(" ")[-1]
                    current_time = datetime.datetime.now()
                    insert.append({"number":int(num),"url":link,"manga":manga["link"],"fansub":"Mangazure","createdAt":current_time})
                returnies.append(insert)
        return returnies
    
    def GetMangaImage(self):
        data = self.GetAllMangas()
        # data = [{"name":"Dragon-Devouring Mage","link":"https://www.mangazure.com/dragondevouring-mage"}]

        options = ChromeOptions()
        options.add_argument('--head')
        options.add_argument("start-maximized")

        output_directory = "Temp"  # Directory to save the images
        os.makedirs(output_directory, exist_ok=True)

        with Chrome(options=options) as driver:
            for manga in data :
                driver.get(manga["link"])
                image_name = manga["link"].split("/")[-1]+"Mangazure" + ".png"  # You can customize the image name here
                image_path = os.path.join(output_directory, image_name)

                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "mdl-img")))
                image_element = driver.find_element(By.CLASS_NAME, "mdl-img")

                # driver.execute_script("window.scrollTo(0,300)")
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
    

# ms = MangazureScrapper()
# logger = ms.GetMangaImage()
# with open("log.txt", "w", errors="replace") as log_file:
#     print(logger, file=log_file)