# Author: Zhu Wenye
# time:2024-4-17
# version:1.0
#
import requests
from bs4 import BeautifulSoup
import pandas as pd


def getcollection(url, headers):

    collections = [] #所有信息容器

    for i in range(11711):  #1624不存在网页，实际运行时应分开遍历0-1623和1625-11710
        print(i)
        url_new = url + str(i) + ".html"  #网址
        response = requests.get(url_new, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        #去除不相关网址
        if (soup.find('div', class_="pad") is None
                or (len(soup.find('div', class_="pad").find_all('div', class_="li") )!=4
                and len(soup.find('div', class_="pad").find_all('div', class_="li") )!=5)):
            continue

        collection = [] #单个文物信息容器

        # 文本部分
        pad = soup.find('div', class_="pad")
        collection.append(pad.find('div', class_="t").text.strip()) #名字
        collection.append(pad.find_all('div', class_="li")[0].text.split('：')[1]) #时代
        collection.append(pad.find_all('div', class_="li")[1].text.split('：')[1]) #级别

        # 展出的会多两条文本
        num = len(pad.find_all('div', class_="li"))
        if num == 4:
            collection.append("")
            collection.append(pad.find_all('div', class_="li")[2].text.split('：')[1]) #大小
            collection.append(pad.find_all('div', class_="li")[3].text.split('：')[1]) #材质
            collection.append("")


        else:
            collection.append(pad.find_all('div', class_="li")[2].text.split('：')[1]) #出土地点
            collection.append(pad.find_all('div', class_="li")[3].text.split('：')[1]) #大小
            collection.append(pad.find_all('div', class_="li")[4].text.split('：')[1]) #材质
            dis = soup.find('div', class_="p").string
            collection.append(dis)  #文本描述

        # 图片部分
        pic = soup.find('div', class_='pic')
        img_url = "htps:" + pic.find('img').get('src')
        collection.append(url_new) #文物详情页网址
        collection.append(img_url) #图片下载链接

        collections.append(collection)

    return collections


def collection_to_csv(collections):
    df = pd.DataFrame(collections)
    df.columns = ['name', 'time', 'leve', 'location(仅镇馆之宝有)', 'size', 'material', 'describe(仅镇馆之宝有)', 'relic_url', 'img_url']
    df.to_csv("shanxi.csv",index_label='id',encoding="utf_8_sig")


url = "https://www.sxhm.com/collections/detail/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
}
collections = getcollection(url, headers)
collection_to_csv(collections)
print("结束")
