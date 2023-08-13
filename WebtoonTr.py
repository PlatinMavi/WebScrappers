from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from bs4 import BeautifulSoup
import os
from PIL import Image
import pymongo
import traceback

class WebtoonScrapper():
    def __init__(self) -> None:

        self.client = pymongo.MongoClient("mongodb+srv://PlatinMavi:23TprQmteTiPJA6r@mangabridge.qceexb2.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["WebtoonTr"]
        self.collection = self.db["mangas"]
        self.chapter = self.db["chapters"]

    def GetTotalPages(self):
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")

        with Chrome(options=options) as driver:
            driver.get("https://webtoon-tr.com/webtoon/?m_orderby=alphabet")

            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "pages")))
            Lastpage = driver.find_element(By.CLASS_NAME, "pages").text
            Lastpage = int(Lastpage.split(" ")[1])
            print(Lastpage,"total pages")

        return Lastpage
    
    def GetAllMangas(self):
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")

        LastPage = self.GetTotalPages()
        Mangas = []
        with Chrome(options=options) as driver:
            for x in range(1, LastPage + 1):
                url = f"https://webtoon-tr.com/webtoon/page/{x}/?m_orderby=alphabet"
                driver.get(url)
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "item-thumb")))
                elements = driver.execute_script('return document.getElementsByClassName("item-thumb");')
                for html in elements:
                    soup = BeautifulSoup(html.get_attribute("outerHTML"), "html.parser")
                    link = soup.find("a").get("href")
                    browser = link.split("/")[-2]
                    title = soup.find("a").get("title")
                    image = soup.find("img").get("src")

                    f = {"Link": link, "name": title, "browser": browser, "image": image}

                    Mangas.append(f)
                print(f"({x} / {LastPage+1}) getting all mangas...")
        return Mangas
    
    def GetImages(self):
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")

        data = self.GetAllMangas()
        output_directory = "WebtoonTr"  # Directory to save the images
        os.makedirs(output_directory, exist_ok=True)

        with Chrome(options=options) as driver:
            for manga in data:
                try:
                    driver.get(manga["Link"])
                    image_name = manga["browser"]+"WebtoonTr" + ".png"  # You can customize the image name here
                    image_path = os.path.join(output_directory, image_name)

                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "loaded")))
                    image_element = driver.find_element(By.CLASS_NAME, "loaded")

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
                except ConnectionRefusedError:
                    print("Connection refused by the target machine. Skipping image download.")
                except Exception as e:
                    print("Error occurred while downloading image:", e)

        return print("Images downloaded successfully.")
    
    def InsertMangas(self):
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")

        data = self.GetAllMangas()
        # data = [{"Link":"https://webtoon-tr.com/webtoon/99-wooden-stick-3/","name":"Bug Train","image":"https://webtoon-tr.com/wp-content/uploads/bug-train.png","browser":"bug-train"}]
        total = len(data)
        index = 0
        with Chrome(options=options) as driver:
            for manga in data:
                try:
                    driver.get(manga["Link"])
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "summary-content")))

                    element = driver.execute_script('return document.getElementsByClassName("summary_content");')
                    soup = BeautifulSoup(element[0].get_attribute("outerHTML"), "html.parser")

                    allGenre = []
                    try:
                        desc = soup.find_all("div", {"class":"manga-excerpt"})[0].find_all("p")[1].contents[0]
                    except:
                        try:
                            desc = soup.find_all("div", {"class":"manga-excerpt"})[0].find_all("p")[0].contents[0]
                        except:
                            desc = ""
                            print("couldnt get description")
                    name = manga["name"]
                    image = manga["image"]
                    browser = manga["browser"]

                    genreC = soup.find("div",{"class":"genres-content"})
                    genre = genreC.find_all("a",{"rel":"tag"})
                    for b in genre:
                        g = b.contents[0]
                        if " "in g:
                            g.replace(" ","")
                            allGenre.append(g)
                        else:
                            allGenre.append(g)

                    ins = {"name":name,"image":image,"desc":desc,"category":allGenre,"browser":browser}

                    index = index+1

                    self.collection.insert_one(ins)
                    

                    print(f"({index}/{total}) , {ins['name']}")
                except:
                    print("i hate fucking cloudflare protected websites")

        return print("inserted")
    
    def InsertChapters(self):
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("start-maximized")
        # data = [{"Link":"https://webtoon-tr.com/webtoon/return-of-the-8th-class-magician-6/","name":"Bug Train","image":"https://webtoon-tr.com/wp-content/uploads/bug-train.png","browser":"99-wooden-stick-3"}]
        index = 0
        data = self.GetAllMangas()
        total = len(data)
        with Chrome(options=options) as driver:
            for manga in data:
                try:
                    driver.get(manga["Link"])
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "version-chap")))
                    element = driver.execute_script('return document.getElementsByClassName("version-chap");')
                    soup = BeautifulSoup(element[0].get_attribute("outerHTML"), "html.parser")

                    ins=[]

                    tag = soup.find_all("a")
                    for x in tag:         
                        try:
                            number = None
                            Query = self.collection.find_one({"browser":manga["browser"]})
                            link = x.get("href")
                            createdAt = datetime.datetime.now()
                            try:
                                content = str(x.contents[0])
                                try:
                                    number = int(content.strip().split(" ")[-1])
                                except:
                                        content = str(x.contents[0])
                                        p = content.split("\n")[1].strip()
                                        number = int(p.split(".")[0])
                                        
                            except:
                                try:
                                    number = ins[-1]["number"]-1

                                except:
                                    number = len(tag)

                            insert = {"number":number,"url":link,"manga":Query["_id"],"fansub":"WebtoonTr","createdAt":createdAt}
                            
                            ins.append(insert)
                        except Exception as e:
                            print(e)
                            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                            print(traceback_str)
                            print("this site is just dumb")
                    index = index+1

                    self.chapter.insert_many(ins)
                    
                    print(f"({index}/{total}) , {manga['name']}")
                except Exception as e:
                    print(e.__cause__)
                    traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                    print(traceback_str)
                    print("f this bro")



s = WebtoonScrapper()
print(s.GetTotalPages())