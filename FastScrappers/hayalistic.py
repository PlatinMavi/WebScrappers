import requests
from bs4 import BeautifulSoup
import datetime
import os
import backbone

class Hayalistic():
    def __init__(self) -> None:
        pass

    def GetLastPage(self):
        url = "https://hayalistic.com.tr/webtoonlar/?m_orderby=alphabet"
        html = requests.get(url).content.decode("utf-8",errors="ignore")
        soup = BeautifulSoup(html,"html.parser")
        lastPage = soup.find("a",{"class":"last"}).get("href").split("/")[-2]
        return lastPage
    
    def GetAllManga(self):
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
    
    def GetAllMangaData(self):
        data = self.GetAllManga()
        # data = [{"link":"https://hayalistic.com.tr/manga/zindan-sifirlanmasi/","title":"Zindan Sıfırlanması"}]
        index = 0
        total = len(data)
        returnies = []

        for links in data:
            try:
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
            except:
                print("hata")
        return returnies
    
    def GetAllChapter(self):
        data = self.GetAllManga()
        # data = [{"link":"https://hayalistic.com.tr/manga/a-bittersweet-couple/","browser":"a-bittersweet-couple","title":"b"}]
        total = len(data)
        index = 0
        hata = []
        returnies = []
        urls = []

        for d in data:
            urls.append({"url":d["link"],"element":"wp-manga-chapter"})

        htmls = backbone.Scrape(urls)

        for x,html in enumerate(htmls):
            try:
                ins = []
                url = data[x]["link"]
                elements = BeautifulSoup(html, "html.parser").find_all("li",{"class":"wp-manga-chapter"})

                for soup in elements:
                    
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
                print("(",index,"/",total,")",data[x]["title"])
                returnies.append(ins)
            except:
                hata.append(data[x]["title"])
            return returnies