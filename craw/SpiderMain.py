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
        names = self.sourcedata.get_entity_names()
        for name in names:
            now_url = self.urls.create_url(name)
            # print(now_url)
            urls,dif_names,upper_names = self.parser.get_difnames_url(now_url)

            if len(urls) > 0:
                for i in range(0,len(urls) - 1):
                    dif_tags, dif_values = self.parser.tuples(urls[i])
                    dif_name = dif_names[i]
                    upper_name = upper_names[i]
                    self.sourcedata.insert_into_main(dif_name,dif_tags,dif_values)
                    self.sourcedata.insert_into_difnames(name,dif_name,urls[i])
                    self.sourcedata.insert_into_uppername(dif_name,upper_name)

if __name__ =="__main__":
    obj_spider = Spider_Main()
    obj_spider.craw()