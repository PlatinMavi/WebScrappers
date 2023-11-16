from bs4 import BeautifulSoup
import requests
import datetime
import re

class Armoni():
    def __init__(self) -> None:
        self.index = 0
        

    def GetAllManga(self):
        url = "https://armoniscans.com/manga/list-mode/"
        html = requests.get(url).content.decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html,"html.parser")
        mangasraw = []
        for link in soup.find_all("a",{"class":"series"}):
            Link = link.get("href")
            Title = link.contents[0]
            if Title == "\n":
                pass
            else:
                if "[Bırakıldı]" or "[Tamamlandı]"in Title:
                    Trimmed = Title.split("[")[0].strip()
                    mangasraw.append({"Title":Trimmed,"Link":Link})
                else:
                    mangasraw.append({"Title":Title,"Link":Link})
        FixedMangas = list({str(item): item for item in mangasraw}.values())
        return FixedMangas 
    
    def GetAllMangaData(self):
        content = self.GetAllManga()
        total = len(content)
        hata = []
        returnies = []
        
        for manga in content:
            try:
                url = manga["Link"]
                html = requests.get(url).content.decode("utf-8", errors="ignore")
                soup = BeautifulSoup(html,"html.parser")

                title = manga["Title"]
                image = str(soup.find("img",{"class":"wp-post-image"})["src"])
                browser = url.split("/")[-2]
                desc = ""
                categorys = []

                description = soup.find("div",{"itemprop":"description"})
                try:
                    for x in description.find_all("p"):
                        if "<" in str(x.contents[0]):
                            pass
                        else:
                            desc = desc + str(x.contents[0])
                except:
                    print("error", url)

                span = soup.find("span",{"class":"mgen"})
                try:
                    for y in span.find_all("a"):
                        category = ""
                        if " " in y.contents[0]:
                            category = y.contents[0].replace(" ","") 
                        else:
                            category = y.contents[0]
                        categorys.append(category)
                except:
                    print("error", url)

                ins = {"name":title,"image":browser,"desc":desc,"category":categorys,"browser":browser}

                returnies.append(ins)

                self.index = self.index+1
                print(self.index,"/",total,title)
            except:
                hata.append(manga)

        return returnies
    
    def GetAllChapter(self):
        content = self.GetAllManga()
        total = len(content)
        index = 0
        returnies = []
        for manga in content:
            url = manga["Link"]
            html = requests.get(url).content
            soup = BeautifulSoup(html,"html.parser")
            index = index + 1

            g = []
            
            for bolumler in soup.find_all("div",{"class":"eph-num"}):  
                atagi = bolumler.find("a")
                link = atagi.get("href")
                num = atagi.find("span",{"class":"chapternum"}).contents[0].split(" ")[1]
                
                # Extract numeric part from the string
                numeric_part = re.search(r'\d+', num)
                if numeric_part:
                    extracted_num = int(numeric_part.group())
                else:
                    extracted_num = 0  # Default value if no numeric part found

                current_time = datetime.datetime.now()
                ins = {"number":extracted_num,"url":link,"manga":url.split("/")[-2],"fansub":"ArmoniScans","createdAt":current_time}
                g.append(ins)
            returnies.append(g)
            print("(",index,"/",total,")")

        return returnies