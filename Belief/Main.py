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
        entity_urls = self.sourcedata.get_entity_urls()
        for url in entity_urls:
            lemmaIds, difnames, lemmaTitles, uppernames = self.parser.get_lemmas(url)
            n = len(lemmaIds)
            for i in range(n):
                # 每一个页面对应了n个作者
                history_url = self.urls.create_history_url(lemmaTitles[i],lemmaIds[i])
                editor_name,editor_urls,edit_times,edited_times = self.parser.get_editor_urls(history_url)
                self.sourcedata.insert_into_create_history(difnames[i],url,edited_times,history_url)
                m = len(editor_name)
                for j in range(m):
                    self.sourcedata.insert_into_edit(editor_name[j],difnames[i],edit_times[j])
                    passed_versions, pass_rate, special_versions, helped_people = self.parser.get_editor_infos(editor_urls[j])
                    self.sourcedata.insert_into_editors(editor_name[j],editor_urls[j],passed_versions,pass_rate,special_versions,helped_people)

if __name__ =="__main__":
    obj_spider = Spider_Main()
    obj_spider.craw()