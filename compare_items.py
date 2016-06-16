#from __future__ import print_function
import sys
import pymongo
import itertools
import json

import mylib


items_to_read = 5000
top_matches_count = 1000

min_similarity = 0.2
max_similarity = 0.8

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles

docs = coll.find().limit(items_to_read)
doclist=[]
documents=[]
print "Items to read=", items_to_read
cx = 0
for doc in docs:
  documents.append([doc['description'], doc['discoverTime'], doc['title']])
  nouns_and_verbs = mylib.get_nouns_and_verbs(doc['description'])
  doclist.append(nouns_and_verbs)
  cx = cx + 1
  if cx % 100 == 0:
    print cx, "documents processed"


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
print len(top_similar)
print top_similar

print "Printing pairs"
for item in top_similar:
  print "Similarity=", item[2]
  doc1 = documents[item[0]]
  doc2 = documents[item[1]]
  if int(doc1[1]) > int(doc2[1]):
    (doc1,doc2) = (doc2,doc1)
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
  trigrams1 = mylib.make_trigrams(doc1[0])
  trigrams2 = mylib.make_trigrams(doc2[0])
  js_bigram_similarity = mylib.jaccard_similarity(bigrams1, bigrams2)
  js_trigram_similarity = mylib.jaccard_similarity(trigrams1, trigrams2)
  if js_trigram_similarity == 0.0:
    bg_tg_ratio = "INFINITE"
  else:
    bg_tg_ratio = js_bigram_similarity/float(js_trigram_similarity)
  print ""
  print "JS_bigram=", js_bigram_similarity,"JS_trigram=", js_trigram_similarity
  print "BGTG ratio =", bg_tg_ratio
  print "Time difference=", abs(int(doc1[1])-int(doc2[1]))/float(3600000), "t1=", doc1[1], "t2=",doc2[1]
  print set(bigrams1) & set(bigrams2)
  print "Common trigrams"
  print set(trigrams1) & set(trigrams2)
  print "=="*40
  print "=="*40
  print ""



