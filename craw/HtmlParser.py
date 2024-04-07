import HtmlDownloader
import json
from bs4 import BeautifulSoup
class HtmlParser(object):
    def __init__(self):
        self.downloader = HtmlDownloader.HtmlDownloader()

    def tuples(self, url):
        html_cont = self.downloader.download(url)
        soup = BeautifulSoup(html_cont, 'lxml', from_encoding='utf-8')

        titleTag = soup.find_all("dt")
        titleValue1 = soup.select('dd')

        titleValue = []
        for dd in titleValue1:
            attr = dd.attrs
            if not bool(attr):
                continue
            titleValue.append(dd.text)

        tags = []

        for tag in titleTag:
            if tag.find("a"):
                continue
            rtag = tag.text.replace(' ', '')
            tags.append(rtag)

        return tags,titleValue

    def get_difnames_url(self,url):
        html_cont = self.downloader.download(url)

        soup = BeautifulSoup(html_cont, 'lxml', from_encoding='utf-8')

        titleScript = soup.find_all("script")
        if len(titleScript) == 0:
            return []

        scripttext = ""

        for script in titleScript:
            if len(script) > 0 and script.text[0] == 'w' and script.text[7] == 'P':
                scripttext = script.text[18:]

        python_obj = json.loads(scripttext)
        navigations = python_obj.get('navigation')

        if navigations == None:
            return [],[],[]

        result = navigations.get('lemmas')

        urls = []
        difnames = []
        uppernames = []

        for dict in result:
            id = dict.get('lemmaId')
            id_url = url + "/" + str(id)
            urls.append(id_url)

            difname = dict.get('lemmaTitle') + '[' + dict.get('lemmaDesc') + ']'
            difnames.append(difname)

            uppernames.append(dict.get('classify'))

        return urls,difnames,uppernames

