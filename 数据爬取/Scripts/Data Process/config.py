COLUMNS = [
	"name",
	"time",
	"creator",
	"level",
	"placeOfOrigin",
	"museum",
	"type",
	"size",
	"material",
	"description",
	"collectionUrl",
	"imageUrl"
]

# 字段对应介绍
COLUMNS_MAP = {
	"id": "文物编号",
	"name": "名字",
	"time": "文物诞生时间",
	"creator": "制造者",
	"level": "文物等级",
	"placeOfOrigin": "文物出土地点 或者来源地",
	"museum": "在哪个博物馆",
	"type": "类型",
	"size": "尺寸",
	"material": "材料",
	"description": "文物描述",
	"collectionUrl": "文物详情页链接",
	"imageUrl": "文物图片下载链接"
}

DATA_BASE_PATH = "../../Data/Raw Data"
HENAN_MUSEUM_PATH = f"{DATA_BASE_PATH}/henan-collections.csv"
AUCKLAND_MUSEUM_PATH = f"{DATA_BASE_PATH}/auckland-museum-collections.csv"
PROCESSED_DATA_PATH = "../../Data/Processed"
MERGED_DATA_PATH = "../../Data/Final/merged-data.csv"
