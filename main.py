URI = "mongodb+srv://MangaBridge:MangaBridge@mangabridgetest.opuehm4.mongodb.net/?retryWrites=true&w=majority"

if __name__ == "__main__":
    from AsuraScans import AsuraScrapper
    from WebtoonTr import WebtoonScrapper
    from Hayalistic import HayalisticScrapper
    from Ruya import RuyaScrapper
    from Clover import CloverScrapper
    from Mangazure import MangazureScrapper
    from Uzay import UzayScrapper
    import pymongo


    client = pymongo.MongoClient(URI)
    db = client["MangaBridge"]
    mangas = db["Manga"]
    chapter = db["Chapter"]

    Scrappers = [
        AsuraScrapper(),
        WebtoonScrapper(),
        HayalisticScrapper(),
        RuyaScrapper(),
        CloverScrapper(),
        MangazureScrapper(),
        UzayScrapper()
    ]

    def ScrapeManga():
        existing_manga_documents = mangas.find()
        unique_fields = ["name", "browser"]

        unique_field_values = set()
        for document in existing_manga_documents:
            for field in unique_fields:
                unique_field_values.add(document.get(field))

        for scrapper in Scrappers:
            data = scrapper.GetAllMangasData()

            new_manga_documents = []

            for manga_data in data:
                if manga_data["name"] not in unique_field_values and manga_data["browser"] not in unique_field_values:
                    new_manga_documents.append(manga_data)

            mangas.insert_many(new_manga_documents)
            print(f"{len(new_manga_documents)} new manga documents inserted from {scrapper.__class__.__name__}")

    def ScrapeChapter():
        # Existing chapter documents and unique fields for chapters
        existing_chapter_documents = chapter.find()
        unique_fields = ["fansub", "number", "manga"]

        unique_field_values = set()
        for document in existing_chapter_documents:
            fansub_number_tuple = tuple(document.get(field) for field in unique_fields)
            unique_field_values.add(fansub_number_tuple)

        for scrapper in Scrappers:  # Modify this to use the appropriate scrapper for chapters
            chapter_data_list = scrapper.GetAllChapters()

            new_chapter_documents = []

            for chapter_data_unwrapped in chapter_data_list:
                try:
                    target = chapter_data_unwrapped[-1]["manga"]
                    obId = mangas.find_one({"browser":target})["_id"]

                    for chapter_data in chapter_data_unwrapped:
                        chapter_data["manga"] = obId
                        fansub_number_tuple = (chapter_data["fansub"], chapter_data["number"], chapter_data["manga"])
                        if fansub_number_tuple not in unique_field_values:
                            new_chapter_documents.append(chapter_data)
                            unique_field_values.add(fansub_number_tuple)  # Update the set
                except:
                    print("Manga Finding Error")

            chapter.insert_many(new_chapter_documents)
            print(f"{len(new_chapter_documents)} new chapter documents inserted from {scrapper.__class__.__name__}")

    ScrapeChapter()