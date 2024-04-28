# Mysql数据

### 建表

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
    imageUrl TEXT
);
```

### 将csv转成sql

```sql
LOAD DATA INFILE 'D:\\work\\project\\KMS\\数据爬取\\Data\\Final\\merged-data.csv'
INTO TABLE artifacts
character set utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '\"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
```

