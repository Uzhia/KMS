# Author: Li Zhikun
# Date: 2024-04-15
# Version: 1.0
# Description: This script is used to crawl the collections of Henan Museum from the official website.
#              It will output the collections' name, type, time, collection URL and image URL to a CSV file.
#              This version is single-threaded and does not support multi-threading.
#              On the further version, I will add multi-threading support to speed up the crawling process.

import requests
import pandas as pd

from tqdm import tqdm
from retrying import retry
from bs4 import BeautifulSoup


def get_page(base_url, headers):
	index_response = requests.get(base_url, headers=headers)
	index_soup = BeautifulSoup(index_response.content, 'html.parser')
	pagination = index_soup.find('div', class_='pagination')
	last_page = pagination.find_all('a')[-1]['data-url'].split('=')[1]
	return int(last_page)


@retry(wait_random_min=500, wait_random_max=2000, stop_max_attempt_number=3)
def get_collections_on_page(base_url, headers, page_index: int):
	collections = []

	page_url = f'{base_url}?pageIndex={page_index}'
	page_response = requests.get(page_url, headers=headers)
	page_soup = BeautifulSoup(page_response.content, 'html.parser')

	masonry_container = page_soup.find('div', id='masonry-container')
	for item in masonry_container.find_all('div', class_='list-item'):
		collection_url = item.find('a')['href'].replace('//', 'https://')
		boutique_cover = item.find('div', class_='boutique-cover')
		img_url = ''
		if boutique_cover is not None:
			img_url = boutique_cover['data-bg'].replace('//', 'https://')
		collections.append({
			'collectionUrl': collection_url,
			'imgUrl': img_url
		})

	return collections


def get_all_collections(base_url, headers, start_page):
	last_page = get_page(base_url, headers)
	collections = []
	for i in tqdm(range(start_page, last_page + 1)):
		collections.extend(get_collections_on_page(base_url, headers, i))
	return collections


@retry(wait_random_min=500, wait_random_max=2000, stop_max_attempt_number=3)
def get_each_collection_info(collection_info, headers):
	collection_response = requests.get(collection_info['collectionUrl'], headers=headers)
	collection_soup = BeautifulSoup(collection_response.content, 'html.parser')
	collection_attributes = collection_soup.find('div', class_='treasure-content-attribute-list') \
		.find_all('div', class_='treasure-content-attribute-item')

	collection_name = collection_soup.find('div', class_='treasure-content-attribute-title').text
	collection_type = collection_attributes[0].text.split(': ')[1]
	collection_time = collection_attributes[1].text.split(': ')[1]

	collection_info['name'] = collection_name
	collection_info['type'] = collection_type
	collection_info['time'] = collection_time


def get_collections_info(collections, headers):
	for collection in tqdm(collections):
		get_each_collection_info(collection, headers)


def output_to_csv(collections):
	df = pd.DataFrame(collections)
	df.to_csv('henan-collections.csv',
	          index_label='id',
	          columns=['name', 'type', 'time', 'collectionUrl', 'imgUrl'],
	          header=['Name', 'Type', 'Time', 'Collection URL', 'Image URL'],
	          encoding='utf-8-sig')


def main():
	request_url = 'https://www.chnmus.net/ch/collection/boutique/index.html'
	request_headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
		# 'Cookie': 'JSESSIONID=4599E9B9C5856C49B79D3C7140558118; Hm_lvt_5d867eb71eb3bfefe2fd61a2d93397be=1713103416; Hm_lpvt_5d867eb71eb3bfefe2fd61a2d93397be=1713103416; mozi-assist={%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false}; PUBLICCMS_ANALYTICS_ID=a46780e4-fc84-4045-9225-fd6f6e3c72f5'
	}

	print('\nGetting all collections...')
	collections = get_all_collections(request_url, request_headers, 1)
	print(f'\nFound {len(collections)} collections')
	print('\nGetting collections info...')
	get_collections_info(collections, request_headers)
	print('\nOutputting to CSV...')
	output_to_csv(collections)
	print('\nDone!')


if __name__ == '__main__':
	main()
