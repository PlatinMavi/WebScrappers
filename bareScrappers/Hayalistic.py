import pymongo
import requests
from bs4 import BeautifulSoup
import datetime
import os
import urllib.request
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HayalisticScrapper():
    def __init__(self) -> None:
        pass

    def GetLastPage(self):
        url = "https://hayalistic.com.tr/webtoonlar/?m_orderby=alphabet"
        html = requests.get(url).content.decode("utf-8",errors="ignore")
        soup = BeautifulSoup(html,"html.parser")
        lastPage = soup.find("a",{"class":"last"}).get("href").split("/")[-2]
        return lastPage
    
    def GetAllMangas(self):
        lastpage = self.GetLastPage()

        allMangas = []

        for number in range(1,int(lastpage)+1):
            url = f"https://hayalistic.com.tr/webtoonlar/page/{number}/?m_orderby=alphabet"
            html = requests.get(url).content.decode("utf-8",errors="ignore")
            soup = BeautifulSoup(html,"html.parser")
            mangas = soup.find_all("div",{"class":"item-thumb"})
            for links in mangas:
                aTag = links.find("a")
                title = aTag.get("title")
                link = aTag.get("href")
                image = aTag.find("img").get("data-src")
                
                allMangas.append({"title":title,"link":link,"image":image})
        return allMangas
    
    def GetAllMangasData(self):
        data = self.GetAllMangas()
        # data = [{"link":"https://hayalistic.com.tr/manga/zindan-sifirlanmasi/","title":"Zindan Sıfırlanması"}]
        index = 0
        total = len(data)
        returnies = []

        for links in data:
            link = links["link"]
            html = requests.get(link).content.decode("utf-8",errors="ignore")
            soup = BeautifulSoup(html,"html.parser")
            categoryFinder = soup.find("div",{"class":"genres-content"})
            category = []
            browser = link.split("/")[-2]
            try:
                desc = soup.find("div",{"class":"summary__content"}).find_all("p")[0].contents[0]
            except:
                desc = ""
                print("no description")

            for x in categoryFinder.find_all("a"):
                ct = x.contents[0]
                category.append(ct)

            index = index+1
            ins = {"name":links["title"],"image":browser+".png","desc":desc,"category":category,"browser":browser,"fansub":"Hayalistic"}
            print("(",index,"/",total,")",links["title"])
            try:
                returnies.append(ins)
            except:
                returnies.append({"name":links["title"],"image":browser+".png","desc":"","category":category,"browser":browser,"fansub":"Hayalistic"})
        return returnies
    
    def GetAllChapters(self):
        data = self.GetAllMangas()
        # data = [{"link":"https://hayalistic.com.tr/manga/a-bittersweet-couple/","browser":"a-bittersweet-couple","title":"b"}]
        total = len(data)
        index = 0
        options = ChromeOptions()
        options.add_argument('--headless')
        hata = []
        returnies = []

        with Chrome(options=options) as driver:
            for manga in data:
                try:
                    ins = []
                    
                    url = manga["link"]
                    driver.get(url)
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "wp-manga-chapter")))
                    elements = driver.execute_script('return document.getElementsByClassName("wp-manga-chapter");')

                    browser = url.split("/")[-2]
        
                    for chapter in elements:
                        soup = BeautifulSoup(chapter.get_attribute("outerHTML"), "html.parser")
                        aTag = soup.find("a")
                        link = aTag.get("href")
                        try:   
                            if len(link.split("/")[-2].split("-")) >= 3:
                                number = float(link.split("/")[-2].split("-")[1]+"."+link.split("/")[-2].split("-")[2])
                            else:
                                number = int(link.split("/")[-2].split("-")[-1])
                        except:
                            number = int(link.split("/")[-2].split("-")[-2])
                            
                        v = datetime.datetime.now()
                        inserted = {"number":number,"url":link,"manga":url.split("/")[-2],"fansub":"Hayalistic","createdAt":v}
                        ins.append(inserted)

                    index = index+1
                    print("(",index,"/",total,")",manga["title"])
                    returnies.append(ins)
                except:
                    hata.append(manga["title"])
        return returnies
    
    def ScrapeImages(self):
    
        def download_image(url, filename):
            response = requests.get(url)
            response.raise_for_status()
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Downloaded image: {filename}")

        data = self.GetAllMangas()
        # data = [{"image":"https://hayalistic.com.tr/wp-content/uploads/2023/06/1583362974000-193x278.jpg","link":"https://hayalistic.com.tr/manga/zindan-sifirlanmasi/"}]
        
        output_directory = "Hayalistic"

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for image in data:
            url = image["image"]
            filename = os.path.join(output_directory, image["link"].split("/")[-2])
            download_image(url, filename+".png")
# 24 manga
# hata : ['Altın Çağ', 'Back to You', 'Büyü İmparatoru', 'Cadıyı Salın', 'Çok Yönlü Büyücü', 'Days of Hana', 'Devil’s Romance', 'Don’t Concern Yourself With That Book', 'Görünüşçülük', 'I Love Yoo', 'Köpek Olmak İçin Güzel Bir Gün', 'Let’s Play', 'Marriage Alliance for Revenge', 'Nasıl Dövüşürsün?', 'Nickelodeon Avatar The Last Airbender – The Lost Adventures', 'Nihayetin Ardındaki Başlangıç', 'Olympus', 'Siyah Bir Ejder Yetiştirdim', 'The Dilettante', 'The Snake and The Flower', 'Tıbbi Dönüşüm', 'Uriah', 'Yaş Önemlidir', 'Yeniden Evlenen İmparatoriçe']
# print(HayalisticScrapper().GetAllMangasData())