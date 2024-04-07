import HtmlDownloader
import json
from bs4 import BeautifulSoup
class HtmlParser(object):
    def __init__(self):
        self.downloader = HtmlDownloader.HtmlDownloader()

    def tuples(self, url):
        html_cont = self.downloader.download(url)
        soup = BeautifulSoup(html_cont, 'lxml', from_encoding='utf-8')
        htmlPrettify = soup.prettify()

        titleTag = soup.find_all("dt")
        titleValue1 = soup.find_all("dd")
        titleValue2 = soup.find_all("span")

        tmp = []
        titleValue = []
        for dd in titleValue1:
            if dd.text != "":
                tmp.append(dd.text)
        for span in titleValue2:
            if span.text in tmp:
                titleValue.append(span.text)

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
        htmlPrettify = soup.prettify()

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

