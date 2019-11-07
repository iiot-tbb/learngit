#!/usr/bin/env python
# coding=utf-8
from nltk.text import TextCollection
import re
import jieba
import sys
def text(file):
    #改函数用来读取文件中的中文数据
    #改函数用来读取文件中的中文数据

    novel_data = open(file).read()
    cleaned_data = ''.join(re.findall(r'[\u4e00-\u9fa5]',novel_data))

    wordlist = jieba.lcut(cleaned_data)
    return cleaned_data


def text_wordlsit(file):                                                        
     #改函数用来读取文件中的中文数据                                    
     #改函数用来读取文件中的中文数据                                    
                                                                        
     novel_data = open(file).read()                                     
     cleaned_data = ''.join(re.findall(r'[\u4e00-\u9fa5]',novel_data))  
                                                                        
     wordlist = jieba.lcut(cleaned_data)                                
     return wordlist                                                

#不同种类的文本
text1= text(file='./text/new2.txt')
#text2 = text(file='./texts/caijing.txt')
#text3 = text(file = './texts/xinwen.txt')
#text4 = text(file = './texts/keji.txt')

#将文本列表初始化为TextCollection类
mytexts = TextCollection([text1])
dict_key = {}
#遍历wordllist，与 计算机类的名词尽心匹配，选出排在最前面的几个词

wordlist = text_wordlsit(sys.argv[1])

for wod in wordlist:
    if len(wod)<3:
        continue
    cfd = mytexts.tf(wod,text1)
    dict_key[wod]=cfd

listdic =sorted(dict_key.items(),key =lambda d: d[1],reverse=True)
print(listdic[:5])


#缺词库，貌似分词做的也不太好。
