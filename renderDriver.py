#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 10:58 AM
# @Author  : MADAO

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class RenderDriver(object):

    chrome_options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values.images': 2
    }
    chrome_options.add_experimental_option('prefs', prefs)
    # 不提供可视化页面
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("user-data-dir=selenium") 
    browser = webdriver.Chrome(options=chrome_options)

    wait = WebDriverWait(browser, 10)

    def __init__(self):
        super().__init__()

    @classmethod
    def load_pagination(cls, url, retry=3):
        if retry == 0:return None
        try:
            cls.browser.get(url)
            cls.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#referenceList')))
            html = cls.browser.page_source
            
            cls.browser.close()
            return html
        except TimeoutException as e:
            load_pagination(url, retry=retry-1)

if __name__ == "__main__":
    url = "https://www.scopus.com/record/display.uri?eid=2-s2.0-85084042488&origin=resultslist&sort=plf-f&src=s&st1=accounting&nlo=&nlr=&nls=&sid=5ecf55b57334be073e10359345e07f95&sot=b&sdt=b&sl=20&s=SRCTITLE%28accounting%29&relpos=0&citeCnt=0&searchTerm="
    RenderDriver.load_pagination(url=url)