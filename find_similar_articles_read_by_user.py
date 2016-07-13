import pymongo
import mylib
import sys
import json
from gensim import models,corpora,similarities
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import RegexpTokenizer
import numpy as np
from scipy import spatial

#tokenizer = RegexpTokenizer(r'\w+')
#model = models.Word2Vec.load_word2vec_format('word_vec_english.txt.vec')

conn = pymongo.MongoClient()
db = conn.test
min_similarity = 0.2
max_similarity = 0.8
article_category_dict = {}
coll = db.articles_new
targetcoll = db.user_similar_articles
targetcoll.remove()
db.user_counts.remove()
def main():

  coll = db.user_read_articles

  items_to_read = 1
  #articles = coll.find().limit(items_to_read)
  users = coll.find()
  for i,user in enumerate(users):
    num_sim = find_similar_articles_read(user)
    db.user_counts.insert({"user": user['user_id'],"num_sim":num_sim})
    if i % 100 == 0:
     print "Processed ", i, " users"

def find_similar_articles_read(user):
  user_id = user['user_id']
  num_sim = 0

  articles_list = user['articles_list']
  num_articles = len(articles_list)
  print "Entered find_similar_articles with user", user_id, num_articles
  if num_articles > 600:
    return 0

  for i in range(0,num_articles):
    for j in range(i+1, num_articles):
      a = articles_list[i]
      b = articles_list[j]
      num_sim += process_article_pair(a, b)
  return num_sim

def process_article_pair(a, b):
  #print "Entered pap with ", a, b

  itema = coll.find_one({"article_id": a})
  if itema is None:
    return 0
  itemb = coll.find_one({"article_id": b})
  if itemb is None:
    return 0
  if itema.get('cat',0) != itemb.get('cat',1):
    return 0
  na = itema['nouns']
  nb = itemb['nouns']
  va = itema['verbs']
  vb = itemb['verbs']
  nva = na + va
  nvb = nb + vb

  js_sim_nv = mylib.jaccard_similarity(nva, nvb)
  if js_sim_nv >= min_similarity and js_sim_nv <= max_similarity:
    print "JS", js_sim_nv, "acat", itema['cat'], "bcat", itemb['cat']
    targetcoll.insert({"a":a,"b":b,"js_sim":js_sim_nv})
    return 1;

  return 0

    #sys.exit()

if __name__ == "__main__":
  # execute only if run as a script
  main()
