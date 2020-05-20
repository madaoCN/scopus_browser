#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 10:58 AM
# @Author  : MADAO

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from handler.search_list_parser import SearchListParser
from collections import OrderedDict

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
    detail_browser = webdriver.Chrome(options=chrome_options)
    # browser.close()
    detail_wait = WebDriverWait(detail_browser, 15)
    
    # 分页
    pagination_browser = webdriver.Chrome(options=chrome_options)
    # browser.close()
    pagination_wait = WebDriverWait(detail_browser, 15)

    # 分页字典结果
    pagination_result_page_dict = OrderedDict()

    def __init__(self):
        super().__init__()

    @classmethod
    def load_detail_page(cls, url, retry=3):
        if retry == 0:return None
        try:
            cls.detail_browser.get(url)
            cls.detail_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#referenceList')))
            html = cls.detail_browser.page_source
            # cls.browser.close()
            return html
        except TimeoutException as e:
            cls.load_detail_page(url, retry=retry-1)

    @classmethod
    def load_pagination_page(cls, url, retry=3):
        '''
        分页加载
        '''
        if retry == 0:return None
        try:
            cls.pagination_browser.get(url)
            if not len(cls.pagination_result_page_dict):
                # 第一次要加载两遍，否则拿不到页面
                cls.pagination_browser.get(url)
            # cls.pagination_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#referenceList')))
            # html = cls.pagination_browser.page_source
            # # cls.browser.close()
            # return html
        except TimeoutException as e:
            cls.load_pagination_page(url, retry=retry-1)

        # 递归翻页
        try:
            cls.__load_pagination_page()
        except Exception as e:
            print("递归翻页错误")
            print(e)
        
        page_dict = dict(cls.pagination_result_page_dict)
        # 重置
        cls.pagination_result_page_dict = OrderedDict()

        return page_dict

    @classmethod
    def __load_pagination_page(cls):

        html = cls.pagination_browser.page_source
        parser = SearchListParser(html)
        parser.parse()

        # 存入字典
        cls.pagination_result_page_dict.update({
            url:parser
        })

        if parser.next_pagination_js and len(parser.next_pagination_js):
            # 执行 翻页 js
            cls.pagination_browser.execute_script(parser.next_pagination_js)
            # 递归翻页
            cls.__load_pagination_page()
        else:
            return

if __name__ == "__main__":
    pass
    # url = "https://www.scopus.com/record/display.uri?eid=2-s2.0-0034423067&origin=resultslist&sort=plf-f&src=s&st1=Budgeting%3a+An+experimental+investigation+of+the+effects+of+negotiation&st2=&sid=95cff0480646c14dd7216f66bd360934&sot=b&sdt=b&sl=77&s=TITLE%28Budgeting%3a+An+experimental+investigation+of+the+effects+of+negotiation%29&relpos=0&citeCnt=74&searchTerm="
    # result = RenderDriver.load_detail_page(url=url)
    # from handler.search_detail_parser import SearchDetailParser
    # ref_parser = SearchDetailParser(result)
    # ref_parser.parse()
    # print(ref_parser.ref_model_list)

    url = 'https://www.scopus.com/search/submit/references.uri?sort=plf-f&src=r&imp=t&sid=d05c40379100aeabe75e542fca0f4262&sot=rec&sdt=citedreferences&sl=22&s=EID%282-s2.0-0034423067%29&origin=recordpage&citeCnt=1&citingId=2-s2.0-0034423067'
    result = RenderDriver.load_pagination_page(url=url)
    # RenderDriver.detail_browser.close()
    # RenderDriver.pagination_browser.close()
    print(result)
