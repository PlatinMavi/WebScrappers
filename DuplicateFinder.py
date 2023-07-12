import pymongo
import base64
import os

class Detector():
    def __init__(self) -> None:
        self.client = pymongo.MongoClient("mongodb+srv://PlatinMavi:23TprQmteTiPJA6r@mangabridge.qceexb2.mongodb.net/?retryWrites=true&w=majority")
        self.WebtoonTr = self.client["WebtoonTr"]
        self.W_manga = self.WebtoonTr["mangas"]
        self.W_chapter = self.WebtoonTr["chapters"]
        self.Asura = self.client["AsuraScans"]
        self.A_manga = self.Asura["mangas"]
        self.A_chapter = self.Asura["chapters"]
        self.Combined = self.client["combined"]
        self.CM =self.Combined["mangas"]
        self.CC = self.Combined["chapters"]
        self.Hayalistic = self.client["Hayalistic"]
        self.H_manga = self.Hayalistic["mangas"]
        self.H_chapter = self.Hayalistic["chapters"]

        # self.result = self.client["results"]
        # self.duplicates = 

    def GetAll(self):
        allmanga = [self.W_manga.find({}),self.A_manga.find({}),self.H_manga.find({})]
        mangas =[]
        
        for x in allmanga:
            for y in x:
                mangas.append(y)
        return mangas
    
    def Compare(self):
        data = self.GetAll()
        duplicates = []
        total = len(data)
        index = 0
        for x in data:
            xbrowser = x["browser"]
            xname = x["name"]
            for y in data:
                ybrowser = y["browser"]
                yname = y["name"]

                if y["_id"] == x["_id"]:
                    pass
                else:
                    if xbrowser == ybrowser or yname == xname:
                        ap = [x,y]
                        poss = [y,x]
                        if duplicates.count(ap) == 0 and duplicates.count(poss) == 0:
                            duplicates.append(ap)
                            print("found duplicate")
            index = index+1
            print(f"( {index} / {total} )")
        return duplicates, data
    
    def UpdateAll(self):
        s = self.A_manga.update_many({},{"$set":{"fansub":"AsuraScans"}})
        return s
    
    def FindAndUpload(self):
        dup, data = self.Compare()
        for x in dup:
            original = x[0]
            duplicate = x[1]

            f = self.CC.update_many({"manga": duplicate["_id"]}, {"$set": {"manga": original["_id"]}})


            for dictionary in data:
                if "_id" in dictionary and dictionary["_id"] == duplicate["_id"]:
                    data.pop(data.index(dictionary))
                    break

        ff = self.CM.insert_many(data)
        return data
        
    def CombineChapers(self,x):
        self.CC.insert_many(x)

    def ImageUpdate(self):
        image_directory = "C:/Users/PC/Desktop/Scrapper/Collection"
        index = 0
        total = len(os.listdir(image_directory))

        for filename in os.listdir(image_directory):
            try:
                image_path = os.path.join(image_directory, filename)
                if os.path.isfile(image_path):
                    
                    browser = filename.split(".")[0]
                    index = index+1
                    # document = {"image_name": filename, "image": base64_image}
                    g =self.CM.update_one({"browser":browser},{"$set":{"image":f"{browser}.png"}})
                    print(f"( {index} / {total} )" ,browser)
            except:
                print("duplicate probably deletetd")
        return print("done")

    
dt = Detector()
y = dt.ImageUpdate()


