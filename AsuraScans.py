from bs4 import BeautifulSoup
import requests
import pymongo
import datetime
import re
import os

class AsuraScrapper():
    def __init__(self) -> None:
        self.index = 0
        

    def GetAllManga(self):
        url = "https://asurascanstr.com/manga/list-mode/"
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
    
    def GetAllMangaDetails(self):
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

                ins = {"name":title,"image":image,"desc":desc,"category":categorys,"browser":browser}

                returnies.append(ins)

                self.index = self.index+1
                print(self.index,"/",total)
            except:
                hata.append(manga)

        return returnies
    
    def InsertChapters(self):
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
                ins = {"number":extracted_num,"url":link,"manga":url,"fansub":"AsuraScans","createdAt":current_time}
                g.append(ins)
            returnies.append(g)
            print("(",index,"/",total,")")

        return returnies
    
    def scrapeImage(self):
    
        def download_image(image_link,name):
            os.makedirs("AsuraScans", exist_ok=True)

            try:
                response = requests.get(image_link)
                if response.status_code == 200:
                    # Extract the filename from the URL
                    filename = os.path.join("AsuraScans", name+"AsuraScans"+".png")

                    # Save the image file
                    with open(filename, "wb") as file:
                        file.write(response.content)

                    print("Image downloaded successfully.")
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error downloading image: {str(e)}")

        content = self.GetAllManga()
        total = len(content)
        index = 0
        for manga in content:
            url = manga["Link"]
            html = requests.get(url).content.decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html,"html.parser")

            browser = url.split("/")[-2]
            image = str(soup.find("img",{"class":"wp-post-image"})["src"])
            download_image(image,browser)
            index = index+1
            print("(",index,"/",total,")",manga["Title"])