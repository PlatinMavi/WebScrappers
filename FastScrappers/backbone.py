from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import threading
import time

def sliceList(listw, partnum):
    part_size = len(listw) // partnum
    extra = len(listw) % partnum
    lists = []

    start = 0
    for i in range(partnum):
        end = start + part_size + (1 if i < extra else 0)
        lists.append(listw[start:end])
        start = end

    return lists

def ScrapeModule(
    urls=[
        {"url":"https://example.com","element":"ExampleClassName"},
    ],wait=0):

    copt = Options()
    copt.add_argument("--headless")
    copt.add_argument('--log-level=3')

    driver = webdriver.Chrome(options=copt)
    driver.get(os.getcwd()+r"\FastScrappers\base.html")

    returnies = []
    lengthofurl = len(urls)
    index = 0

    for url in urls:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'urlInput')))
            input_text_fname = driver.find_element(By.ID, 'urlInput')
            input_text_fname.clear()
            input_text_fname.send_keys(url["url"])

            go_button = driver.find_element(By.ID, "goButton")
            go_button.click()

            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'browserFrame')))
            time.sleep(wait)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,url["element"])))

            page_source = driver.page_source
            returnies.append(page_source)

            driver.switch_to.default_content()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'urlInput')))
                input_text_fname = driver.find_element(By.ID, 'urlInput')
                input_text_fname.clear()
                input_text_fname.send_keys(url["url"])

                go_button = driver.find_element(By.ID, "goButton")
                go_button.click()

                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'body')))
                time.sleep(wait)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,url["element"])))
            except:
                pass
        
        index += 1
        print(f"{index} / {lengthofurl}")

    driver.quit()
    return returnies

def Scrape(
    urls=[
        {"url":"https://example.com","element":"ExampleClassName"},
    ],threadCount=4,wait=0):

    if len(urls) <= 3:
        scraped = ScrapeModule(urls,wait)
        return scraped

    sliced = sliceList(urls, threadCount)
    threads = []
    returnies = []

    def worker(url_chunk):
        result = ScrapeModule(url_chunk,wait)
        returnies.extend(result)

    for url_chunk in sliced:
        thread = threading.Thread(target=worker, args=(url_chunk,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return returnies