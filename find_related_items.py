import sys
import pymongo
import itertools
import json

import mylib


num_items_to_read = 5000
num_items_to_skip = 10000

min_similarity = 0.2
max_similarity = 0.8

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles_new
target_collection = db.docpairs

docs = coll.find().limit(num_items_to_read).skip(num_items_to_skip)
cx = 0
words = {}
for doc in docs:
  nouns = doc['nouns']
  verbs = doc['verbs']
  for verb in verbs:
    obj = db.verbs_nouns.find_one({"word": verb})
    tfidf = obj['tfidf']
    words[verb]=tfidf
  for noun in nouns:
    obj = db.verbs_nouns.find_one({"word": noun})
    tfidf = obj['tfidf']
    words[noun]=tfidf

  sort_words = sorted(words.items(), key=lambda x:x[1], reverse=True)


  print sort_words
  sys.exit()
