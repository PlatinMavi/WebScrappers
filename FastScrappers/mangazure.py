from bs4 import BeautifulSoup
import backbone
import datetime

class Mangazure:
    def __init__(self) -> None:
        pass

    def GetLastPage(self):
        html = backbone.Scrape([{"url":"https://www.mangazure.com/search/label/T%C3%BCm%C3%BC" ,"element":"content-out"}])[0]
        soup = BeautifulSoup(html, "html.parser")
        lastpage = int(soup.find("div", {"class":"p-nav-right"}).text.strip().split(" ")[1])
        return lastpage
    
    def GetAllManga(self):
        lastpage = self.GetLastPage()
        # lastpage = 1
        urls = []
        returnies = []
        for pgnum in range(1,lastpage+1):
            urls.append({"url":f"https://www.mangazure.com/search/label/T%C3%BCm%C3%BC?p={pgnum}","element":"content-out"})

        htmls = backbone.Scrape(urls,wait=1,threadCount=1)

        for html in htmls:
            try:
                soup = BeautifulSoup(html,"html.parser").find("div",{"class":"content-out"})
                mangas = soup.find_all("div",{"class":"item-box"})
                for manga in mangas:
                    title = manga.text
                    link = "https://www.mangazure.com"+manga.find("a").get("href")
                    returnies.append({"name":title ,"link":link})
            except:
                print("Hata")
        return returnies
    
    def GetAllMangaData(self):
        data = self.GetAllManga()
        # data = [{'name': 'The Terminally Ill Young Master of the Baek Clan', 'link': 'https://www.mangazure.com/the-terminally-ill-young-master-of-the-baek-clan'}]
        urls = []
        returnies = []
        for url in data:
            urls.append({"url":url["link"],"element":"manga-detail"})
        
        htmls = backbone.Scrape(urls,wait=1,threadCount=1)

        for x,html in enumerate(htmls):
            try:    
                soup = BeautifulSoup(html, "html.parser").find("div",{"class":"manga-detail"})

                browser = data[x]["link"].split("/")[-1]
                desc = soup.find("div",{"class":"mdr-desc"}).text
                category= []
                genres = soup.find("span",{"class":"mdl-tur"}).find_all("a")
                for genre in genres:
                    category.append(genre.text)

                returnies.append({"name":data[x]["name"],"image":browser,"desc":desc,"category":category,"browser":browser})
            except:
                print("hata")
        return returnies
    
    def GetAllChapter(self):
        data = self.GetAllManga()
        # data = [{'name': 'The Terminally Ill Young Master of the Baek Clan', 'link': 'https://www.mangazure.com/the-terminally-ill-young-master-of-the-baek-clan'}]
        urls = []
        returnies = []
        for url in data:
            urls.append({"url":url["link"],"element":"mdr-list"})
        
        htmls = backbone.Scrape(urls,wait=1.2,threadCount=1)

        for x,html in enumerate(htmls):
            try:
                soup = BeautifulSoup(html, "html.parser").find("ul",{"class":"mdr-list"})
                insert = []
                print(soup)
                chapters = soup.find_all("li")
                for chapter in chapters:
                    anchor = chapter.find("a")
                    link = anchor.get("href")
                    num = anchor.text.strip().split(" ")[-1]
                    current_time = datetime.datetime.now()
                    insert.append({"number":int(num),"url":link,"manga":data[x]["link"].split("/")[-1],"fansub":"Mangazure","createdAt":current_time})
                returnies.append(insert)
            except:
                print("hata")

        return returnies