#!/usr/bin/env python
# coding=utf-8
 
import json
import requests
#import test_extra_word
from test_extra_word import extract_keys
class findyou:
    def __init__(self):
        self.dic = {}
        self.person=[]

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
            name =self.dic['data']['resultForm'][i]['name']
            if self.dic['data']['resultForm'][i]['name'] not in self.person:
                if name is not None:
                    self.person.append(name)
        for i in range(len(self.person)):
            if len(self.person[i]) == 0:
                self.person.pop(i)
        #for per in self.person:
        #    print(per)
    def print_person(self):
        for per in self.person:
            print(per)
if __name__ == '__main__':
    extr = extract_keys()
    extr.Print()
    finding = findyou()
    for word in extr.keywords_en:
        finding.find_name_byKey(word)
        finding.put_person_inList()
    finding.print_person()
    #finding.find_name_byKey('Transmission system')












