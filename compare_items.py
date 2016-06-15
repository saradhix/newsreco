#from __future__ import print_function
import sys
import pymongo
import itertools
import json

import mylib


items_to_read = 1000
top_matches_count = 1000

min_similarity = 0.2
max_similarity = 0.8

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles

docs = coll.find().limit(items_to_read)
doclist=[]
documents=[]
for doc in docs:
  documents.append([doc['description'], doc['discoverTime'], doc['title']])
  nouns_and_verbs = mylib.get_nouns_and_verbs(doc['description'])
  doclist.append(nouns_and_verbs)


print len(doclist)
similarity_matrix=[]
for i in range(len(doclist)):
  for j in range(i+1,len(doclist)):
    a = doclist[i]
    b = doclist[j]
    similarity = mylib.jaccard_similarity(a,b)
    if similarity >= min_similarity and similarity <= max_similarity:
      row = (i, j, similarity)
      similarity_matrix.append(row)

#Now we have a list of rows, which are to be sorted on similarity which is 3rd
#element in the tuple

top_similar = sorted(similarity_matrix, key = lambda x:x[2], reverse=True)[0:top_matches_count]
print top_similar

print "Printing pairs"
for item in top_similar:
  print "Similarity=", item[2]
  doc1 = documents[item[0]]
  doc2 = documents[item[1]]
  print "Document 1"
  print doc1
  print "*"*40
  print "Document 2"
  print doc2
  print "-"*40
  print "Common nouns and verbs"
  print set(doclist[item[0]]) & set(doclist[item[1]])
  bigrams1 = mylib.make_bigrams(doc1[0])
  bigrams2 = mylib.make_bigrams(doc2[0])
  js_bigram_similarity = mylib.jaccard_similarity(bigrams1, bigrams2)
  print "JS_bigram=", js_bigram_similarity
  print "Time difference=", (int(doc1[1])-int(doc2[1]))
  print set(bigrams1) & set(bigrams2)
  print "=="*40
  print "=="*40
  print ""



