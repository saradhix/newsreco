#from __future__ import print_function
import sys
import pymongo
import itertools
import json

import mylib


items_to_read = 30
top_matches_count = 100

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles

docs = coll.find().limit(items_to_read)
doclist=[]
documents=[]
for doc in docs:
  documents.append(doc)
  nouns_and_verbs = mylib.get_nouns_and_verbs(doc['description'])
  doclist.append(nouns_and_verbs)


print len(doclist)
similarity_matrix=[]
for i in range(len(doclist)):
  for j in range(i+1,len(doclist)):
    a = doclist[i]
    b = doclist[j]
    similarity = mylib.jaccard_similarity(a,b)
    row = (i, j, similarity)
    similarity_matrix.append(row)

#Now we have a list of rows, which are to be sorted on similarity which is 3rd
#element in the tuple

top_similar = sorted(similarity_matrix, key = lambda x:x[2], reverse=True)[0:top_matches_count]
print top_similar

print "Printing pairs"
for item in top_similar:
  print "Similarity=", item[2]
  print ((documents[item[0]]))
  print (json.loads(documents[item[0]]))
  print json.dumps(json.loads(documents[item[0]]))
  print "*"*40
  print json.dumps(json.loads(documents[item[1]]))
  print "-"*40
  print set(doclist[item[0]]) & set(doclist[item[1]])
  print "=="*40



