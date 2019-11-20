#!/usr/bin/env python
# coding=utf-8
import urllib.parse
import http.client
import random
import hashlib
 
appKey = '49ff79007daed96a'
secretKey = 'X4E7RWzpr984bHJA0PRd1GX18UoDXET7'
 
def youdaoTranslate(q):
    if q == None or q == ' ' or q =='\n':
        return ''
    httpClient = None
    s =[]
    myurl = '/api'
    fromLang = 'zh-CHS'
    toLang = 'EN'
    salt = random.randint(1, 65536)
    sign = appKey+q+str(salt)+secretKey
    m1 = hashlib.new('md5')
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl+'?appKey='+appKey+'&q='+ urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    try:
        httpClient = http.client.HTTPConnection('openapi.youdao.com')
        httpClient.request('GET', myurl)
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        s = eval(response.read().decode("utf-8"))['translation']
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
    if len(s) != 0:
        ss = s[0]
        return ss
    return "CS"
 
if __name__ == '__main__':
    ss = youdaoTranslate('智能@@火车#汽车')
    print(type(ss))
    print(ss)
