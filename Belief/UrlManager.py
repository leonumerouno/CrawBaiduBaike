from urllib import parse
class UrlManager(object):
    #初始化，待爬取URL和已爬取URL
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    def get_search_name(self,url):
        names = url.split('/')
        return parse.unquote(names[4])

    def create_url(self,name):
        encodename = parse.quote(str(name))
        return "https://baike.baidu.com/item/" + encodename

    def create_history_url(self,lemmaTitle,lemmaId):
        encodename = parse.quote(str(lemmaTitle))
        return "https://baike.baidu.com/p/history?lemmaTitle=" + encodename + "&lemmaId=" + str(lemmaId)

    def create_editor_url(self,href):
        return "https://baike.baidu.com" + href

