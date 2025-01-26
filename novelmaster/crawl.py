

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class Crawl():
    def __init__(self):
        return
    
    def openBrowser(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(time_to_wait=10)
    
    def closeBrowser(self):
        self.browser.close()
    
    def syosetuCrawl(self, target_url, episode):
        self.browser.get(target_url + episode)
        time.sleep(2)
        # wait for complete load
        
        novel_subTitle_1 = self.browser.find_elements(By.TAG_NAME, "span")[5]
        novel_subTitle_2 = self.browser.find_element(By.TAG_NAME, "h1")
        novel_body = self.browser.find_element(By.CLASS_NAME, "p-novel__body")
        text = (novel_subTitle_1.text + "\n"
                + novel_subTitle_2.text + "\n\n"
                + novel_body.text)
        return text
    
    def bakafireCrawl():
        pass
    '''
        http://bfpblog.bakafire.main.jp/
    '''

#%% test

if __name__ == '__main__':
    base_url = "http://bfpblog.bakafire.main.jp/"
    browser = webdriver.Chrome()
    browser.get(base_url)
    links = browser.find_elements()
    url_list = []
    for link in links:
        url = link.get_attribute('href')
        if base_url == url[:(len(base_url))]:
            url_list.append(url)
    browser.close()
