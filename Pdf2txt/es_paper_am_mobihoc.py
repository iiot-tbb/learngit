#!/usr/bin/env python
# coding: utf-8

# # 创建index
import elasticsearch
import json

es = elasticsearch.Elasticsearch("10.10.10.10:9200")
print("es.ping(): ",es.ping())


mapping = {
    # "aliases": {
    #     "paper": {}
    # },
    "mappings": {
        "dynamic_templates": [
            {
                "strings": {
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "text",
                        "analyzer": "text_analyzer"
                    }
                }
            }
        ],
        "properties": {
            "abstract": {
                "type": "text",
                "analyzer": "text_analyzer",
                "copy_to": [
                    "all"
                ]
            },
            "affiliation": {
                "properties": {
                    "abbr": {
                        "type": "text",
                        "analyzer": "text_no_stemmer",
                        "copy_to": [
                            "all"
                        ]
                    },
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "text_no_stemmer",
                        "copy_to": [
                            "all"
                        ]
                    }
                }
            },
            "all": {
                "type": "text",
                "analyzer": "text_analyzer"
            },
            "analysis": {
                "properties": {
                    "citation_count": {
                        "type": "integer"
                    },
                    "reference_count": {
                        "type": "integer"
                    },
                    "score": {
                        "type": "integer"
                    }
                }
            },
            "author": {
                "properties": {
                    "aff_index": {
                        "type": "short",
                        "index": False
                    },
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "text_no_stemmer",
                        "copy_to": [
                            "all"
                        ]
                    }
                }
            },
            "first_author": {
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "text_no_stemmer"
                    }
                }
            },
            "conference_intance": {
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "text_no_stemmer",
                        "copy_to": [
                            "all"
                        ]
                    }
                }
            },
            "conference_series": {
                "properties": {
                    "abbr": {
                        "type": "text",
                        "analyzer": "text_no_stemmer",
                        "copy_to": [
                            "all"
                        ]
                    },
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "text_analyzer",
                        "copy_to": [
                            "all"
                        ]
                    }
                }
            },
            "doc_type": {
                "type": "byte"
            },
            "field": {
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "text_analyzer",
                        "copy_to": [
                            "all"
                        ]
                    }
                }
            },
            "first_page": {
                "type": "integer",
                "index": False
            },
            "issue": {
                "type": "integer",
                "index": False
            },
            "journal": {
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "text_analyzer",
                        "copy_to": [
                            "all"
                        ]
                    }
                }
            },
            "last_page": {
                "type": "integer",
                "index": False
            },
            "machine_reading": {
                "type": "object"
            },
            "title": {
                "type": "text",
                "analyzer": "text_analyzer",
                "copy_to": [
                    "all"
                ]
            },
            "volume": {
                "type": "integer",
                "index": False
            },
            "year": {
                "type": "short"
            }
        }
    },
    "settings": {
        "index": {
            "number_of_shards": "16",
            "number_of_replicas": "0"
        },
        "analysis": {
            "filter": {
                "eng_stemmer": {
                    "type": "stemmer",
                    "name": "english"
                },
                "eng_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                }
            },
            "analyzer": {
                "text_analyzer": {
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding", "eng_stemmer", "eng_stop"]
                },
                "text_no_stemmer": {
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding"]
                }
            }
        }
    }
}

# 添加别名
# curl -XPOST '10.10.10.10::9200/_aliases' -d 
# {
#     "actions": [
#         {"add": {"index": "", "alias": ""}}
#     ]
# }


es.indices.create(index='am_mobihoc', body=mapping)

import time
import MySQLdb
import MySQLdb.cursors
import elasticsearch.helpers
import json
import multiprocessing as mp
from tqdm import tqdm_notebook as tqdm
import sys





db = MySQLdb.connect('10.10.10.10', 'readonly', 'readonly', 'am_paper', charset='utf8mb4', cursorclass=MySQLdb.cursors.SSCursor)
cursor = db.cursor()



# Author ID to name.
sql = 'SELECT author_id, name FROM am_author;'
cursor.execute(sql)
author_id2name = {aid: name for aid, name in cursor}
# for aid, name in tqdm(cursor):
#     author_id2name[aid] = name


