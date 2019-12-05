#!/usr/bin/env python
# coding=utf-8
import elasticsearch
es = elasticsearch.Elasticsearch("10.10.10.10:9200")
if es.ping() != True:
    print("es.ping():",es.ping())
abstract = "The objective of this research was to accelerate crystallization of the trans-free unhydrogenated palm oil-based shortening. Crystallization thermograms of the unhydrogenated palm oil-based shortening were measured by differential scanning calorimetry(DSC) to-10 ℃ at the rate of 5 ℃ /min, in the presence of blended with different ratios of icing sugar(1 ∶ 0.5, 1 ∶ 1.0, 1 ∶ 1.5 and 1 ∶ 2.0) or from different initial heating temperatures(30, 35, 40, 42, 45, 50, 60, 70 ℃ and 80 ℃). The crystallization properties of unsaturated and partially hydrogenated palm oil-based shortening were also compared. Sugar acted as a catalyst and helped to overcome the free energy barrier by forming the heterogeneous nucleus. Crystallization rates from temperatures above the melting point were faster than those below the top limit of the melting point. The reason might be that a higher initial heating temperature induced a completely melted state and thus a larger driving force toward the solid phase."
print(abstract)
query_json = {
   "query" : {
        "match" : {
            "title" : '\"'+abstract+'\"'
        }
    }
}
query = es.search(index='paper',body=query_json,request_timeout=100) # index = 索引或别名

for j in query['hits']['hits']:
    print ( j["_id"])
    #print(j["_source"]["abstract"])
