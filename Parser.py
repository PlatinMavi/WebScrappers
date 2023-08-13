from bs4 import BeautifulSoup
import requests
import datetime
import re
import pymongo

class Parser:
    def __init__(self) -> None:
        pass

    def ParseMangaData(sub, url):
        match sub:
            case "asura":
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
                return list({str(item): item for item in mangasraw}.values())
            
    def GetMangaDataDetail(sub,manga):
        match sub:
            case "asura":
                
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

                return {"name":title,"image":image,"desc":desc,"category":categorys,"browser":browser}
            
    def GetChapterData(sub,manga):
        match sub:
            case "asura":
                client = pymongo.MongoClient("mongodb+srv://alpergezer13:alpergezer13@mangabridgetest.a4ggcj9.mongodb.net/?retryWrites=true&w=majority")
                db = client["AsuraScans"]
                collection = db["mangas"]

                url = manga["Link"]
                query = manga["Title"]
                html = requests.get(url).content
                soup = BeautifulSoup(html,"html.parser")
                find = collection.find_one({"name":query})

                g = []
                
                for bolumler in soup.find_all("div",{"class":"eph-num"}):  
                    atagi = bolumler.find("a")
                    link = atagi.get("href")
                    num = atagi.find("span",{"class":"chapternum"}).contents[0].split(" ")[1]

                    numeric_part = re.search(r'\d+', num)
                    if numeric_part:
                        extracted_num = int(numeric_part.group())
                    else:
                        extracted_num = 0  

                    current_time = datetime.datetime.now()
                    ins = {"number":extracted_num,"url":link,"manga":find["_id"],"fansub":"AsuraScans","createdAt":current_time}
                    g.append(ins)
                return g