# Affiliation ID to name and abbr.
sql = 'SELECT affiliation_id, name, abbreviation FROM am_affiliation;'
cursor.execute(sql)
aff_id2name = {0: ''}
aff_id2abbr = {0: ''}
for aid, name, abbr in cursor:
    aff_id2name[aid] = name
    aff_id2abbr[aid] = abbr
print("len(aff_id2name):",len(aff_id2name))


# Conference instance ID to name.
sql = 'SELECT conference_instance_id, name FROM am_conference_instance;'
cursor.execute(sql)
conf_instance_id2name = {cid: name for cid, name in cursor}
conf_instance_id2name[0] = ''
print("len(conf_instance_id2name):",len(conf_instance_id2name))


# Conference series ID to name and abbr.
sql = 'SELECT conference_series_id, name, abbreviation FROM am_conference_series;'
cursor.execute(sql)
conf_id2name = {0: ''}
conf_id2abbr = {0: ''}
for cid, name, abbr in cursor:
    conf_id2name[cid] = name
    conf_id2abbr[cid] = abbr
print("len(conf_id2name):",len(conf_id2name))


# Journal ID to name.
sql = 'SELECT journal_id, name FROM am_journal;'
cursor.execute(sql)
journal_id2name = {jid: name for jid, name in cursor}
journal_id2name[0] = ''
print("len(journal_id2name):",len(journal_id2name))



# Field ID to name
sql = 'SELECT field_id, name FROM am_field;'
cursor.execute(sql)
field_id2name = {fid: name for fid, name in cursor}
print("len(field_id2name):",len(field_id2name))


# Get papers' authors and affiliations where id in [begin, end).
def get_paper_author(param):
    try:
        db = MySQLdb.connect('10.10.10.10', 'readonly', 'readonly', 'am_paper', charset='utf8mb4', cursorclass=MySQLdb.cursors.SSCursor)
        cursor = db.cursor()
        sql = """SELECT paper_id, sequence, author_id, affiliation_id FROM am_paper_author 
        WHERE paper_id in (%s);""" % (",".join(str(i) for i in param))
        cursor.execute(sql)
        info = sorted(cursor)
        paper_author = {}
        paper_aff = {}
        paper_aff_index = {}
        paper_first_author = {}
        for pid, seq, auid, afid in info:
            if seq == 1:
                paper_first_author[pid] = auid
            if pid not in paper_author:
                paper_author[pid] = []
                paper_aff[pid] = []
                paper_aff_index[pid] = []
            if auid not in paper_author[pid]:
                paper_author[pid].append(auid)
                paper_aff_index[pid].append([])
            if afid:
                if afid not in paper_aff[pid]:
                    paper_aff[pid].append(afid)
                paper_aff_index[pid][paper_author[pid].index(auid)].append(paper_aff[pid].index(afid))
        return paper_author, paper_aff, paper_aff_index, paper_first_author
    finally:
        cursor.close()
        db.close()



# Get papers' fields where id in [begin, end).
def get_paper_field(param):
    try:
        db = MySQLdb.connect('10.10.10.10', 'readonly', 'readonly', 'am_paper', charset='utf8mb4', cursorclass=MySQLdb.cursors.SSCursor)
        cursor = db.cursor()
        sql = """SELECT paper_id, field_id FROM am_paper_field
        WHERE paper_id in (%s);""" % (",".join(str(i) for i in param))
        cursor.execute(sql)
        paper_field = {}
        for pid, field in cursor:
            paper_field.setdefault(pid, []).append(field)
        return paper_field
    finally:
        cursor.close()
        db.close()


