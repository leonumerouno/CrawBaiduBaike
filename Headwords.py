# coding:utf8
import urllib.request
import re
import urllib.parse
from bs4 import BeautifulSoup
# coding:utf8
class UrlManager(object):
    #初始化，待爬取URL和已爬取URL
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    #添加新URL进管理器
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    #批量添加URLS
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0
    #pop方法可以把其中的一个URL给弹出，并且移除
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

# coding:utf8
class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None

        response = urllib.request.urlopen(url)

        if response.getcode() !=200:
            return None

        return response.read()

# -*- coding: UTF-8 -*-
class HtmlParser(object):

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # /view/123.htm
        links = soup.find_all('a', href=re.compile(r"/view/\d+\.htm"))
        for link in links:
            new_url = link['href']
            #urljoin 函数可以将new_url 按page_url 的格式拼接成一个全新的url
            new_full_url = urllib.parse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls
    #获取的数据为 title and summary
    def _get_new_data(self, page_url, soup):
        res_data = {}

        #url
        res_data['url'] = page_url

        #获取 title
        #<dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        title_node = soup.find('dd',class_="lemmaWgt-lemmaTitle-title").find('h1')
        res_data['title'] = title_node.get_text()

        #获取 summary
        #<div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div',class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()

        return res_data

class HtmlOutputer(object):

        def __init__(self):
            self.datas = []

        def collect_data(self, data):
            if data is None:
                return
            self.datas.append(data)

        def output_html(self):
            fout = open('outputer.html', 'w')

            fout.write("<html>")
            fout.write('<body>')
            fout.write('<table>')

            # ascii
            for data in self.datas:
                fout.write("<tr>")
                fout.write('<td>%s</td>' % data['url'])
                fout.write('<td>%s</td>' % data['title'].encode("utf-8"))
                fout.write('<td>%s</td>' % data['summary'].encode("utf-8"))
                fout.write("</tr>")

            fout.write('</table>')
            fout.write('</body>')
            fout.write("</html>")

            fout.close()


class Spider_Main(object):
    #爬虫的初始化，管理器、下载器、解析器、输出器
    def __init__(self):
        self.urls = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()

    # coding:utf8
    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            #有一些URL已经失效，或者无法访问，所以我们需要添加特殊情况
            try:
                new_url = self.urls.get_new_url
                print ('craw %d : %s'%(count,new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url,html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                #只爬取1000个
                if count ==1000:
                    break
                count = count +1
            except:
                print ("craw failed")


        self.outputer.output_html()

if __name__ =="__main__":
    root_url = "https://baike.baidu.com/item/Python/407313"
    obj_spider = Spider_Main()
    obj_spider.craw(root_url)
