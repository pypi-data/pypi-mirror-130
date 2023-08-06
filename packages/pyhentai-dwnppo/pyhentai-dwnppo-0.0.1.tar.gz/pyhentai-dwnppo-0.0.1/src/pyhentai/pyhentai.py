import random
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import shutil
import time
import re

def lookup(code):
    url = "https://nhentai.net/g/" + str(code)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    title = soup.select('h1')[0].text
    print("URL: " + url)
    print("Title: " + title)
    print("Tags: ")
    taglist = []
    tags = soup.select('div.tag-container.field-name')[2]
    for item in tags('span', class_='tags'):
        for finaltag in item.find_all('span', class_='name'):
            print(finaltag.get_text())
    
def download(code):
    numcode = 1
    while True:
        check = "https://nhentai.net/g/" + str(code)
        if check == 404:
            print("Check your code, 404 found.")
        file_name = str(numcode) + ".jpg"
        link = "https://i.nhentai.net/galleries/" + str(code) + "/" + str(numcode) + ".jpg"
        res = requests.get(link, stream=True)
        if res.status_code == 404:
            continue
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f) 
                numcode += 1
                print(file_name + " " + "downloaded")
                
        else:
            break
    
    print('Sauce downloaded: ',code)
    
def random(count):
    url = "https://nhentai.net/random/"
    print("CAUTION: The generation of the codes can be slow if your internet connection is slow.")

    tries = 0
    start = time.time()
    codes = set()

    while len(codes) != count:
        tries += 1
        r = requests.get(url).url
        code = re.findall(r"(\d+)", r)
        if len(code):
            codes.add(code[0])

    codes = list(codes)

    print(codes)


    end = time.time()
    print(str(end - start) + " second/s elapsed.")
    print("Found {} codes with {} tries.".format(len(codes), tries))