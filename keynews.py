# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
#import time
#from pprint import pprint
class news:
    def __init__(self, keyWord):
        self.keyWord = keyWord
        self.urlList = []
        self.singleNewsSoup = None
        self.news = []
        self.singleNews = {'title':'', 'time':'', 'content':'', 'resource':'', 'url':''}
    def newsurl(self):
        for i in range(1,4):
            res = requests.get('https://www.ettoday.net/news_search/doSearch.php?keywords={}&idx=1&page='.format(self.keyWord)+str(i))
            soup = BeautifulSoup(res.text, 'html.parser')
            for link in soup.findAll('div',class_='box_1'):
                self.urlList.append(link.find('a')['href'])
    def GetNewsSoup(self, link):
        res = requests.get(link)
        self.singleNews['url'] = link
        self.singleNewsSoup = BeautifulSoup(res.text, 'html.parser')
    def GetTitle(self):
        self.singleNews['title'] = self.singleNewsSoup.find('h1',class_='title').get_text()#.strip()
    def GetTime(self):
        self.singleNews['time'] = self.singleNewsSoup.find('time',class_='date').get_text().strip()
    def GetContent_Resource(self):
        temp = self.singleNewsSoup.find('div',class_='story').find_all('p')
        article = []
        for i in temp:
            if i.find('img') == None and i.find('strong') == None:
                article.append(i.get_text().strip().replace(' ',''))
        allword = ''
        for i in range(1,len(article)):
            allword = allword + article[i]
        self.singleNews['content'] = allword
        self.singleNews['resource'] = article[0]#.split('／')[0]
    def CrawlAllNews(self):
        try:
            for link in self.urlList:
                self.GetNewsSoup(link)
                self.GetTitle()
                self.GetTime()
                self.GetContent_Resource()
                self.news.append(self.singleNews)
                self.singleNews = {'title':'', 'time':'', 'content':'', 'resource':'', 'url':''}
                print('hihi')
#                time.sleep(3)
        except:
            print('oh~oh~')
    def Start(self):
        self.newsurl()
        self.CrawlAllNews()
import jieba
import jieba.analyse
from wordcloud import WordCloud ,ImageColorGenerator
#from scipy.misc import imread  # 處理圖的函数
from collections import Counter
import matplotlib.pyplot as plt

from PIL import Image
import numpy as np
from io import BytesIO
def getimage(url):#要白底
    response = requests.get(url)
    img = np.array(Image.open(BytesIO(response.content)))
    return img
#frame = imread('trump.png')圖片
jieba.case_sensitive = True # 可控制對於詞彙中的英文部分是否為case sensitive, 預設False
stopwords = []
with open('stopWords.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopwords.append(data)

class jiebacut:
    def __init__(self, content,keyWord,frame):
        self.content = content
        self.keyWord = keyWord
        self.frame = frame
        self.data = []
    def cut(self,num):
#        seg_list = jieba.cut(self.content[num]['content'].replace(' ',''))
#        self.data.extend(seg_list)
        seg_list = jieba.analyse.extract_tags(self.content[num]['content'].replace(' ',''), topK=30, withWeight=True, allowPOS=())
        for i in range(0,len(seg_list)):
            self.data.append(seg_list[i][0])
        self.data = list(filter(lambda a: a not in stopwords and a != '\n', self.data))
    def make(self):
        for i in range(0, len(self.content)):
            self.cut(i)
        sorted(Counter(self.data).items(), key=lambda x:x[1], reverse=True)
        font = r'C:\Windows\Fonts\kaiu.ttf'#chinese
        wc = WordCloud(background_color="white",font_path=font,mask=self.frame,max_font_size=200,random_state=42,stopwords=stopwords,max_words=500)#collocations=False,
        wc.generate_from_frequencies(frequencies=Counter(self.data))
        image_colors = ImageColorGenerator(self.frame,(255,255,255))#對應顏色 #需要去背
        plt.figure()
        plt.imshow(wc.recolor(color_func=image_colors))
        plt.axis('off')
        wc.to_file(self.keyWord+'.png')#save
def main():
    keyWord = input("請輸入關鍵字: ")
    imageurl = input("合成圖片: ")
    find = news(keyWord)
    find.Start()
    frame = getimage(imageurl)
    wordcloud = jiebacut(find.news,keyWord,frame)
    wordcloud.make()
main()