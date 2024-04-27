# Author: Zhu Wenye
# time:2024-4-18
# version:1.0
#

import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_collection(url, headers, img_src):
    name_pad_all = ['Inventory number', 'Collection','Artist/maker / School / Artistic centre',
                  'Object name/Title', 'Type of object', 'Description/Features', 'Inscriptions',
                  'Dimensions', 'Materials and techniques',
                  'Date','Place of origin',
                  'Collector / Previous owner / Commissioner / Archaeologist / Dedicatee','Acquisition details','Acquisition date','Owned by','Held by',
                  'Current location',
                  "Mode d'acquisition",'Period','Places','Type']
    collection = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    pad = soup.find_all('div', class_="notice__fullcartel__entries")

    # 文本信息
    for item in name_pad_all:
        bool_ = 0
        for i in range(len(pad)):
            part_firsts  = pad[i].find_all('div', class_="m-3col part__label")
            part_lasts = pad[i].find_all('div', class_="m-7col m-last part__content")
            for j in range(len(part_firsts)):
                part_first = part_firsts[j].text.strip()
                if part_first == item :
                    part_last = part_lasts[j].text.strip().replace("                         ", " ")
                    collection.append(part_last)
                    bool_=1
                    break
            if bool_==1 :
                break

        if bool_ == 0 :
            collection.append("")


    # 图片及链接
    collection.append({"relic_url": url})
    collection.append({"img_url": f"https://collections.louvre.fr/{img_src}"})
    return collection


def getcollection(url, headers):
    collections = []
    for i in range(1, 173):
        url_search = url + str(1) + "&q=Chine%2B"
        response = requests.get(url_search, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(i)
        set_url = soup.find_all('div', class_="card__img square mb-05")
        num_collection_onepage = len(set_url)
        for j in range(num_collection_onepage):
            img_src = set_url[j].find('a').find('img')['src']
            true_url_collection = "https://collections.louvre.fr/" + set_url[j].find('a')['href'] 

            collection = get_collection(true_url_collection, headers, img_src)
            collections.append(collection)
    return collections


def collection_to_csv(collections): #保存为csv文件
    df = pd.DataFrame(collections)
    df.columns = ['Inventory number', 'Collection','Artist/maker / School / Artistic centre',
                  'Object name/Title', 'Type of object', 'Description/Features', 'Inscriptions',
                  'Dimensions', 'Materials and techniques',
                  'Date','Place of origin',
                  'Collector / Previous owner / Commissioner / Archaeologist / Dedicatee','Acquisition details','Acquisition date','Owned by','Held by',
                  'Current location',
                  "Mode d'acquisition",'Period','Places','Type',
                  'relic_url', 'img_url']

    df.to_csv("louvre.csv", index_label='id', encoding="utf_8_sig")


url = "https://collections.louvre.fr/en/recherche?page="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
}

collections = getcollection(url, headers)
collection_to_csv(collections)
print("结束")