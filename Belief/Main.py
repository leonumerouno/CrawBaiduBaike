import UrlManager
import HtmlParser
import HtmlDownloader
import SourceData
class Spider_Main(object):
    def __init__(self):
        self.urls = UrlManager.UrlManager()
        self.downloader = HtmlDownloader.HtmlDownloader()
        self.parser = HtmlParser.HtmlParser()
        self.sourcedata = SourceData.SourceData()

    # coding:utf8
    def craw(self):
        ids,entity_urls = self.sourcedata.get_entity_urls()
        for i in range(0,len(entity_urls)):
            print(entity_urls[i])
            view = self.parser.get_views(entity_urls[i])
            print(view)
            self.sourcedata.update_name_view(ids[i],view)

if __name__ =="__main__":
    obj_spider = Spider_Main()
    obj_spider.craw()