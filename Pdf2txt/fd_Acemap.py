#!/usr/bin/env python
# coding=utf-8
 
import json
import requests
#import test_extra_word
from test_extra_word import extract_keys
from DataBaseConn import database_filtered_chinese
class findyou:
    def __init__(self):
        self.dic = {}
        self.person=[]
        self.personDict={}
        self.personChinese = []
        self.personDictChinese= {}
    def find_name_byKey(self,key):
        url = 'https://dev.acemap.info/api/v1/thucloud/find-experts-by-domain'
        #data_json = {'condition':'Transmission system'}
        data_json = {'condition':key}
        resp = requests.post(url,data_json)
        #print(type(resp))
        
        #json.loads(resp)
        #dic = dict(resp.text)
        self.dic=json.loads(resp.text)
        #print(dic['data']['resultForm'][0]['name'])
        #print(resp.text)
    def put_person_inList(self):
        for i in range(len(self.dic['data']['resultForm'])):
            name =self.dic['data']['resultForm'][i]['name'] #将寻找人名改为寻找id，这样可以提高数据库的检索效率
            fetch_id =self.dic['data']['resultForm'][i]['fetchId']#返回的id是字符串
            #if self.dic['data']['resultForm'][i]['name'] not in self.person:
            if fetch_id not in self.person:
                if fetch_id is not None:
                    self.person.append((fetch_id,name))
                    self.personDict[fetch_id] =1
            else:
                self.personDict[fetch_id]+=1
        for i in range(len(self.person)):
            if len(self.person[i][0]) == None:
                self.person.pop(i)
        #for per in self.person:
        #    print(per)

    def print_person(self):
        print('print_person________:')
        #for per in self.person:
        #    print(per)
        #print(self.personDict)
        test_data = sorted(self.personDict.items(),key = lambda x:x[1],reverse= True)
        print(test_data)

    def filter_left_chinese(self):
        print(self.person)
        self.personDictChinese=database_filtered_chinese(self.person)
        print("-----------------------------------------chinese people-----------------------------:")
        print(self.personDictChinese)
        #for idd in self.personDictChinese.keys():
            #print("idd=",idd)
            #print(self.personDict[idd[0]]) #这块我要打印什么？》
if __name__ == '__main__':
    extr = extract_keys()
    extr.Print()
    finding = findyou()
    for word in extr.keywords_en:
        finding.find_name_byKey(word)
        finding.put_person_inList()
    finding.print_person()
    finding.filter_left_chinese()
    #finding.find_name_byKey('Transmission system')












