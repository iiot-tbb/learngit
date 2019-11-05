#!/usr/bin/env python
# coding=utf-8

def selectionSort(alist):
    for fillslot in range(len(alist)-1,0,-1):
        postionOfMax =0
        for location in range(1, fillslot+1):
            if alist[location]>alist[postionOfMax]:
                postionOfMax =location

        alist[postionOfMax],alist[fillslot]=alist[fillslot],alist[postionOfMax]


def selectionSort2(alist):
    for seq in range(len(alist)-1,0, -1):
        postionOfMax =0
        for locate in range(1,seq+1):
            if alist[postionOfMax]<alist[locate]:
                postionOfMax =locate

        alist[postionOfMax],alist[locate]=alist[locate],alist[postionOfMax]



if __name__ =='__main__':
    alist =[54,26,39,17,77,56,54,34,87]
    selectionSort2(alist)
    print(alist)
