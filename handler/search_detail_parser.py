#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 13:15 AM
# @Author  : MADAO

from lxml import etree
from models.SearchRefModel import SearchRefModel
import re

class SearchDetailParser(object):

    # 年份匹配
    YEAR_COMPILER = re.compile("[0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3}")
    # 期刊页面匹配
    JOURNAL_PAGE_COMPILER = re.compile("[0-9].+?pp\..+?$")

    def __init__(self, html):

        super().__init__()
        
        self.html = None
        # doi
        self.doi = None
        self.ref_list = []
        # 引用列表
        self.ref_model_list = []
        # 解析成功标志
        self.parse_successed = False
        try:
            # 当前解析的html
            self.html = re.sub("<!--.+?-->", "", html)
        except Exception as e:
            print(e)


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

        # doi 
        doi_node = root.xpath('''//*[@id="recordDOI"]''')
        if len(doi_node):
            self.doi = doi_node[0].text
        reference_lists = root.xpath('//table[@class="referenceLists table"]//tr/td')

        # 递归遍历子节点
        def walk_tree(root_node, content_list, level=0):
            if level > 2:return
            #遍历每个子节点
            content_list.append(root_node)
            children_node = root_node.getchildren()
            if len(children_node) == 0:
                return
            for child in children_node:
                walk_tree(child, content_list, level+1)
            return 

        # 遍历节点
        for reference in reference_lists:
            node_list = []
            walk_tree(reference, node_list)
            content_list = []
            ref_model = SearchRefModel()

            # 查找链接
            page_node_list = reference.xpath(".//a")
            for page_node in page_node_list:
                href = page_node.get("href", "")
                # 查找journal地址
                if href and href.startswith("https://doi.org/"):
                    ref_model.journal_page = href
                # 查找文章地址
                elif href and href.startswith("https://www.scopus.com/record/display.uri"):
                    ref_model.title_link = href
                    ref_model.title = page_node.text
                # 引文地址
                elif href and href.startswith("https://www.scopus.com/search/submit/citedby.uri"):
                    ref_model.ref_link = href

            for index in range(len(node_list)):
                node = node_list[index]
                if node.tag == 'a':
                    content_list.append("[{content}]({link})".format(content="".join(node.itertext()).strip(), link=node.get("href", "")))
                    continue
                if node.text:
                    text = node.text.strip()
                    if len(text):
                        content_list.append(text)
                
                # node tail
                node_tail = node.tail
                if node_tail and len(node_tail.strip()):
                    content_list.append(node_tail.strip()) 

                # doi
                if node_tail and node_tail.strip().startswith("doi"):
                    ref_model.doi = node_tail.split("doi")[-1].strip(": ")
                elif node.text and node.text.strip().startswith("doi"):
                    ref_model.doi = node.text.split("doi")[-1].strip(": ")

                # 查找异常类型标题
                if ref_model.title == None:
                    title_liked_class_name = node.get("class")
                    if title_liked_class_name and re.search("refAuthorTitle", title_liked_class_name):
                        child_nodes = list(node.getchildren())
                        if len(child_nodes) > 2 and \
                            child_nodes[0].tag == "br" and \
                            child_nodes[1].tag == "br":
                            ref_model.title = child_nodes[0].tail
                            
                # author 
                if node.get("class", "") == "refAuthorTitle":
                    author_liked = node.text
                    if author_liked:
                        author_liked = author_liked.strip()
                        if author_liked.endswith("."):
                            ref_model.author = author_liked
                
                # 年份
                year_liked = None
                if node_tail and self.YEAR_COMPILER.search(node_tail):
                    year_liked = re.sub("[()（）]", "", node_tail).strip()
                elif node.text and self.YEAR_COMPILER.search(node.text):
                    year_liked = re.sub("[()（）]", "", node.text).strip()
                if year_liked and year_liked.isnumeric():
                    ref_model.year = year_liked
                
                # journal
                if node.tag == "em":
                    ref_model.journal = node.text
                    
                    # 非规范标题
                    # if ref_model.title == None:
                    #     # print(list(node.itersiblings()))
                    #     previous = node.getprevious()
                    #     if previous is not None:
                    #         previous = previous.getprevious()
                    #         if previous is not None and previous.tag == "br":
                    #             ref_model.title = previous.tail

                # journal page
                journal_page_liked = None
                if node_tail and self.JOURNAL_PAGE_COMPILER.search(node_tail):
                    journal_page_liked = node_tail.strip()
                elif node.text and self.JOURNAL_PAGE_COMPILER.search(node.text):
                    journal_page_liked = node.text.strip()
                if journal_page_liked:
                    ref_model.journal_page = journal_page_liked.lstrip(",， ").strip()
                
            ref_model.raw = "\r\n".join(content_list)
            # 引用列表    
            self.ref_list.append("\r\n".join(content_list))
            # 引用model列表
            self.ref_model_list.append(ref_model)

            # print(ref_model.raw)
            # print(ref_model)

        self.parse_successed = True


if __name__ == "__main__":
    import codecs
    path = "./test2.html"
    with codecs.open(path, "r") as file:    
        search = SearchDetailParser(file.read())
        search.parse()
        print(search.ref_model_list)
