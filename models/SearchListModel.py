#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 13:15 AM
# @Author  : MADAO

class SearchListModel(object):

    def __init__(self):
        super().__init__()

        self.doi = None
        self.title = None
        self.title_link = None
        # tuple
        self.author = None
        self.year = None
        self.journal = None
        self.journal_no = None
        self.journal_link = None 

        # 参考文献数量
        self.ref_count = 0
        # 期刊信息
        self.journal_info = None
        # 摘要
        self.abstract = None
        # 作者关键字
        self.author_keywords = None
        # issn
        self.issn = None
        # 原始语言
        self.raw_lang = None
        # 来源出版物类型
        self.src_journal_type = None
        # 文献类型
        self.document_type = None
        # 出版商
        self.publisher = None
        
        self.ref_list = []
        self.ref_model_list = []

    def __repr__(self):
        var_str = " ========\r\n "
        for name,value in vars(self).items():
            var_str += "{key}: {value}\r\n".format(key=name, value=value)
        var_str += " ========\r\n "
        return var_str