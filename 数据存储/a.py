import pandas as pd

# 加载CSV文件
df = pd.read_csv('D:\work\project\KMS\数据存储\modify1.csv', encoding='utf-8', na_values=['空'])

# 定义一个函数，用于将包含多个URL的字符串转换为单个URL
# def get_first_url(urls):
#     if urls:  # 检查是否有URL
#         return urls.split(';')[0]  # 返回第一个URL
#     else:
#         return None  # 如果没有URL，则返回None

# 应用该函数到 'imageUrl' 列
# df['imageUrl'] = df['imageUrl'].apply(get_first_url)

# 保存修改后的CSV文件
df.to_csv('D:\work\project\KMS\数据存储\modify1.csv',na_rep='null', index=False, encoding='utf-8')