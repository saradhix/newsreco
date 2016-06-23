#from __future__ import print_function
import sys
import pymongo
import itertools
import json
import time

import mylib


items_to_read = 10000
top_matches_count = 2000

min_similarity = 0.2
max_similarity = 0.8

t1 = time.time()
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
  nouns_and_verbs = doc['nv']
  doclist.append(nouns_and_verbs)
  cx = cx + 1
  if cx % 100 == 0:
    print cx, "documents processed"

print "Calculating similarity for documents", len(doclist)
similarity_matrix=[]
cx = 0
for i in range(len(doclist)):
  for j in range(i+1,len(doclist)):
    a = doclist[i]
    b = doclist[j]
    similarity = mylib.jaccard_similarity(a,b)
    if similarity >= min_similarity and similarity <= max_similarity:
      row = (i, j, similarity)
      similarity_matrix.append(row)
    cx = cx + 1
    if cx % 100000 == 0:
      print cx, "pairs computed "

#Now we have a list of rows, which are to be sorted on similarity which is 3rd
#element in the tuple

top_similar = sorted(similarity_matrix, key = lambda x:x[2], reverse=True)[0:top_matches_count]
print len(top_similar)
#print top_similar

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
  #print "Common nouns and verbs"
  #print set(doclist[item[0]]) & set(doclist[item[1]])
  bigrams1 = mylib.make_bigrams(doc1[0])
  bigrams2 = mylib.make_bigrams(doc2[0])
  trigrams1 = mylib.make_trigrams(doc1[0])
  trigrams2 = mylib.make_trigrams(doc2[0])
  fourgrams1 = mylib.make_fourgrams(doc1[0])
  fourgrams2 = mylib.make_fourgrams(doc2[0])
  fivegrams1 = mylib.make_fivegrams(doc1[0])
  fivegrams2 = mylib.make_fivegrams(doc2[0])
  sixgrams1 = mylib.make_sixgrams(doc1[0])
  sixgrams2 = mylib.make_sixgrams(doc2[0])
  bg_sim = mylib.jaccard_similarity(bigrams1, bigrams2)
  tg_sim = mylib.jaccard_similarity(trigrams1, trigrams2)
  fog_sim = mylib.jaccard_similarity(fourgrams1, fourgrams2)
  fig_sim = mylib.jaccard_similarity(fivegrams1, fivegrams2)
  si_sim = mylib.jaccard_similarity(sixgrams1, sixgrams2)
  sim = []
  sim.append(bg_sim)
  sim.append(tg_sim)
  sim.append(fog_sim)
  sim.append(fig_sim)
  sim.append(si_sim)
  if tg_sim == 0.0:
    bg_tg_ratio = "INFINITE"
  else:
    bg_tg_ratio = bg_sim/float(tg_sim)
  print "Similarity features"
  print sim
  #print "BGTG ratio =", bg_tg_ratio
  print "Time difference=", abs(int(doc1[1])-int(doc2[1]))/float(3600000), "t1=", doc1[1], "t2=",doc2[1]
  #print set(bigrams1) & set(bigrams2)
  #print set(trigrams1) & set(trigrams2)
  #print set(fourgrams1) & set(fourgrams2)
  print "=="*40
  print "=="*40
  print ""


t2 = time.time()
print "Time taken is ", t2-t1
