from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
    def download_edit_history(self, url):
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--headless')
        s = Service('chromedriver.exe')

        driver = webdriver.Chrome(service=s, options=options)
        sleep(5)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        driver.get(url)
        driver.refresh()

        sleep(5)

        page_source = driver.page_source
        sleep(5)

        return page_source

    def download_user(self, url):
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--headless')
        s = Service('chromedriver.exe')

        driver = webdriver.Chrome(service=s, options=options)
        sleep(5)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        driver.get(url)
        driver.refresh()

        sleep(5)

        wait = WebDriverWait(driver, 10)  # 设置等待时长
        confirm_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,"#floor-www-index_558 > div > div.www-home-content.active > div.headlines > div.headlines-right > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(1) > a.title")
            )
        )
        confirm_btn.click()

        sleep(5)
        page_source = driver.page_source

        return page_source