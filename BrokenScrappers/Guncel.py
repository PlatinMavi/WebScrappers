import requests
import datetime
import os
from bs4 import BeautifulSoup

class GuncelScrapper():
    def __init__(self) -> None:
        pass

    def GetLastPage(self):
        headers ={
            "accept": "*/*",
            "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        }
        url = "https://guncelmanga.net/wp-admin/admin-ajax.php"
        html = requests.post(url,headers=headers)
        return html
    
print(GuncelScrapper().GetLastPage())

# fetch("https://guncelmanga.net/wp-admin/admin-ajax.php", {
#   "headers": {
#     "accept": "*/*",
#     "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
#     "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
#     "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "x-requested-with": "XMLHttpRequest"
#   },
#   "referrer": "https://guncelmanga.net/manga-oku/?m_orderby=alphabet",
#   "referrerPolicy": "strict-origin-when-cross-origin",
#   "body": "action=madara_load_more&page=5&template=madara-core%2Fcontent%2Fcontent-archive&vars%5Bpaged%5D=1&vars%5Borderby%5D=post_title&vars%5Btemplate%5D=archive&vars%5Bsidebar%5D=right&vars%5Bpost_type%5D=wp-manga&vars%5Bpost_status%5D=publish&vars%5Border%5D=ASC&vars%5Bmeta_query%5D%5Brelation%5D=AND&vars%5Bmanga_archives_item_layout%5D=big_thumbnail",
#   "method": "POST",
#   "mode": "cors",
#   "credentials": "omit"
# });