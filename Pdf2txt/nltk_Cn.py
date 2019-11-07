#!/usr/bin/env python
# coding=utf-8
from nltk.text import Text,ContextIndex
import re
import jieba
novel_data = open('./new3.txt').read()

#清除无关信息，只保留中文文本
cleaned_data = ''.join(re.findall(r'[\u4e00-\u9fa5]',novel_data))

wordlist = jieba.lcut(cleaned_data)
text =Text(wordlist)
print(type(wordlist))
print('-------------------')

text.concordance(word="青年",width=20,lines=10)
text.similar(word='研究',num=10)

Contextindex =ContextIndex(wordlist)

similarity_scores =Contextindex.word_similarity_dict(word='研究')

for key,value in similarity_scores.items():
    if value>0.02:
        print(key, value)



