import backbone
from bs4 import BeautifulSoup
import datetime

class Webtoontr:
    def __init__(self) -> None:
        pass

    def GetLastPage(self):
        html = backbone.Scrape([{"url":"https://webtoontr.net/webtoon/?m_orderby=alphabet" ,"element":"pages"}])[0]
        soup = BeautifulSoup(html,"html.parser")
        page = int(soup.find("span",{"class":"pages"}).text.split(" ")[1])
        return page
    
    def GetAllManga(self):
        lastpage = self.GetLastPage()
        # lastpage = 3
        urls = []
        Mangas = []
        for pgnum in range(1,lastpage+1):
            urls.append({"url":f"https://webtoontr.net/webtoon/page/{pgnum}/?m_orderby=alphabet","element":"item-thumb"})
        htmls = backbone.Scrape(urls)

        for html in htmls:
            soup = BeautifulSoup(html,"html.parser")
            elements = soup.find_all("div",{"class":"item-thumb"})

            for mangas in elements:
                link = mangas.find("a").get("href")
                browser = link.split("/")[-2]
                title = mangas.find("a").get("title")

                f = {"url": link, "name": title, "browser": browser}
                Mangas.append(f)
        return Mangas
    
    def GetAllMangaData(self):
        mangasw = self.GetAllManga()
        # mangasw = [{'url': 'https://webtoontr.net/webtoon/a-werewolf-boy/', 'name': 'A Werewolf Boy', 'browser': 'a-werewolf-boy'}]

        urls = []
        returnies = []
        for mangaw in mangasw:
            urls.append({"url":mangaw["url"],"element":"summary-content"})

        htmls = backbone.Scrape(urls)

        for x,html in enumerate(htmls):
            try:
                soups = BeautifulSoup(html,"html.parser")
                soup = soups.find("div",{"class":"summary_content"})
                allGenre = []
                try:
                    desc = soup.find_all("div", {"class":"manga-excerpt"})[0].find_all("p")[1].contents[0]
                except:
                    try:
                        desc = soup.find_all("div", {"class":"manga-excerpt"})[0].find_all("p")[0].contents[0]
                    except:
                        desc = ""
                        print("couldnt get description")
                name = mangasw[x]["name"]
                # image = manga["image"]
                browser = mangasw[x]["browser"]

                genreC = soup.find("div",{"class":"genres-content"})
                genre = genreC.find_all("a",{"rel":"tag"})
                for b in genre:
                    g = b.contents[0]
                    if " "in g:
                        g.replace(" ","")
                        allGenre.append(g)
                    else:
                        allGenre.append(g)

                ins = {"name":name,"image":browser,"desc":desc,"category":allGenre,"browser":browser}
                returnies.append(ins)
            except:
                print("Error!")
        return returnies
    
    def GetAllChapter(self):
        mangasw = self.GetAllManga()
        # mangasw = [{'url': 'https://webtoontr.net/webtoon/a-werewolf-boy/', 'name': 'A Werewolf Boy', 'browser': 'a-werewolf-boy'}]

        urls = []
        returnies = []
        for mangaw in mangasw:
            urls.append({"url":mangaw["url"],"element":"summary-content"})

        htmls = backbone.Scrape(urls)

        for x,html in enumerate(htmls):
            try:
                ins =[]
                soup = BeautifulSoup(html,"html.parser").find("ul",{"class":"version-chap"})
                chapters = soup.find_all("a")
                for chapter in chapters:
                    try:
                        try:
                            num = int(chapter.text.strip().split(".")[0])
                        except:
                            p = chapter.text.split("\n")[1].strip()
                            num = int(p.split(".")[0])
                    except:
                        try:
                            num = int(chapter.text.strip().split(" ")[1])
                        except:
                            num = int(chapter.text.strip().split(" ")[-1])
                            try:
                                num = ins[-1]["number"]-1
                            except:
                                num = len(chapters)

                    link = chapter.get("href")
                    createdAt = datetime.datetime.now()
                    ins.append({"number":int(num),"url":link,"manga":mangasw[x]["browser"],"fansub":"WebtoonTr","createdAt":createdAt})
                
                returnies.append(ins)
            except:
                print("Error!")
        return returnies