import jieba  # 分词
from matplotlib import pyplot as plt  # 绘图，数据可视化
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算
import sqlite3  # 数据库

# 准备词云
conn = sqlite3.connect("movie.db")
cur = conn.cursor()
sql = "select introduction from movie250"
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
cur.close()
conn.close()

# 分词
cut = jieba.cut(text)
words = ' '.join(cut)
img = Image.open(r'./static/assets/img/cloud.jpg')  # 打开遮罩图片
img_array = np.array(img)  # 将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask=img_array,  # 遮罩文件
    font_path="msyh.ttc"  # 字体文件
)
wc.generate_from_text(words)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')  # 是否显示坐标轴
# plt.show()  # 显示生成的词云图片
plt.savefig(r'./static/assets/img/wordcloud.jpg', dpi=500)  # 输出词云图片到文件
