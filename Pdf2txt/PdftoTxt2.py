#!/usr/bin/env python
# coding=utf-8
import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

def extract_text_by_page(pdf_path):
    with open(pdf_path,'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True, check_extractable=True):
            resource_manager =PDFResourceManager()#注册PDF资源管理器
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager,fake_file_handle)#转换器注册为文本转换器
            page_interpreter = PDFPageInterpreter(resource_manager, converter)#创建一个PDF解释器对象
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            #close open handles
            converter.close()
            fake_file_handle.close()

def extract_text(pdf_path):
    for page in extract_text_by_page(pdf_path):
        print(page)
        print()

if __name__ =='__main__':
    extract_text('tb.pdf')

