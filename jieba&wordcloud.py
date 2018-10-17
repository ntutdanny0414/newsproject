# -*- coding: utf-8 -*-
import json
import jieba
from wordcloud import WordCloud ,ImageColorGenerator
from scipy.misc import imread  # 處理圖的函数
frame = imread('trump.png')  # 图片
jieba.case_sensitive = True # 可控制對於詞彙中的英文部分是否為case sensitive, 預設False
#開檔
with open ('news.json', 'r',encoding = 'utf8') as f:
    olddata = json.load(f)
data = []
def cut(data, num):
    seg_list = jieba.cut(olddata[num]['content'].replace(' ','').replace('facebook','').replace('。','').replace('，',''))
    data.extend(seg_list)
#切字
for i in range(0, len(olddata)):
    cut(data, i)
#小數據
d = []
for i in range(50):
    d.append(data[i])
#print('/'.join(data))
#text = {e:data.count(e) for e in data}太多
text = {e:d.count(e) for e in d}
font = r'C:\Windows\Fonts\kaiu.ttf'#chinese
wc = WordCloud(background_color="white",font_path=font,mask=frame, max_words=2000,max_font_size=40, random_state=42)

wc.generate_from_frequencies(text)
image_colors = ImageColorGenerator(frame)#對應顏色
import matplotlib.pyplot as plt
#隨機顏色
plt.imshow(wc)
plt.axis("off")
wc.to_file('trumpcolor.png')#save
#照圖來
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')
wc.to_file('trumptest.png')#save