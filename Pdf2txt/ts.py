#!/usr/bin/env python
# coding=utf-8
seq = ['monday','tusday','wednesday','thursday','friday']
sep ="&&@@@@&&"
str1=sep.join(seq)
print(str1)

seq2=str1.split(sep)
print(seq2)
