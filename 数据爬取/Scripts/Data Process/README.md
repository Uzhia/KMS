# 数据处理说明

`config.py`中存放的为配置信息，直接使用即可。

```python
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
```

merge.py为合并数据的脚本，可以直接将Processed目录下的数据合并为一个文件。

***要求每个csv的字段一致，为config.py中的字段。***