# Get papers' info where id in (pid,pid,pid).
def get_paper_info(param):
    try:
        tt = ",".join(str(i) for i in param)
        db = MySQLdb.connect('10.10.10.10', 'readonly', 'readonly', 'am_paper', charset='utf8mb4', cursorclass=MySQLdb.cursors.SSCursor)
        cursor = db.cursor()
        sql = """SELECT paper_id, title, year, doc_type, journal_id, conference_series_id, 
        conference_instance_id, volume, issue, first_page, last_page 
        FROM am_paper WHERE paper_id in (%s);""" % (tt)
        cursor.execute(sql)
        paper_info = list(cursor)
        
        sql = """SELECT paper_id, abstract FROM am_paper_abstract WHERE paper_id in (%s);""" % (tt)
        cursor.execute(sql)
        paper_abstract = {pid: abst for pid, abst in cursor}
        
        sql = """SELECT paper_id, score, reference_count, citation_count 
        FROM am_analysis.am_paper_analysis WHERE paper_id in (%s);""" % (tt)
        cursor.execute(sql)
        paper_analysis = {i[0]: i[1:] for i in cursor}
        
        sql = """SELECT  paper_id,machine_reading FROM am_analysis.am_paper_abstract_analysis WHERE paper_id in (%s);""" % (tt)
        cursor.execute(sql)
        paper_abstract_analysis = {i[0]: i[1] for i in cursor}
        
        return paper_info, paper_abstract, paper_analysis, paper_abstract_analysis
    finally:
        cursor.close()
        db.close()



def gen_doc(param):
    paper_info, paper_abstract, paper_analysis,paper_abstract_analysis = get_paper_info(param)
    paper_field = get_paper_field(param)
    paper_author, paper_aff, paper_aff_index, paper_first_author = get_paper_author(param)
    for line in paper_info:
        pid, title, year, doc_type, jid, csid, ciid, vol, iss, first_page, last_page= line
        abst = paper_abstract.get(pid, '')
        score, ref_cnt, cit_cnt = paper_analysis.get(pid, (0, 0, 0))
        mr = paper_abstract_analysis.get(pid, None)
        yield {
            '_index': 'am_mobihoc',
            '_id': pid,
            '_source': {
                'title': title,
                'year': year,
                'journal': {
                    'id': jid,
                    'name': journal_id2name[jid]
                },
                'conference_series': {
                    'id': csid,
                    'name': conf_id2name[csid],
                    'abbr': conf_id2abbr[csid]
                },
                'conference_intance': {
                    'id': ciid,
                    'name': conf_instance_id2name[ciid]
                },
                'doc_type': doc_type,
                'volume': vol,
                'issue': iss,
                'first_page': first_page,
                'last_page': last_page,
                'abstract': abst,
                'field': {
                    'id': paper_field.get(pid, []),
                    'name': [field_id2name[fid] for fid in paper_field.get(pid, [])]
                },
                'analysis': {
                    'score': score,
                    'reference_count': ref_cnt,
                    'citation_count': cit_cnt
                },
                'author': {
                    'id': paper_author.get(pid, []),
                    'name': [author_id2name[auid] for auid in paper_author.get(pid, [])],
                    'aff_index': paper_aff_index.get(pid, [])
                },
                'first_author': {
                    'id': paper_first_author.get(pid, 0),
                    'name': author_id2name[paper_first_author[pid]] if pid in paper_first_author else ''
                },
                'affiliation': {
                    'id': paper_aff.get(pid, []),
                    'name': [aff_id2name[afid] for afid in paper_aff.get(pid, [])],
                    'abbr': [aff_id2abbr[afid] for afid in paper_aff.get(pid, [])]
                },
                'machine_reading': json.loads(mr or '{}')
            }
        }


def update_to_es(param,host):
    es = elasticsearch.Elasticsearch(host)
    print(time.ctime(), "start!")
    sys.stdout.flush()
    docs = list(gen_doc(param))
    print("len(docs):",len(docs))
    print(docs[:1])
    for i in range(10):
        try:
            for success, info in elasticsearch.helpers.streaming_bulk(es, docs, chunk_size=1000, max_chunk_bytes=524288000, raise_on_exception=False, max_retries=5):
                if not success:
                    print('A document failed:', info)
            return
        except Exception as e:
            print('ERROR FOR PARAM:', param, i)
            sys.stdout.flush()




if __name__ == '__main__':
	pids = set()
	with open("mobihoc_paper_id.txt") as fp:
	    for line in fp:
	        pids.add(int(line))

	print(len(pids))

	host = '10.10.10.10:9200'
	update_to_es(pids,host)




