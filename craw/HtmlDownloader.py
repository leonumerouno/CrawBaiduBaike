from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
class HtmlDownloader(object):
    def download(self, url):
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--headless')
        s = Service('chromedriver.exe')

        driver = webdriver.Chrome(service=s, options=options)
        sleep(5)
        driver.get(url)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        sleep(10)

        page_source = driver.page_source
        sleep(5)

        return page_source