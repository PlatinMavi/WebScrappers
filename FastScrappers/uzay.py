import requests
from bs4 import BeautifulSoup
import datetime
import os

class Uzay():
    def __init__(self) -> None:
        pass

    def GetAllManga(self):
        url = "https://uzaymanga.com/manga/list-mode/"
        html = requests.get(url).content.decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")

        returnies = []
        mangaList = soup.find("div",{"class":"soralist"}).find_all("a",{"class":"series"})
        for manga in mangaList:
            returnies.append({"name":manga.text.strip(),"link":manga.get("href")})

        return returnies
    
    def GetAllMangaData(self):
        data = self.GetAllManga()
        # data = [{"name":"Acımasız Eğitmen","link":"https://uzaymanga.com/manga/acimasiz-egitmen/"}]
        returnies = []

        for manga in data:
            html = requests.get(manga["link"]).content.decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            desc = soup.find("div",{"itemprop":"description"}).text
            browser = manga["link"].split("/")[-2]
            category = []
            genres = soup.find("span",{"class":"mgen"}).find_all("a")
            for genre in genres:
                category.append(genre.text)

            returnies.append({"name":manga["name"],"image":browser,"desc":desc,"category":category,"browser":browser})

        return returnies
    
    def GetAllChapter(self):
        data = self.GetAllManga()
        # data = [{"name":"Acımasız Eğitmen","link":"https://uzaymanga.com/manga/acimasiz-egitmen/"}]
        returnies = []

        for manga in data:
            html = requests.get(manga["link"]).content.decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            insert = []

            chapters = soup.find_all("div",{"class":"eph-num"})
            for chapter in chapters:
                anchor = chapter.find("a")
                link = anchor.get("href")
                num = anchor.find("span",{"class":"chapternum"}).text.strip().split(" ")[-1]
                current_time = datetime.datetime.now()
                insert.append({"number":num,"url":link,"manga":manga["link"].split("/")[-2],"fansub":"UzayManga","createdAt":current_time})
            returnies.append(insert[1:])
        return returnies