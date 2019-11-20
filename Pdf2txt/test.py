#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function                                                             
from textrank4zh import TextRank4Keyword
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re 
import codecs
from jieba import analyse
import jieba
import sys
from enum import Enum,unique
from io import StringIO

st = "关键字是什么随着软件行业的发展，软件的规模越来越大，传统的人工代码审查和单元测试已无法100%\
地保证程序的正确性。同时，随着越来越多的行业开始深入使用软件技术，对于软件可靠性进\
行监管的需求也越来越高。而程序正确性证明/检验技术正是保障程序正确性并对第三方自证\
程序正确性的重要手段。\
稿\
本项目关注并发程序的正确性证明以及其理论\
"

def tf_idf(strs):#str是待用tf_idf 处理的字符串
    tfidf = analyse.extract_tags
    keywords = tfidf(strs)
    for key in keywords:
        print(key)
tf_idf(st)
