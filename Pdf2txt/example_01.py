#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword,TextRank4Sentence

text =codecs.open('./new3.txt','r','utf-8').read()
tr4w = TextRank4Keyword()

tr4w.analyze(text=text, lower= True,window=2)

print('关键词： ')
for item in tr4w.get_keywords(20,word_min_len=2):
    print(item.word,item.weight)

print()
print("关键短语:")
for phrase in tr4w.get_keyphrases(keywords_num=20,min_occur_num = 2):
    print(phrase)

tr4s = TextRank4Sentence()
tr4s.analyze(text=text, lower= True,source = 'all_filters')

print()
print('摘要：')
for item in tr4s.get_key_sentences(num=3):
    print(item.index,item.weight,item.sentence)
