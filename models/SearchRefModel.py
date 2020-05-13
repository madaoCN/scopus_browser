#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 13:15 AM
# @Author  : MADAO

class SearchRefModel(object):

    def __init__(self):
        super().__init__()
        self.raw = None
        self.doi = None
        self.title = None
        self.title_link = None 
        self.author = None
        self.year = None
        self.journal = None
        self.journal_page = None
        self.ref_link = None 

    def __repr__(self):
        return ''' ========\r\n doi: {doi}\r\n title: {title}\r\n title_link: {title_link}\r\n author: {author}\r\n year: {year}\r\n journal: {journal}\r\n journal_page: {journal_page}\r\n ref_link: {ref_link}\r\n ========\r\n'''.format(
                doi = self.doi,
                title = self.title,
                title_link = self.title_link,
                author = self.author,
                year = self.year,
                journal = self.journal,
                journal_page = self.journal_page,
                ref_link = self.ref_link
                )