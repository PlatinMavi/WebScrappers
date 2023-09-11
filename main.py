if __name__ == "__main__":

    from AsuraScans import AsuraScrapper
    from WebtoonTr import WebtoonScrapper
    from Hayalistic import HayalisticScrapper
    from Ruya import RuyaScrapper
    from Clover import CloverScrapper
    from Mangazure import MangazureScrapper
    from Uzay import UzayScrapper

    import pymongo

    Scrappers = [
        AsuraScrapper(),
        WebtoonScrapper(),
        HayalisticScrapper(),
        RuyaScrapper(),
        CloverScrapper(),
        MangazureScrapper(),
        UzayScrapper()
        ]

    for scrapper in Scrappers:
        context = scrapper.GetAllMangas()
        print(context)