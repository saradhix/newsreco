#from __future__ import print_function
import sys
import pymongo
import itertools
import json

import mylib

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles

docs = coll.find().limit(1000)
doclist=[]
documents=[]
for doc in docs:
  documents.append(doc['description'])
  nouns_and_verbs = mylib.get_nouns_and_verbs(doc['description'])
  doclist.append(nouns_and_verbs)


print len(doclist)
max_similarity = 0
maxa=doclist[0]
maxb=doclist[0]
for i in range(len(doclist)):
  for j in range(i+1,len(doclist)):
    a = doclist[i]
    b = doclist[j]
    similarity = mylib.jaccard_similarity(a,b)
    if similarity > max_similarity:
      max_similarity = similarity
      maxa = a
      maxb = b
      idxa = i
      idxb = j
#    print similarity
print max_similarity
print "-"*60
print sorted(maxa)
print "-"*30
print sorted(maxb)
print "-"*30
print sorted(set(maxa) & set(maxb))

print "-"*30
print "Printing articles"
print documents[idxa]
print "-"*30
print documents[idxb]


