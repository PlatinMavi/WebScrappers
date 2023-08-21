import requests
import datetime
import os
from bs4 import BeautifulSoup

class GuncelScrapper():
    def __init__(self) -> None:
        pass

    def GetLastPage(self):
        url = "https://guncelmanga.net/manga-oku/?m_orderby=alphabet"
        html = requests.get(url).content.decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")

        lastpage = soup.find("")