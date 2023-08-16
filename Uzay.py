import requests
from bs4 import BeautifulSoup
import datetime
import os

class UzayScrapper():
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
    
    def GetAllChapters(self):
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
                insert.append({"number":num,"url":link,"manga":manga["link"],"fansub":"UzayManga","createdAt":current_time})
            returnies.append(insert[1:])
        return returnies
    

    def GetMangaImage(self):
        def download_image(image_link,name):
            # os.makedirs("AsuraScans", exist_ok=True)
            try:
                response = requests.get(image_link)
                if response.status_code == 200:
                    # Extract the filename from the URL
                    filename = os.path.join("Temp", name+"Uzay"+".png")

                    # Save the image file
                    with open(filename, "wb") as file:
                        file.write(response.content)

                    print("Image downloaded successfully.")
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error downloading image: {str(e)}")

        content = self.GetAllManga()
        # content = [{"name":"Acımasız Eğitmen","link":"https://uzaymanga.com/manga/acimasiz-egitmen/"}]
        total = len(content)
        index = 0
        for manga in content:
            url = manga["link"]
            html = requests.get(url).content.decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html,"html.parser")

            browser = url.split("/")[-2]
            image = str(soup.find("img",{"class":"wp-post-image"})["src"])
            download_image(image,browser)
            index = index+1
            print("(",index,"/",total,")",manga["name"])


# logger = UzayScrapper().GetMangaImage()
# with open("log.txt", "w", errors="replace") as log_file:
#     print(logger, file=log_file)