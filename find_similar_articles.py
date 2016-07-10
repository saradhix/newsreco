import pymongo
import mylib
import sys
import json
import math
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
min_similarity = 0.15
max_similarity = 0.75
max_days = 30
offset = max_days*24*60*60*1000 
#Number of microseconds in max_days
conn = pymongo.MongoClient()
db = conn.test
coll = db.articles_new_with_verbs
targetcoll = db.article_pairs
targetcoll.remove()

def main():

  items_to_read = 1
  #articles = coll.find().limit(items_to_read)
  topics = coll.distinct("cat")
  num = 0
  for topic in topics:
    num += find_similar_articles(topic)
  print "Total num=", num

def find_similar_articles(topic):
  print  "Entered fsa with topic", topic
  articles = coll.find({"cat":topic}).sort([("ts",1)])
  num_articles = articles.count()
  articles_list=[]
  for article in articles:
    articles_list.append(article)

  for i in range(0, num_articles):
    for j in range(i+1, num_articles):
      itema = articles_list[i]
      itemb = articles_list[j]
      process_article_pair(itema, itemb)
      print "i=",i, "j=",j, "topic=", topic, "num=", num_articles
  return num_articles

def process_article_pair(itema, itemb):
  #print "Entered pap with ", a, b

  nva = itema['nv']
  nvb = itemb['nv']

  js_sim_nv = mylib.jaccard_similarity(nva, nvb)
  if js_sim_nv >= min_similarity and js_sim_nv <= max_similarity:
  #if True:
    #Now calculate the wv similarity
    doca = itema['desc']
    docb = itemb['desc']
    #print doca
    #print "-"*40
    #print docb
    veca = generate_wordvectors(doca)
    vecb = generate_wordvectors(docb)
    similarity = 1 - spatial.distance.cosine(veca,vecb)
    similarity = math.fabs(similarity)
    print "JS", js_sim_nv, "WV", similarity
    targetcoll.insert({"itema":itema,"itemb":itemb,"js_sim":js_sim_nv,
    "wv_sim":similarity})
    print "="*40

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
