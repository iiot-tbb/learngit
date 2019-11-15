#!/usr/bin/env python
# coding=utf-8

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



class extract_keys:
    def __init__(self):
        self.text = ""
        self.keywords=[]
        self.initial_tag = {'中文关键词':50,'中文关键字':40,'关键字':20,'研究方向':300,
                            '项目名称':20}

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

    def text_processing(self):  #处理文本
        #print(''.join([s for s in text.splitlines(True) if s.strip()]))	 
        self.text=''.join([s for s in self.text.splitlines(True) if s.strip()]) #去除多余的空格和空行
        lst =list(jieba.cut_for_search(self.text))
        for i in lst:
            if len(i)<2:
                lst.remove(i)
            elif re.match(r'[a-zA-Z0-9]+',i):
                lst.remove(i)
        self.text=' '.join(lst)
        #    else:
        #        print(i)
    def find_tags(self):
        tag = False
        for (s,v) in self.initial_tag.items():
            #length_key =
            pos=self.text.find(s)
            if pos != -1:
                tag = True
                lentxt = pos+len(s)
                strtp = self.text[lentxt:lentxt+v]
                if s is not '研究方向':
                    #lst=strtp.split("；")
                    lst=re.split(" |!|\?|\.|;|；",strtp)
                    self.keywords.extend(lst)
                else:
                    tf_idf(strtp)
        if tag =False:
            Stupid_Textrank(self.text)


    def print_keywords(self):
        print('关键字：')
        for i in self.keywords:
            print(i)

    def rec_as_keys(self): #识别出来关键字从
        for i in self.keywords:
            if len(i)<3:
                self.keywords.remove(i)
    
    def tf_idf(self,strs):#str是待用tf_idf 处理的字符串
        tfidf = analyse.extract_tags
        keywords = tfidf(text)
        for key in keywords:
            if 2<len(key) <10:
                self.keywords.append(key)
    

    def Stupid_Textrank(self):
        tr4w = TextRank4Keyword()
        tr4w.analyse(text = self.text ,lower = True,window=2)
        for phrase in tr4w.get_keyphrases(keywords=10,min_occur_num =1):
            self.keywords.append(phrase)


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
    extr.convert_pdf_to_txt(sys.argv[1])
    #extr.print_txt()
    extr.text_processing()
    extr.find_tags()
    extr.rec_as_keys()
    extr.print_keywords()



