#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 13:15 AM
# @Author  : MADAO

from lxml import etree
from models.SearchListModel import SearchListModel

class SearchListParser(object):
    def __init__(self, html):
        super().__init__()

        # 当前解析的html
        self.html = html
        # 解析成功标志
        self.parse_successed = False
        # 当前页面
        self.current_page_index = 0
        # 下一页面
        self.next_page_index = 0
        # 搜索结果对象
        self.search_list = []
        # 分页 js submitOnPaginationLinkClick($(this).closest('form'),'1');
        self.next_pagination_js = None

    def parse(self):
        if self.html == None:
            return
        
        root = None
        try:
            root = etree.HTML(self.html)
            # root = tree.getroot()
        except Exception as e:
            print(e)
            pass
        
        if root == None: return
        # 查找page 下标 
        pagination = root.xpath('//ul[@class="pagination"]/li/a')
        if pagination and len(pagination):

            # 获取当前页和下一页
            for page in pagination:
                att = page.attrib
                # 查找当前page
                if att and att.has_key("class") and att["class"] == "selectedPage":
                    self.current_page_index = int(att.get("data-value", 0))
                # 查找下一个page
                elif att and self.current_page_index > 0:
                    self.next_page_index = int(att.get("data-value", 0))
                    self.next_pagination_js = page.get("onclick", "").replace("$(this)", '''$("[data-value='{}']")[0]'''.format(self.next_page_index))
                    break

        # 解析 content 列表
        content_panel = root.xpath('//table[@id="srchResultsList"]//tr[@class="searchArea"]')
        for panel in content_panel:
            tr_list = panel.xpath(".//td")
            
            if len(tr_list) != 5:continue

            model = SearchListModel()
            # 标题
            model.title = "".join(tr_list[0].itertext()).strip()
            hrefs = tr_list[0].xpath('./a/@href')
            if hrefs and hrefs[0]:
                model.title_link = hrefs[0]

            # 作者
            author = []
            for au in tr_list[1].xpath('.//a'):
                name = au.text
                link = au.get("href", "")
                author.append((name, link))
            model.author = author
            
            # 年份
            model.year = "".join(tr_list[2].itertext()).strip()

            # 出版物
            journal_group = filter(
                lambda x:len(x.strip("\r\n")),
                list(tr_list[3].itertext())
            )
            journal_group = list(journal_group)
            model.journal = journal_group[0]
            if len(journal_group) > 1:
                model.journal_no = "".join(journal_group[1:]).replace("\n", "")

            journal_link = tr_list[3].find('.//a')
            if journal_link is not None:
                model.journal_link = journal_link.get("href", "")
            
            self.search_list.append(model)
            
        print(self.search_list)
        # 解析完成
        self.parse_successed = True

if __name__ == "__main__":
    import codecs
    path = "./test.html"
    with codecs.open(path, "r") as file:    
        search = SearchListParser(file.read())
        search.parse()
        print(search.search_list)

