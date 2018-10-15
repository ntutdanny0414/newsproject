# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
from pprint import pprint
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
                time.sleep(3)
        except:
            print('oh~oh~')
    def Start(self):
        self.newsurl()
        self.CrawlAllNews()
def main():
    keyWord = input("請輸入關鍵字: ")
    find = news(keyWord)
    find.Start()
    pprint(find.news)
main()