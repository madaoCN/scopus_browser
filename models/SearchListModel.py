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
        
        self.ref_list = []
        self.ref_model_list = []

    def __repr__(self):
        return ''' ========\r\n doi: {doi}\r\n title: {title}\r\n titlelink: {titlelink}\r\n author: {author}\r\n year: {year}\r\n journal: {journal}\r\n journal_no: {journal_no}\r\n journal_link: {journal_link}\r\n ========\r\n'''.format(
                doi = self.doi,
                title = self.title,
                titlelink = self.title_link,
                author = self.author if self.author else [],
                year = self.year,
                journal = self.journal,
                journal_no = self.journal_no,
                journal_link = self.journal_link
            )