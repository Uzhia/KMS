import pandas as pd

import config


def get_data():
	df = pd.read_csv(config.HENAN_MUSEUM_PATH)
	datas = []
	# 遍历每一行
	for index, row in df.iterrows():
		data = {}
		for column in df.columns:
			data[column] = row[column]
		datas.append(data)

	return datas


def process_data(datas):
	new_datas = []
	for data in datas:
		new_data = {}
		for column in config.COLUMNS:
			if column in data:
				new_data[column] = data[column]
			else:
				if column == 'museum':
					new_data[column] = '河南博物院'
				elif column == 'level':
					new_data[column] = '普通'
				else:
					new_data[column] = '未知'
		new_datas.append(new_data)
	return new_datas


def main():
	datas = get_data()
	new_datas = process_data(datas)
	df = pd.DataFrame(new_datas)
	df.to_csv("henan-processed.csv", index_label='id', columns=config.COLUMNS,
	          encoding='utf-8-sig')


if __name__ == '__main__':
	main()
