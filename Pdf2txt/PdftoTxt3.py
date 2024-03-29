#!/usr/bin/env python
# coding=utf-8
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
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


if __name__ =='__main__':
    fd = open(sys.argv[1],'w') #第一个参数是生成的文件名
    fd.write(convert_pdf_to_txt(sys.argv[2]))#第二个参数是是打开PDF文件，
    fd.close()
