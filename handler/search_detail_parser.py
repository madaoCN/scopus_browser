#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 13:15 AM
# @Author  : MADAO

from lxml import etree
from models.SearchListModel import SearchListModel


class SearchDetailParser(object):
    def __init__(self, html):
        super().__init__()
        # 当前解析的html
        self.html = html
        self.ref_list = []
        # 解析成功标志
        self.parse_successed = False

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

        for reference in reference_lists:
            node_list = []
            walk_tree(reference, node_list)
            content_list = []
            for node in node_list:
                if node.tag == 'a':
                    content_list.append("[{content}]({link})".format(content="".join(node.itertext()).strip(), link=node.get("href", "")))
                    continue
                if node.text:
                    text = node.text.strip()
                    if len(text):
                        content_list.append(text)
                node_tail = node.tail
                if node_tail and len(node_tail.strip()):
                    content_list.append(node_tail.strip())     
            self.ref_list.append("\r\n".join(content_list))
        self.parse_successed = True


if __name__ == "__main__":
    import codecs
    path = "./test2.html"
    with codecs.open(path, "r") as file:    
        search = SearchDetailParser(file.read())
        search.parse()
        print(search.ref_list)
