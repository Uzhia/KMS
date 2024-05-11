import csv
#源文件中所有的字段
#id,name,time,creator,level,placeOfOrigin,museum,type,size,material,description,collectionUrl,imageUrl

#relations为知识图谱中会出现的字段，indexs每个元素表示relations中对应元素在源文件中的位置，例如'年代'对应的index为2，'藏品等级'为4
relations = ['年代', '藏品等级', '藏品原产地', '现藏博物馆', '类型', '藏品材质']
indexs = [2, 4, 5, 6, 7, 9]
#details_relations为藏品节点所独有的信息，indexs_details每个元素表示details_relations中对应元素在源文件中的位置
indexs_details = [3, 8, 10, 11, 12]
details_relations = ['创作者', '藏品尺寸', '藏品描述', '藏品网址', '图片链接']
#表示文物结点的个数，为了使节点名统一，通过该dict方便加后缀
times = {}
#生成的三元组（不包括空字段）
triples = []
cnt = 0
#保存对应文件及其不会出现在知识图谱中的详细信息
details = {}
relic_id = {}#保存藏品的对应entityId
info_id = {}
id = 0
#merged-data.csv为总的数据
with open('data.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        #跳过第一行
        if cnt == 0:
            cnt = 1
            continue
        #给重复的文物名加后缀使其唯一
        if row[1] in times:
            times[row[1]] += 1
        else:
            times[row[1]] = 1
        if times[row[1]] > 1:
            row[1] = row[1] + str(times[row[1]])
        relic_id[row[1]] = row[0]
        id += 1
        #print(row[1])
        info_tmp = []
        #保存文物对应的详细信息
        for x in indexs_details:
            info_tmp.append(row[x])
        details[row[1]] = info_tmp
        #制作三元组
        for i in range(len(relations)):
            if row[indexs[i]] == '无' or row[indexs[i]] == 'Unknown' or row[indexs[i]] == '未知':
                continue
            triples.append([row[1], relations[i], str(row[indexs[i]])])
# 将数据写入文件
with open('triples.txt', 'w', encoding='utf-8') as output_file:
    for triple in triples:
        output_line = '\t'.join(triple) + '\n'
        output_file.write(output_line)

# 初始化三个空列表，用于保存三元组的每一列
#entity_h中存放的都是文物节点，role中存放关系，entity_t存放的是其他类型的节点，例如年代，藏品等级等
entity_h = []
role = []
entity_t = []

# 读取文件中的每一行，使用 'utf-8' 编码器
with open('triples.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 使用split()函数分割每一行，以空格或其他分隔符为准
        elements = line.strip().split('\t')
        if len(elements) < 3:
            continue
        # 将每个元素添加到相应的列表中
        entity_h.append(elements[0])
        role.append(elements[1])
        entity_t.append(elements[2])

# 去除重复实体
entity_1 = set(entity_h)
entity_2 = set(entity_t) # 将所有entity_h中的实体添加到entity1中

# 保存节点文件
with open("entities.csv", "w", newline='', encoding='utf-8') as csvf_entity:
    w_entity = csv.writer(csvf_entity)
    # 写入表头
    w_entity.writerow(("entity:ID", "name", ":LABEL", "创作者", "藏品尺寸", "藏品描述", "藏品网址", "图片链接"))
    # 写入节点信息
    for entity in entity_1:
        LABEL = "relic"
        detail_info = details.get(entity, "")  # 使用字典的get方法，如果实体不存在于details中，则返回默认值""
        if detail_info != "":
            #此时节点是文物节点，将detail_info中保存的各个字段信息写入
            creator = detail_info[0]
            size = detail_info[1]
            description = detail_info[2]
            collectionUrl = detail_info[3]
            imageUrl = detail_info[4]
            w_entity.writerow(("e" + str(relic_id[entity]), entity, LABEL, creator, size, description, collectionUrl, imageUrl))
        else:
            print("ERROR")
    idx = 0
    for entity in entity_2:
        LABEL = "info"
        # 此时节点不是文物节点，detail_info信息置空字符串
        w_entity.writerow(("e" + str(id + idx), entity, LABEL, detail_info))
        info_id[entity] = id + idx
        idx += 1

# 保存关系文件
with open("roles.csv", "w", newline='', encoding='utf-8') as csvf_roles:
    w_roles = csv.writer(csvf_roles)
    # 写入表头
    w_roles.writerow((":START_ID", ":END_ID", ":TYPE"))
    # 写入关系信息
    for h, r, t in zip(entity_h, role, entity_t):
        w_roles.writerow(("e" + str(relic_id[h]), "e" + str(info_id[t]), r))


