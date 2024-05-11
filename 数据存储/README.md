# csv数据

后面带`_tran`就是原文的翻译后内容，如果原文为中文，这些项值都为`无`

经过统一后，外文中`空数据`均以`null`表示，中文中`空数据`均以`无`表示。

`a.py`文件用来将`modify1.csv`文件中的imageUrl中多个url转成一个url。

> 注意：csv文件中的id不代表mysql中的id。
> 所有csv文件编码均为`utf-8`(不是`utf-8 with bom`)，使用excel打开会中文乱码。

# Mysql数据

### 建表

其中:

- `artifacts`的csv数据为`final.csv`
- `artifacts2`的csv数据为`modified_file.csv`

```sql
CREATE TABLE artifacts (
  id INT,
  name TEXT,
  time VARCHAR(255),
  creator VARCHAR(255),
  level VARCHAR(255),
  placeOfOrigin VARCHAR(255),
  museum VARCHAR(255),
  type VARCHAR(255),
  size TEXT,
  material TEXT,
  description TEXT,
  collectionUrl VARCHAR(255),
  imageUrl TEXT,
  name_tran TEXT,
  time_tran VARCHAR(255),
  creator_tran VARCHAR(255),
  level_tran VARCHAR(255),
  placeOfOrigin_tran VARCHAR(255),
  museum_tran VARCHAR(255),
  type_tran VARCHAR(255),
  size_tran TEXT,
  material_tran TEXT,
  description_tran TEXT
);

CREATE TABLE artifacts2 (
  id INT,
  name TEXT,
  time VARCHAR(255),
  creator VARCHAR(255),
  level VARCHAR(255),
  placeOfOrigin VARCHAR(255),
  museum VARCHAR(255),
  type VARCHAR(255),
  size TEXT,
  material TEXT,
  description TEXT,
  collectionUrl VARCHAR(255),
  imageUrl TEXT
);
```

### 将csv转成sql

> 注意：必须将文件放在`C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\`里面才能导入！

```sql
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\modified_file.csv'
INTO TABLE artifacts2
character set utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '\"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
```

