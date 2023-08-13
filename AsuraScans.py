from bs4 import BeautifulSoup
import requests
import pymongo
import os
from Parser import Parser

class AsuraScrapper():
    def __init__(self) -> None:
        self.client = pymongo.MongoClient("mongodb+srv://alpergezer13:alpergezer13@mangabridgetest.a4ggcj9.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["AsuraScans"]
        self.collection = self.db["mangas"]
        self.chapter = self.db["chapters"]
        self.index = 0
        

    def GetAllManga(self):
        url = "https://asurascanstr.com/manga/list-mode/"   
        return Parser.ParseMangaData("asura",url)
    
    def InsertManga(self):
        content = self.GetAllManga()
        total = len(content)
        hata = []
        for manga in content:
            try:
                ins = Parser.GetMangaDataDetail("asura",manga)
                f = self.collection.insert_one(ins)

                self.index = self.index+1
                print(self.index,"/",total,manga["title"])
            except:
                hata.append(manga)

        return print("ok",hata)
    
    def InsertChapters(self):
        content = self.GetAllManga()
        total = len(content)
        index = 0
        for manga in content: 
            g = Parser.GetChapterData("asura",manga)                
            index = index+1
            f = self.chapter.insert_many(g)
            print("(",index,"/",total,")",manga["title"])

    def DownloadMangaImage(self):       
        content = self.GetAllManga()
        total = len(content)
        index = 0
        for manga in content:
            url = manga["Link"]
            html = requests.get(url).content.decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html,"html.parser")

            name = url.split("/")[-2]
            image = str(soup.find("img",{"class":"wp-post-image"})["src"])
            
            os.makedirs("CollectivePool", exist_ok=True)

            try:
                response = requests.get(image)
                if response.status_code == 200:
                    # Extract the filename from the URL
                    filename = os.path.join("CollectivePool", name+".png")

                    # Save the image file
                    with open(filename, "wb") as file:
                        file.write(response.content)

                    print("Image downloaded successfully.")
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error downloading image: {str(e)}")

            index = index+1
            print("(",index,"/",total,")",manga["Title"])
        

  
sc = AsuraScrapper()

print(sc.InsertManga())
print(sc.InsertChapters())