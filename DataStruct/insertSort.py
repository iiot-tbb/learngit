#!/usr/bin/env python
# coding=utf-8

def insertionSort(alist):
    for index in range(1,len(alist)):

        currentvalue = alist[index]
        postition = index

        while postition>0 and alist[postition-1] >currentvalue:
            alist[postition] =alist[postition-1]
            postition = postition -1

        alist[postition] = currentvalue

if __name__ =='__main__':
    alist = [54,26,65,76,83,45,87,32,56,76]
    insertionSort(alist)
    print(alist)
