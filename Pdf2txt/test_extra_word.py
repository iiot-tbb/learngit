#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
from textrank4zh import TextRank4Keyword
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter,HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re 
import codecs
from jieba import analyse
import jieba
import sys
from enum import Enum,unique
from io import StringIO
from youdao import youdaoTranslate
import elasticsearch
from DataBaseConn import database_find_field_name
from DataBaseConn import database_filtered_chinese
class extract_keys:
    def __init__(self):
        self.text = ""
        self.keywords=[]
        self.keywords_en = []
        self.initial_tag = {'中文关键词':50,'中文关键字':50,'关键字':40,'关键词':40,'研究方向':500,
                            '项目名称':20,'研究意义':1500,'研究现状':1500,'中文摘要':-1500,'中\n文\n摘\n要':-1500}

    def print_txt(self):
        print(self.text)
    def convert_pdf_to_txt(self,path):
        rsrcmgr =PDFResourceManager()
        retstr = StringIO()
        codec ='utf-8'
        laparams =LAParams()
        device = TextConverter(rsrcmgr, retstr,laparams = laparams)
        fp =open(path,'rb')
        interpreter =PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching =True
        pagenos= set()
        for page in PDFPage.get_pages(fp,pagenos,maxpages=maxpages,password=password,caching=caching,check_extractable=True):
            interpreter.process_page(page)
        self.text = retstr.getvalue()
        
        fp.close()
        device.close()
        retstr.close()
    def convert_pdf_to_html(self,path):
        rsrcmgr =PDFResourceManager()
        retstr = StringIO()
        codec ='utf-8'
        laparams =LAParams()
        device = HTMLConverter(rsrcmgr, retstr,laparams = laparams)
        fp =open(path,'rb')
        interpreter =PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching =True
        pagenos= set()
        for page in PDFPage.get_pages(fp,pagenos,maxpages=maxpages,password=password,caching=caching,check_extractable=True):
            interpreter.process_page(page)
        self.text = retstr.getvalue()
        print(self.text)        
        fp.close()
        device.close()
        retstr.close()

    def text_processing(self):  #处理文本
        #print(''.join([s for s in text.splitlines(True) if s.strip()]))	 
        self.text=''.join([s for s in self.text.splitlines(True) if s.strip()]) #去除多余的空格和空行
        #lst =list(jieba.cut_for_search(self.text))
        lst=re.split(" |!|\?|\.|;|；",self.text)
        for i in lst:
            if len(i)<2:
                lst.remove(i)
            elif re.match(r'[a-zA-Z0-9]+',i):
                lst.remove(i)
        self.text=' '.join(lst)
        #text_half = int(len(self.text)/4)
        #print(self.text[:text_half])#.........................打印
        #    else:
        #        print(i)
    def text_processing_text(self):  #测试
        #print(''.join([s for s in text.splitlines(True) if s.strip()]))	 
        self.text=''.join([s for s in self.text.splitlines(True) if s.strip()]) #去除多余的空格和空行
        lst =list(jieba.cut(self.text))
        for i in lst:
            if len(i)<2:
                lst.remove(i)
            elif re.match(r'[a-zA-Z0-9]+',i):
                lst.remove(i)
        print(lst)
        self.text=' '.join(lst)
        
        #    else:
        #        print(i)
    def tf_idf(self,strs):#str是待用tf_idf 处理的字符串
        tfidf = analyse.extract_tags
        jieba.analyse.set_idf_path('./idf.txt.big.txt')
        lst =list(jieba.cut_for_search(strs))
        for i in lst:
            if len(i)<2:
                lst.remove(i)
            elif re.match(r'[a-zA-Z0-9]+',i):
                lst.remove(i)
        strs=' '.join(lst)
        keywords = tfidf(strs,allowPOS=('n','nr','ns'))
       # print("----tf_idf---------")
        for key in keywords:
           # print(key)
            if 2<len(key) <10:
                self.keywords.append(key)
    
    def find_tags(self):
        tag = False
        for (s,v) in self.initial_tag.items():
            #length_key =
           # self.keywords.append("....."+s+".....:")
            pos=self.text.find(s)
            if pos != -1:
                tag = True
                if v<0:
                    lentxt =pos
                    if pos > -v:
                        strtp = self.text[lentxt+v:lentxt]
                    else:
                        strtp = self.text[:lentxt]
                else:
                    lentxt = pos+len(s)
                    strtp = self.text[lentxt:lentxt+v]
                #if s is not '研究方向':
                if '关键' in s:
                    #lst=strtp.split("；")
                    lst=re.split(" |!|\?|\.|;|；",strtp)
                    self.keywords.extend(lst)
                elif '摘' in s:
                    #self.translate(strtp)#待完成
                    #self.extractFromDiscover()#待完成
                    #self.findInMysql()#待完成
                    translate_strtp = youdaoTranslate(strtp)
                    list_essay_id=self.find_essay_id_in_es(translate_strtp)
                    self.keywords_en.extend(self.find_filed_in_acemap_Database(list_essay_id))
                    #print(translate_strtp)
                    #print(list_essay_id)
                elif '项目名称' in s:
                    translate_strtp = youdaoTranslate(strtp)
                    list_essay_id=self.find_essay_id_in_es(translate_strtp,1)
                    self.keywords_en.extend(self.find_filed_in_acemap_Database(list_essay_id))
                else:
                    self.tf_idf(strtp)
                    self.Stupid_Textrank(strtp)
        if tag ==False:
            self.Stupid_Textrank(self.text)


    def print_keywords(self):
        #print('英文关键字：---------------')
        for i in range(len(self.keywords)):
            word=youdaoTranslate(self.keywords[i].strip(' \n'))
            if word =='CS' or word=='':
                #self.keywords.pop(i)
                pass
            else:
                self.keywords_en.append(word)
        #        print(word)
        #str_sep = "@"
        #str_key = str_sep.join(self.keywords)
        #str_after = youdaoTranslate(str_key)
        #self.keywords_en = str_after.split(str_sep)
        #for i in self.keywords_en:
        #    print(i)
        
        #print('中文关键字：----------------')
        #for i in self.keywords:
        #    print(i)
    def rec_as_keys(self): #识别出来关键字从
        new_keywords = []
        
        for i in self.keywords:
            if len(i)>=3:
                if i not in new_keywords:
                    new_keywords.append(i)
                #self.keywords.remove(i)
        self.keywords = new_keywords

        #停止词
    

    def Stupid_Textrank(self,strs):
        tr4w = TextRank4Keyword()
        tr4w.analyze(text = strs ,lower = True,window=2)
        for phrase in tr4w.get_keyphrases(keywords_num=10,min_occur_num =1):
            self.keywords.append(phrase)
   
    def find_essay_id_in_es(self,abstract,tag = 0):
        list_id = []
        es = elasticsearch.Elasticsearch("10.10.10.10:9200")
        if es.ping() != True:
            print("es.ping():",es.ping())
        query_json = {
            "query":{
                "match":{
                    "abstract":'\"' + abstract + '\"'
                }
            }
        }
        query_json2 = {
            "query":{
                "match":{
                    "title":'\"' + abstract + '\"'
                }
            }
        }
        if tag ==0:
            query = es.search(index = 'paper',filter_path=['hits.hits._id','hits.hits.field.name'],body=query_json,request_timeout=100) #index = 索引或别名
        elif tag == 1:
            query = es.search(index = 'paper',body=query_json2,filter_path=['hits.hits._id,hits.hits.field.name'],request_timeout=100) #index = 索引或别名
        for j in query['hits']['hits']:
            list_id.append(j["_id"])
            #print("\n\n\n\n\n\n\n-------------------------------------query-----------------------\n\n\n\n")
            #print(query)
        return list_id
    def find_filed_in_acemap_Database(self,paperId_list):
        fild_name = database_find_field_name(paperId_list)
        return fild_name
    def Print(self):
        self.convert_pdf_to_txt(sys.argv[1])
        self.text_processing()
        self.find_tags()
        self.rec_as_keys()
        self.print_keywords()


if __name__ == '__main__':
    #tfidf作为baseline
    #tfidf = analyse.extract_tags
    #keyw rds =tfidf(text)
    #for key in keywords:
    #    print(key)

    #f= StringIO(text)
    #while True:
    #    s = f.readline()
    #    if treat_as_keys()
    extr = extract_keys()
    #extr.convert_pdf_to_txt(sys.argv[1])
    ##extr.print_txt()
    #extr.text_processing()
    ##extr.text_processing_text()
    #extr.find_tags()
    #extr.rec_as_keys()
    #extr.print_keywords()
    extr.Print()


