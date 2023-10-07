import requests 
import os
from bs4 import BeautifulSoup
import datetime

class Clover():
    def __init__(self) -> None:
        pass

    def GetLastPage(self):
        url = "https://clover-manga.com/manga/?m_orderby=alphabet"
        html = requests.get(url).content.decode("utf-8", errors="ignore")
        soup  = BeautifulSoup(html,"html.parser")
        lastpage = soup.find("span",{"class":"pages"}).text.strip().split(" ")[1]
        return int(lastpage)
    
    def GetAllManga(self):
        data = self.GetLastPage()
        # data = 1
        returnies = []
        for page in range(1,data+1):
            url = f"https://clover-manga.com/manga/page/{page}/?m_orderby=alphabet"
            html = requests.get(url).content.decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")

            mangas = soup.find_all("div",{"class":"page-item-detail"})
            for manga in mangas:
                anchor = manga.find("a")
                title = anchor.get("title")
                image = anchor.find("img").get("src")
                link = anchor.get("href")
                returnies.append({"name":title,"image":image,"link":link})
        return returnies

    def GetAllMangaData(self):
        data = self.GetAllManga()
        # data = [{'name': '+99 Tahta çubuk', 'image': 'https://clover-manga.com/wp-content/uploads/BDC3B8AEC1EE_C7A5C1F6_690x1000-1-193x278-1-2476-175x238.jpg', 'link': 'https://clover-manga.com/manga/99-tahta-cubuk/'}]
        returnies = []
        
        for manga in data:
            html = requests.get(manga["link"]).content.decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")

            browser = manga['link'].split("/")[-2]
            desc = soup.find("div",{"class":"summary__content"}).text.replace("\n","")
            category = []
            genres = soup.find("div",{"class":"genres-content"}).find_all("a")
            for genre in genres:
                category.append(genre.text)

            returnies.append({"name":manga["name"],"image":browser,"desc":desc,"category":category,"browser":browser})
        return returnies
    
    def GetAllChapter(self):
        data = self.GetAllManga()
        # data = [{'name': '+99 Tahta çubuk', 'image': 'https://clover-manga.com/wp-content/uploads/BDC3B8AEC1EE_C7A5C1F6_690x1000-1-193x278-1-2476-175x238.jpg', 'link': 'https://clover-manga.com/manga/99-tahta-cubuk/'}]
        returnies = []

        for manga in data:
            html = requests.get(manga["link"]).content.decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            insert = []
            chapters = soup.find("div",{"class":"listing-chapters_wrap"}).find_all("a")
            for chapter in chapters:
                link = chapter.get("href")
                number = chapter.text.strip().split(" ")[-1]
                v = datetime.datetime.now()
                insert.append({"number":number,"url":link,"manga":manga["link"].split("/")[-2],"fansub":"CloverManga","createdAt":v})
            returnies.append(insert)
        return returnies