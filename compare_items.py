#from __future__ import print_function
import sys
import pymongo
import itertools
import json

import mylib

news_file = 'newsarticles.txt'

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles

docs = coll.find().limit(10)
doclist=[]
for doc in docs:
  print doc['description']
  doclist.append(doc['description'])


print len(doclist)
for a in doclist:
  for b in doclist:
    similarity = mylib.similarity(a,b)
    print similarity
