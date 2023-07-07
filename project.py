from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import os
from PIL import Image

class WebtoonScrapper():
    def __init__(self) -> None:
        pass

    def GetTotalPages(self):
        options = ChromeOptions()
        options.add_argument('--headless')

        with Chrome(options=options) as driver:
            driver.get("https://webtoon-tr.com/webtoon/?m_orderby=alphabet")

            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "pages")))
            Lastpage = driver.find_element(By.CLASS_NAME, "pages").text
            Lastpage = int(Lastpage.split(" ")[1])
            print(Lastpage)

        return Lastpage
    
    def GetAllMangas(self):
        options = ChromeOptions()
        options.add_argument('--headless')

        LastPage = self.GetTotalPages()
        Mangas = []
        with Chrome(options=options) as driver:
            for x in range(1, LastPage + 1):
                url = f"https://webtoon-tr.com/webtoon/page/{x}/?m_orderby=alphabet"
                driver.get(url)
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "item-thumb")))
                elements = driver.execute_script('return document.getElementsByClassName("item-thumb");')
                for html in elements:
                    soup = BeautifulSoup(html.get_attribute("outerHTML"), "html.parser")
                    link = soup.find("a").get("href")
                    browser = link.split("/")[-2]
                    title = soup.find("a").get("title")
                    image = soup.find("img").get("src")
                    Mangas.append({"Link": link, "Title": title, "Browser": browser, "Image": image})
        return Mangas
    
    def GetImages(self):
        options = ChromeOptions()
        options.add_argument('--headless')

        data = self.GetAllMangas()
        output_directory = "WebtoonTr"  # Directory to save the images
        os.makedirs(output_directory, exist_ok=True)

        with Chrome(options=options) as driver:
            for manga in data:
                try:
                    driver.get(manga["Link"])
                    image_name = manga["Browser"] + ".png"  # You can customize the image name here
                    image_path = os.path.join(output_directory, image_name)

                    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "loaded")))
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

s = WebtoonScrapper()
s.GetImages()
