#!/usr/bin/env python
# coding=utf-8


def bubbleSort(alist):
    for passnum in range(len(alist)-1,0,-1):
        for i in range(passnum):
            if alist[i]>alist[i+1]:
                alist[i],alist[i+1]=alist[i+1],alist[i]


def shortBubbleSort(alist):
    exchange = True
    passnum =len(alist)-1
    while passnum > 0 and exchange:
        exchange = False
        for i in range(passnum):
            if alist[i] >alist[i+1]:
                exchange = True
                alist[i],alist[i+1]=alist[i+1],alist[i]
        passnum = passnum -1 

alist = [54,26,93,17,77,31,44,55,20]
blist=alist[:]
bubbleSort(alist)
shortBubbleSort(blist)
print(alist)
print(blist)
