URI = "mongodb+srv://MangaBridge:MangaBridge@mangabridgetest.opuehm4.mongodb.net/?retryWrites=true&w=majority"

if __name__ == "__main__":
    from AsuraScans import AsuraScrapper
    from WebtoonTr import WebtoonScrapper
    from Hayalistic import HayalisticScrapper
    # from Ruya import RuyaScrapper
    from Clover import CloverScrapper
    from Mangazure import MangazureScrapper
    from Uzay import UzayScrapper
    import pymongo
    from more_itertools import chunked


    client = pymongo.MongoClient(URI)
    db = client["MangaBridge"]
    mangas = db["Manga"]
    chapter = db["Chapter"]

    Scrappers = [
        AsuraScrapper(),
        WebtoonScrapper(),
        HayalisticScrapper(), # KINDA BROKEN (nots)
        # RuyaScrapper(), BROKEN
        CloverScrapper(),
        MangazureScrapper(),
        UzayScrapper()
    ]

    def ScrapeManga():
        for scrapper in Scrappers:
            try:
                existing_manga_documents = mangas.find()
                unique_fields = ["name", "browser"]

                unique_field_values = set()
                for document in existing_manga_documents:
                    for field in unique_fields:
                        unique_field_values.add(document.get(field))
            
                data = scrapper.GetAllMangasData()
                chunkIndex = 0
                
                new_manga_documents = []

                for manga_data in data:
                    if manga_data["name"] not in unique_field_values and manga_data["browser"] not in unique_field_values:
                        new_manga_documents.append(manga_data)

                chunkedList = list(chunked(new_manga_documents, 50))
                nTh = len(chunkedList)

                erroredInserts = []

                for chunk in chunkedList:
                    try:
                        chunkIndex += 1
                        mangas.insert_many(chunk)
                        print(f"{len(new_manga_documents)} new manga documents inserted from {scrapper.__class__.__name__} ({chunkIndex}/{nTh})")
                    except:
                        print("InsertErr: Probably no new Mangas...")
                        erroredInserts.append(chunk)

                if len(erroredInserts) != 0:
                    for reChunk in erroredInserts:
                        try:
                            chunkIndex += 1
                            mangas.insert_many(reChunk)
                            print(f"{len(erroredInserts)} new manga documents(errored) inserted from {scrapper.__class__.__name__} ({chunkIndex}/{nTh})")
                        except:
                            print("Some error in inssert...")


            except:
                print("SCRAPPER BROKE DOWN !!!")

    def ScrapeChapter():
        # Existing chapter documents and unique fields for chapters
        for scrapper in Scrappers:
            existing_chapter_documents = chapter.find()
            unique_fields = ["fansub", "number", "manga"]

            unique_field_values = set()
            for document in existing_chapter_documents:
                fansub_number_tuple = tuple(document.get(field) for field in unique_fields)
                unique_field_values.add(fansub_number_tuple)

          # Modify this to use the appropriate scrapper for chapters
            chapter_data_list = scrapper.GetAllChapters()
            chunkIndex = 0

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
            
            chunkedList = list(chunked(new_chapter_documents, 50))
            nTh = len(chunkedList)
            for chunk in chunkedList:
                try:
                    chapter.insert_many(chunk)
                    print(f"{len(new_chapter_documents)} new chapter documents inserted from {scrapper.__class__.__name__} ({chunkIndex}/{nTh})")
                except:
                    print("InsertErr: Probably no new Chapters...")

    submittedExecution = input("\033[92m1 For MangaScraping 2 For ChapterScraping : ")

    match submittedExecution:
        case "1":
            ScrapeManga()
        case "2":
            ScrapeChapter()
