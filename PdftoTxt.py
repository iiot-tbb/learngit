#!/usr/bin/env python
# coding=utf-8
import io
import sys
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle =io.StringIO()
    converter = TextConverter(resource_manager,fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path,'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                     caching = True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            

        text =fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text

if __name__ == '__main__':
    f=open(sys.argv[1],'w')
    tes=extract_text_from_pdf(sys.argv[2])
    f.write(tes)
    f.close()
   # print(extract_text_from_pdf('tb.pdf'))
