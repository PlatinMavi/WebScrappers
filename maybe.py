import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

class MangaSehriScrapper:
    def __init__(self):
        self.geckodriver_path = "C:/Users/PC/Desktop/Scrapper/geckodriver.exe"
        self.firefox_binary_path = "C:/Program Files/Mozilla Firefox/firefox.exe"
        self.user_agent = "sec-ch-ua-full-version-list:"


    def GetTotalPages(self):
        options = FirefoxOptions()
        options.headless = True

        profile = FirefoxProfile()
        profile.set_preference("general.useragent.override", self.user_agent)

        with Firefox(options=options, firefox_profile=profile) as driver:
            driver.get("https://mangasehri.com/manga/?m_orderby=alphabet")
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "pages")))
            Lastpage = driver.find_element(By.CLASS_NAME, "pages").text
            Lastpage = int(Lastpage.split(" ")[1])
            print(Lastpage, "total pages")

        return Lastpage

    def GetAllMangas(self):
        lastpage = self.GetTotalPages()
        options = FirefoxOptions()
        options.headless = True

        profile = FirefoxProfile()
        profile.set_preference("general.useragent.override", self.user_agent)

        mangas = []

        with Firefox(options=options, firefox_profile=profile) as driver:
            for num in range(1, lastpage + 1):
                url = f"https://mangasehri.com/manga/page/{num}/?m_orderby=alphabet"
                driver.get(url)

                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "item-thumb")))
                elements = driver.execute_script("return document.getElementsByClassName('item-thumb');")
                for element in elements:
                    soup = BeautifulSoup(element.get_attribute("outerHTML"), "html.parser")
                    Tag = soup.find("a")

                    link = Tag.get("href")
                    title = Tag.get("title")
                    image = soup.find("img").get("src")
                    mangas.append({"link": link, "title": title, "image": image})

        return mangas

    def InsertMangas(self):
        # data = self.GetAllMangas()
        data = [{"title": "A Way To Protect You, Sweetheart", "link": "https://mangasehri.com/manga/a-way-to-protect-you-sweetheart-2/"}]
        options = FirefoxOptions()
        options.headless = True

        profile = FirefoxProfile()
        profile.set_preference("general.useragent.override", self.user_agent)

        # Set geckodriver path as system property
        os.environ["webdriver.gecko.driver"] = self.geckodriver_path

        with Firefox(options=options, firefox_profile=profile) as driver:
            for manga in data:
                driver.get(manga["link"])
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "tab-summary")))
                elements = driver.execute_script("return document.getElementsByClassNamr('more')")
                print(elements)

ms = MangaSehriScrapper()
print(ms.InsertMangas())
