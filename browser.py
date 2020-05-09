#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 10:58 AM
# @Author  : MADAO

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

from handler.search_list_parser import SearchListParser
from renderDriver import RenderDriver
import sys
import re
from collections import OrderedDict

class MainWindow(QMainWindow):

    # noinspection PyUnresolvedReferences
    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('Scopus Browser')
        # 设置窗口图标
        self.setWindowIcon(QIcon('icons/penguin.png'))
        # 设置窗口大小1200*900
        self.resize(1200, 900)
        self.show()

        # 设置浏览器
        self.browser = QWebEngineView()
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)

        ###使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        #添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        #QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        next_button = QAction(QIcon('icons/next.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/cross.png'), 'stop', self)
        reload_button = QAction(QIcon('icons/renew.png'), 'reload', self)

        back_button.triggered.connect(self.browser.back)
        next_button.triggered.connect(self.browser.forward)
        stop_button.triggered.connect(self.browser.stop)
        reload_button.triggered.connect(self.browser.reload)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)

        #添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        #让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.renew_urlbar)

        # 添加操作按钮
        action_button = QAction("解析提取引文", self)
        action_button.triggered.connect(self.parse_html)
        navigation_bar.addAction(action_button)

        # 渲染浏览器
        # self.renderWebView = QWebEngineView()
        self.browser.loadFinished.connect(self.render_load_finished)
        # self.browser.loadProgress.connect(self.render_load_progress)

        # 结果
        self.search_result_page_dict = None
        self.init_result_dict()

        # 是否需要解析
        self.parsing_pages_now = False

    def init_result_dict(self):
        self.search_result_page_dict = OrderedDict()

    def parse_html(self, *args):
        self.init_result_dict()
        self.parsing_pages_now = True
        self.browser.page().toHtml(lambda x: self.__parser_html(x))

    def __parser_html(self, html, scrapy_next = True):
        '''
        爬取下一页面
        '''
        parser = SearchListParser(html)
        parser.parse()
        self.search_result_page_dict.update({
            self.browser.page().url():parser
        })
        
        # 加载下一页面
        if scrapy_next and parser.next_pagination_js and len(parser.next_pagination_js):
            print(parser.next_pagination_js)
            self.browser.page().runJavaScript(parser.next_pagination_js)

            # 测试代码
            self.parsing_pages_now = False
            # 爬取详情代码
            self.__craw_detail_page()
        else:
        # 没有要加载的页面
            self.parsing_pages_now = False
            print(self.search_result_pages)
            print("抓取成功：=========")
            print(len(self.search_result_pages))

    def __craw_detail_page(self):
        pass

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def render_load_finished(self, isOk):
        '''
        渲染成功
        '''
        print("load success: {} for url: {}".format(isOk, self.browser.url()))
        if isOk and self.parsing_pages_now:
            # 渲染成功，进行解析页面
            self.browser.page().toHtml(lambda x: self.__parser_html(x))

    def render_load_progress(self, progress):
        '''
        加载进度
        '''
        print("progress: {} for url: {}".format(progress, self.browser.url()))

    @staticmethod
    def run(url=None):
        # 创建应用
        app = QApplication(sys.argv)
        # 创建主窗口
        window = MainWindow(url=url)
        # 显示窗口
        window.show()
        # 运行应用，并监听事件
        app.exec_()
        

if __name__ == '__main__':
    url = 'https://www.scopus.com/search/form.uri?display=basic&zone=header&origin='
    MainWindow.run(url=url)