import pymongo
import mylib
import sys
import math

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles_new
target_coll = db.verbs_nouns
target_coll.remove()
items_to_read = 1
#docs = coll.find().limit(items_to_read)
docs = coll.find()
num_docs = docs.count()
print "Items=", docs.count()

#print "Items to read=", items_to_read
cx = 0
verbs_dict = {}
nouns_dict = {}
idf_n_dict = {}
idf_v_dict = {}
for doc in docs:
  cx = cx + 1
  nouns = doc['nouns']
  verbs = doc['verbs']
  #print nouns
  #print verbs
  for verb in verbs:
    verbs_dict[verb] = verbs_dict.get(verb, 0) + 1
  for noun in nouns:
    nouns_dict[noun] = nouns_dict.get(noun, 0) + 1


  for verb in set(verbs):
    idf_v_dict[verb] = idf_v_dict.get(verb, 0) + 1
  for noun in set(nouns):
    idf_n_dict[noun] = idf_n_dict.get(noun, 0) + 1

  if cx % 1000 == 0:
    print "Documents processed =", cx

for word, tf in verbs_dict.iteritems():
  tf = 1+math.log(tf)
  idf = math.log(num_docs/idf_v_dict[word])
  tfidf = tf*idf
  target_coll.insert({'word':  word,'tf': tf, 'idf': idf,'tfidf':tfidf})

for word, tf in nouns_dict.iteritems():
  tf = 1+math.log(tf)
  idf = math.log(num_docs/idf_n_dict[word])
  tfidf = tf*idf
  target_coll.insert({'word':  word,'tf': tf, 'idf': idf, 'tfidf':tfidf})

print "Done"
