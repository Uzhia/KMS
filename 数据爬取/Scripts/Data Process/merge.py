import os

import pandas as pd

import config


def get_file_list():
	file_list = []
	for file in os.listdir(config.PROCESSED_DATA_PATH):
		if file.endswith('.csv'):
			file_list.append(os.path.join(config.PROCESSED_DATA_PATH, file))
	return file_list


def merge_csv(file_list):
	dfs = []
	for file in file_list:
		df = pd.read_csv(file)
		dfs.append(df)
	new_data = []
	c_id = 0
	for df in dfs:
		for index, row in df.iterrows():
			c_id += 1
			row['id'] = c_id
			new_data.append(row)
	df = pd.DataFrame(new_data)
	return df


def main():
	file_list = get_file_list()
	df = merge_csv(file_list)
	df.to_csv(config.MERGED_DATA_PATH, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
	main()
