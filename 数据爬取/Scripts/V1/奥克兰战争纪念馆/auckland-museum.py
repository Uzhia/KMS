import json
import re

import pandas as pd
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

import config
from retrying import retry


def get_collections_on_page(base_url, headers, page_index: int):
	collections = []
	page_url = f'{base_url}&p={page_index}'
	page_response = requests.get(page_url, headers=headers)
	page_soup = BeautifulSoup(page_response.content, 'html.parser')

	item_list = page_soup.find('ul', class_='item-view__list')
	for item in item_list.find_all('li', class_='item'):
		collection_id = item.find('a')['href'].split('/')[-1].split('?')[0]
		collections.append(collection_id)

	return collections


def get_all_collections(base_url, headers):
	collections = []
	print("\nGetting all collections...")
	for i in tqdm(range(1, config.LAST_PAGE + 1)):
		collections.extend(get_collections_on_page(base_url, headers, i))
	print("\nAll collections have been fetched.")
	return collections


def get_collection_info(api_url, collection_id):
	raw_data = requests.get(f'{api_url}{collection_id}').json()
	if 'opacObjectFieldSets' not in raw_data:
		return {}
	raw_field_sets = raw_data['opacObjectFieldSets']
	images = []

	if 'imagesCollection' in raw_data and 'images' in raw_data['imagesCollection']:
		images = get_images(raw_data['imagesCollection']['images'])

	field_sets = get_field_sets(raw_field_sets, collection_id, images)
	return field_sets


def get_field_sets(field_sets, collection_id, images):
	result = {
		'collectionId': collection_id,
		'images': images,
	}
	ignore_fields = [
		'object_av_rights',
		'thumbnail_caption',
		'classification',
		'copyright',
		'object_av_link'
	]
	specaial_fields = [
		'measurement_notes',
		'measurement_reading'
	]
	specaial_fields_values = {
		'measurement_notes': [],
		'measurement_reading': []
	}
	for field_set in field_sets:
		if 'identifier' not in field_set or 'opacObjectFields' not in field_set:
			continue
		if field_set['identifier'] in ignore_fields:
			continue
		value = ''
		if field_set['identifier'] in specaial_fields:
			if field_set['identifier'] == 'measurement_reading':
				specaial_fields_values['measurement_reading'] = field_set['opacObjectFields']
				continue
			elif field_set['identifier'] == 'measurement_notes':
				specaial_fields_values['measurement_notes'] = field_set['opacObjectFields']
				value = process_measurement_notes(specaial_fields_values['measurement_notes'],
				                                  specaial_fields_values['measurement_reading'])
				result['measurements'] = value
		else:
			for field_value in field_set['opacObjectFields']:
				if value != '':
					value += '; '
				value += field_value['value']
			result[field_set['identifier']] = value
	return result


def process_measurement_notes(measurement_notes, measurement_reading):
	# print(measurement_notes, measurement_reading)
	measurements = []
	for i, notes in enumerate(measurement_notes):
		if i < len(measurement_reading):
			measurements.append(f'{notes["value"]}: {measurement_reading[i]["value"]}; ')
	result = ''.join(measurements)
	return result


def get_images(images):
	result = []
	for image in images:
		result.append(image['imageDerivatives'][0]['url'])
	if len(result) == 0:
		return ''
	return '; '.join(result)


def get_all_collections_info(api_url, collections):
	collections_info = []
	print("\nGetting all collections info...")
	for collection in tqdm(collections):
		collection_info = get_collection_info(api_url, collection)
		if collection_info == {}:
			continue
		collections_info.append(collection_info)
	print("\nAll collections info have been fetched.")
	return collections_info


def to_upper_camel_case(x):
	s = re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), x.lower())
	return s


def get_columns():
	csv_columns = config.COLUMNS
	csv_header = []
	for column in csv_columns:
		csv_header.append(to_upper_camel_case(column))
	return csv_columns, csv_header


def output_to_csv(collections):
	csv_columns, csv_names = get_columns()
	df = pd.DataFrame(collections)
	df.to_csv('auckland-museum-collections.csv',
	          index_label='id',
	          columns=csv_columns,
	          header=csv_names,
	          encoding='utf-8-sig')


def main():
	base_url = 'https://www.aucklandmuseum.com/discover/collections/search?k=chinese'
	api_url = 'https://collection-api.aucklandmuseum.com/api/v3/opacobjects/'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
	}
	collections = get_all_collections(base_url, headers)
	collections_info = get_all_collections_info(api_url, collections)
	output_to_csv(collections_info)


def test():
	url = f'https://www.aucklandmuseum.com/discover/collections/search?k=chinese'
	api_url = f'https://collection-api.aucklandmuseum.com/api/v3/opacobjects/'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
	}
	test_id = 738488
	collection = get_collection_info(api_url, test_id)

	collections = [collection]

	output_to_csv(collections)


if __name__ == '__main__':
	main()
