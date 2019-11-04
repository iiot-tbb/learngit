#!/usr/bin/env python
# coding=utf-8
import threading


#class student(object):
#    def __init__(self,name):
#        self.name = name


#创建全局ThreadLocal对象：
local_school = threading.local()


def process_student():
    #获取当前线程关联的student：
    std = local_school.student
    print('Hello, %s(in %s)' %(std, threading.current_thread().name))


def process_thread(name):
    #绑定threadLocal的student
    local_school.student = name
    process_student()


t1 = threading.Thread(target = process_thread, args=('Alice',), name ='Thread-A')
t2 = threading.Thread(target = process_thread, args =('Bob', ), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
