#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from textrank4zh import TextRank4Keyword,TextRank4Sentence
import codecs
import sys
def convert_pdf_to_txt(path):
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

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


#


def Text_extract_Key(text):
    #text = codecs.open(sys.argv[1],'r',utf-8).read()
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text,lower = True,window=2)

    print('关键词: ')
    for item in tr4w.get_keywords(20,word_min_len=2):
        print(item.word,item.weight)

    print('------------')
    print('关键短语:')
    for phrase in tr4w.get_keyphrases(keywords_num=20,min_occur_num = 2):
        print(phrase)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text = text, lower = True, source ='all_filters')

    print('-----------')
    print('摘要：')
    for item in tr4s.get_key_sentences(num=3):
        print(item.index,item.weight,item.sentence)

if __name__ =='__main__':
    #fd = open(sys.argv[1],'w') #第一个参数是生成的文件名
    #fd.write(convert_pdf_to_txt(sys.argv[2]))#第二个参数是是打开PDF文件，
    #fd.close()
    text = convert_pdf_to_txt(sys.argv[1])
    Text_extract_Key(text)
