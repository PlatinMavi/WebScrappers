import spine
from bs4 import BeautifulSoup
import datetime
import math

class Ruya:
    def __init__(self) -> None:
        pass

    def GetLastPage(self):
        htmls = spine.Scrape(["https://www.ruyamanga.com/manga/?m_orderby=alphabet"],wait=1)
        try:
            soup = BeautifulSoup(str(htmls[0]),"html.parser")
            total = math.ceil(int(soup.find("div",{"class":"h4"}).text.strip().split(" ")[0])/18)
            return total
        except:
            print("parsing err")
    
    def GetAllManga(self):
        lastpage = self.GetLastPage()
        # lastpage = 1
        urls = []
        returnies = []
        for pgnum in range(1,lastpage+1):
            urls.append(f"https://www.ruyamanga.com/manga/page/{pgnum}/?m_orderby=alphabet")
        htmls = spine.Scrape(urls,wait=1,tab_switch=5)

        for html in htmls:
            try:
                soup = BeautifulSoup(str(html),"html.parser")
                mangas = soup.find_all("div",{"class":"item-thumb"})
                for manga in mangas:
                    base = manga.find("a")
                    returnies.append({"link":base.get("href"),"name":base.get("title")})
            except:
                print("parsing err")

        return returnies
    
    def GetAllMangaData(self):
        data = self.GetAllManga()
        # data = [{'link': 'https://www.ruyamanga.com/manga/above-the-heavens/', 'name': 'Above The Heavens'}]
        urls = []
        returnies = []
        for url in data:
            urls.append(url["link"])
        htmls = spine.Scrape(urls,wait=1,tab_switch=5)

        for x,html in enumerate(htmls):
            try:
                soup = BeautifulSoup(str(html),"html.parser")
                browser = data[x]["link"].split("/")[-2]
                
                category = []
                genrescontent = soup.find("div",{"class":"genres-content"}).find_all("a")
                for genre in genrescontent:
                    category.append(genre.text)

                desc = soup.find("div",{"class":"description-summary"}).find("p").text

                returnies.append({"name":data[x]["name"],"image":browser,"desc":desc,"category":category,"browser":browser})
            except:
                print("parsing err")
        
        return returnies
    
    def GetAllChapter(self):
        data = self.GetAllManga()
        # data = [{'link': 'https://www.ruyamanga.com/manga/above-the-heavens/', 'name': 'Above The Heavens'}]
        urls = []
        returnies = []
        for url in data:
            urls.append(url["link"])
        htmls = spine.Scrape(urls,wait=1,tab_switch=5)

        for x,html in enumerate(htmls):
            insert = []
            try:
                soup = BeautifulSoup(str(html),"html.parser")
                chapters = soup.find_all("li",{"wp-manga-chapter"})
                for chapter in chapters:
                    link = chapter.find("a").get("href")
                    try:
                        num = chapter.find("a").text.strip().split(" ")[1]
                    except:
                        num = link.split("/")[-2].split("-")[-1]
                    current_time = datetime.datetime.now()
                    insert.append({"number":int(num),"url":link,"manga":data[x]["link"].split("/")[-2],"fansub":"RuyaManga","createdAt":current_time})

                returnies.append(insert)
            except:
                print("parsing err")
        return returnies
    
print(Ruya().GetAllManga())