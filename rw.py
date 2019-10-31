#!/usr/bin/env python
# coding=utf-8
try:
    f =open('/home/tbb/for.py','r')
   # print(f.read())
    for line in f.readlines():
        print(line.strip())
finally:
    if f:
        f.close()

