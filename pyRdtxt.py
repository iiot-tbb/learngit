#!/usr/bin/env python
# coding=utf-8



#read txt method one

#f = open("./new3.txt")
#line =f.readline()
#while line:
#    print(line)
#    line =f.readline()
#
#f.close()


#read txt method two
#f = open("./new3.txt")
#for line2 in open("./new3.txt","r"):
#    print(line2)


#read txt method three

f2 =open("./new2.txt","r")
lines =f2.readlines()
for line3 in lines:
    print(line3)
