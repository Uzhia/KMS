## make.py功能：
对数据进行一定的整理
- 可以给多次出现的文物名字加后缀，使其唯一，例如五铢钱，五铢钱2，五铢钱3。。。
- 剔除空值字段使其不出现在三元组文件中，使其不会出现在知识图谱的节点上
- 把源文件data.csv中的一些数据放入文物节点的信息中，而不使其在节点上
- 文物在知识图谱中的entityID和源文件data.csv的第一列字段id对应

生成三元组文件文件triples.txt

通过triples.txt得到所有的节点存放至entities.csv中，并区分文物节点和其他信息节点，文物节点会有更多的信息

通过triples.txt得到所有的关系存放至roles.csv中

## 导入到neo4j:

在neo4j的安装路径的bin目录使用命令行，输入

`neo4j-admin.bat import --nodes [entities.csv所在的绝对路径] --relationships [roles.csv所在的绝对路径] --force`

例如：`neo4j-admin.bat import --nodes D:\a.csv --relationships D:\b.csv --force`进行导入
