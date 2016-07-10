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

tokenizer = RegexpTokenizer(r'\w+')
model = models.Word2Vec.load_word2vec_format('word_vec_english.txt.vec')

conn = pymongo.MongoClient()
db = conn.test
min_similarity = 0.2
max_similarity = 0.8
article_category_dict = {}
def main():

  coll = db.user_read_articles

  items_to_read = 1
  #articles = coll.find().limit(items_to_read)
  users = coll.find()
  for i,user in enumerate(users):
    find_similar_articles_read(user)
    print "Processed ", i, " users"

def find_similar_articles_read(user):
  user_id = user['user_id']

  articles_list = user['articles_list']
  num_articles = len(articles_list)
  print "Entered find_similar_articles with user", user_id, num_articles
  if num_articles > 30:
    return

  for i in range(0,num_articles):
    for j in range(i+1, num_articles):
      a = articles_list[i]
      b = articles_list[j]
      process_article_pair(a, b)

def process_article_pair(a, b):
  #print "Entered pap with ", a, b

  coll = db.articles_new_with_verbs
  targetcoll = db.user_similar_articles
  itema = coll.find_one({"article_id": a})
  if itema is None:
    return
  itemb = coll.find_one({"article_id": b})
  if itemb is None:
    return
  nva = itema['nv']
  nvb = itemb['nv']

  js_sim_nv = mylib.jaccard_similarity(nva, nvb)
  if js_sim_nv >= min_similarity and js_sim_nv <= max_similarity:
    print itema
    print itemb
    #Now calculate the wv similarity
    doca = itema['desc']
    docb = itemb['desc']
    veca = generate_wordvectors(doca)
    vecb = generate_wordvectors(docb)
    similarity = 1 - spatial.distance.cosine(veca,vecb)
    print "JS", js_sim_nv, "WV", similarity
    targetcoll.insert({"a":a,"b":b,"js_sim":js_sim_nv,
    "wv_sim":similarity, "doca":doca,"docb":docb})

    #sys.exit()

def generate_wordvectors(string):
  words_list=tokenizer.tokenize(string.lower())
  filter_words_list=words_list[:]
  new_list=[]
  count=0
  for word in words_list:
    if word in stopwords.words('english'):
      filter_words_list.remove(word)
      for word in filter_words_list:
        try:
          wordVector = model[word]
          if len(new_list)==0:
            new_list.append(wordVector)
          else:
            new_list=[x+y for (x,y) in zip(new_list,wordVector)]
        except KeyError:
          count=count+1
          #print "not found! ",  word
  return np.array(new_list)/(len(filter_words_list)-count) 

if __name__ == "__main__":
  # execute only if run as a script
  main()
