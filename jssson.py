#!/usr/bin/env python
# coding=utf-8
import json

def student2dict(std):
    return {
        'name':std.name,
        'age':std.age,
        'score':std.score
    }

def dict2student(d):
    return Student(d['name'],d['age'],d['score'])

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s= Student('tbb',24,100)
print(json.dumps(s, default= student2dict))
json_str='{"age":20,"score":88,"name":"Bob"}'
print(json.loads(json_str,object_hook=dict2student))



def Tb2dict(std):
    return{
        "name":std.name,
        "age":std.age,
        "height":std.height
    }

def dict2Tb(d):
    return Tb(d['name'],d['age'],d['height'])

class Tb(object):
    def __init__(self,name,age,height):
        self.name = name
        self.age= age
        self.height=height

t=Tb("tb",24,177)
js = json.dumps(t,default=Tb2dict)
print(js)

t2 = json.loads(js,object_hook = dict2Tb)
print(t2)

