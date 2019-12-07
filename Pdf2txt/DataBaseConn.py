#!/usr/bin/env python
# coding=utf-8
import pymysql
#创建数据库，创建连接对象conection
#连接对象作用是，连接数据库，发送数据库信息，处理回滚操作(查询中断时，数据库回到最初状态)，创建新的光标对象
import elasticsearch

def database_find_field_name(List_paperId):
    config = {
        'host':'202.120.36.29',
        'port':13306,
        'user':'readonly',
        'password':'readonly',
        'db':'am_paper',
    
    }
    
    #connection = pymysql.connect(host = '202.120.36.29',
    #                            user = 'readonly',
    #                            password ='readonly',
    #                            db = 'mysql',
    #                            port =13306)
    #
    connection = pymysql.connect(**config)
    #创建光标对象，一个连接可以有很多光标，一个光标跟踪一种数据状态。
    #光标对象做同事：、创建删除写入查询等等
    #cur = connection.cursor()
    ##查看有哪些数据库，通过cur。fetchall()获取查询所有结果
    #res =cur.fetchall()
    #print(res)
    try:
        with connection.cursor() as cursor:
            list_field_id = []
            list_field_name = []
            sql = "SELECT field_id FROM am_paper_field where paper_id = '%d' "
            sql2="SELECT name FROM am_field where field_id = '%d'"
            for paperid in List_paperId:
                cursor.execute(sql%paperid)
                #result = cursor.fetchone()#取一条数据
                for row in cursor.fetchall():
                    #print(type(row))
                    list_field_id.append(row[0])
    
                #print("37")
                #print(result)
                #print("39")
                #print(list_field_id)
            for filedId in list_field_id:
                cursor.execute(sql2%filedId)
                for row in cursor.fetchall():
                    list_field_name.append(row[0])
            
            print(list_field_name)
        connection.commit()
    
    finally:
        connection.close()
        return list_field_name


def database_filtered_chinese(list_raw):
    affil_id =[]
    author_contr ={}
    config = {
        'host':'202.120.36.29',
        'port':13306,
        'user':'readonly',
        'password':'readonly',
        'db':'am_paper',
    
    }
    connection = pymysql.connect(**config)
    #sql = "select author_id from am_author where name = '%s' or NormalizedName = '%s'"
    sql2 ="select last_known_affiliation_id,name from am_author where author_id ='%d'"
    sql3 = "select country_id from am_affiliation where affiliation_id = %d"
    
    try:
        with connection.cursor() as cursor:
            for name_id in list_raw:#list_raw的每一个元素为（author_id,author_name）元组
                cursor.execute(sql2%int(name_id[0]))
                for row in cursor.fetchall():
                    if row[0]!=0:
                        print(row[1])
                        affil_id.append((name_id,row[0]))
            #print(affil_id)
            for afiId in affil_id:
                cursor.execute(sql3%afiId[1])
                #print((sql3%afiId[1]))
                for row in cursor.fetchall():
                    if row[0]==2140066376 or row[0] ==2140082755 or row[0]==2140684314 or row[0]==2140705156 or row[0]==2140778575 :#中国，中国香港，中国台湾，中国澳门,新加坡
                    	author_contr[afiId[0]]=row[0]
                    #print(row)
        #print(author_contr)
        connection.commit()
    finally:
        connection.close()
        return author_contr  #返回包含key=author_id，value=countryid的字典
    

if __name__ =='__main__':
    #listp = [257993614,332168020,146298480,287619529,173977416]
    #li=database_find_filed_name(listp)

    list_author=[1000000310,1000000285,1000000378]
    database_filtered_chinese(list_author)

