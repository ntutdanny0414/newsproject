from bs4 import BeautifulSoup
import requests
class apple:
    def __init__(self, keyWord):
        self.keyWord = keyWord
        self.urlList = []
        self.singleNewsSoup = None
        self.news = []
        self.singleNews = {'title':'', 'time':'', 'content':'', 'resource':'', 'url':''}
    def newsurl(self):
        res = requests.get('https://tw.appledaily.com/search/result?querystrS='+self.keyWord)
        soup = BeautifulSoup(res.text, 'html.parser')
        for link in soup.findAll('div',class_='content'):
            self.urlList.append(link.find('a')['href'])                
    def GetNewsSoup(self, link):
        res = requests.get(link)
        self.singleNews['url'] = link
        self.singleNewsSoup = BeautifulSoup(res.text, 'html.parser')
    def GetTitle(self):
        self.singleNews['title'] = self.singleNewsSoup.find('h1').get_text()
    def GetTime(self):
        self.singleNews['time'] = self.singleNewsSoup.find('div',class_='ndArticle_creat').get_text()[5:]
    def GetContent_Resource(self):
        article = self.singleNewsSoup.find('p').get_text().split('。')[:-1]
        self.singleNews['content'] = '。'.join(article) + '。'
        self.singleNews['resource'] = self.singleNewsSoup.find('p').get_text().split('。')[-1].split('）')[0][1:]
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
        except:
            print('oh~oh~')
    def Start(self):
        self.newsurl()
        self.CrawlAllNews()
        
def main():
    keyWord = input("請輸入關鍵字: ")
    find = apple(keyWord)
    find.Start()
main()