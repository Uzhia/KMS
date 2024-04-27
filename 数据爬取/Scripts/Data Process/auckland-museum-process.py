from cmath import nan

import pandas as pd

import config


def get_data():
	df = pd.read_csv(config.AUCKLAND_MUSEUM_PATH)
	datas = []
	# for col in df.columns:
	# 	print(col)
	# 遍历每一行
	for index, row in df.iterrows():
		data = {}
		for column in df.columns:
			data[column] = row[column]
		datas.append(data)

	return datas


def process_column(data, column):
	if column in data:
		if data[column] == "":
			return '未知'
		return data[column]
	elif column == 'size':
		if data['measurements'] == ': ; ':
			return '未知'
		elif data['measurements'].startswith(': '):
			return data['measurements'][2:]
		return data['measurements']
	elif column == 'material':
		materials = data['mediaMaterials']
		if materials == "":
			return '未知'
		return materials
	elif column == 'time':
		if data['date'] == "":
			return '未知'
		return data['date']
	elif column == 'museum':
		return "奥克兰战争纪念馆"
	elif column == 'type':
		if data['collectionType'] == '' or data['collectionType'] == 'nan':
			return '未知'
		return data['collectionType']
	elif column == 'imageUrl':
		if data['images'] == "[]" or data['images'] == "":
			return ''
		return data['images']
	elif column == 'collectionUrl':
		c_id = data['collectionid']
		return f"https://www.aucklandmuseum.com/discover/collections/record/{c_id}?k=chinese"
	elif column == 'level':
		if data['levelCurrentRecord'] == "":
			return '未知'
		return data['levelCurrentRecord']
	return '未知'


def process_data(datas):
	new_datas = []
	for data in datas:
		new_data = {}
		for column in config.COLUMNS:
			new_data[column] = process_column(data, column)
		new_datas.append(new_data)
	return new_datas


def main():
	datas = get_data()
	new_datas = process_data(datas)
	df = pd.DataFrame(new_datas)
	df.to_csv(config.AUCKLAND_MUSEUM_PROCESSED_PATH, index_label='id', columns=config.COLUMNS,
	          encoding='utf-8-sig')


if __name__ == '__main__':
	main()
