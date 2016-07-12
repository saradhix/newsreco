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
import os

#tokenizer = RegexpTokenizer(r'\w+')
#print "Reading model file. May take some time"
#model = models.Word2Vec.load_word2vec_format('word_vec_english.txt.vec')
#model = models.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
#print "Done reading model file"

conn = pymongo.MongoClient()
db = conn.test
min_similarity = 0.15
max_similarity = 0.75
max_days = 30
offset = max_days*24*60*60*1000 
#Number of microseconds in max_days
conn = pymongo.MongoClient()
db = conn.test
coll = db.articles_new
targetcoll = db.article_pairs_nvjs
#targetcoll.remove()

topic_resume_file = 'topics.resume'
index_resume_file = 'index.resume'

def main():

  items_to_read = 1
  #articles = coll.find().limit(items_to_read)
  #Read the completed topics into a list
  processed_topics = []
  try:
    fp = open(topic_resume_file,'r')
    for processed_topic in fp:
      processed_topics.append(processed_topic.strip())
    fp.close()
  except:
    print "topic_resume_file not present"
    pass
    #If file not present processed_topics would be empty
  topics = coll.distinct("cat")
  num = 0
  for topic in topics:
    if topic is None: continue
    if topic in processed_topics: continue
    num += find_similar_articles(topic)
    try:
      fp = open(topic_resume_file,'a+')
      fp.write(topic+'\n')
      fp.close()
    except:
      print "Write to topic resume file failed"

  print "Total num=", num

def find_similar_articles(topic):
  print  "Entered fsa with topic", topic
  #Check if index.resume is present
  start_index = 0
  try:
    fp = open(index_resume_file,'r')
    start_index = int(fp.read().strip())
    fp.close()
    #Delete the file
    os.remove(index_resume_file)
  except:
    print "No index file present"

  print "Start index =", start_index
  articles = coll.find({"cat":topic}).sort([("ts",1)])
  num_articles = articles.count()
  articles_list=[]
  for article in articles:
    articles_list.append(article)
  print "Num articles=", num_articles
  for i in range(start_index, num_articles):
    for j in range(i+1, num_articles):
      itema = articles_list[i]
      itemb = articles_list[j]
      process_article_pair(itema, itemb)
      print "i=",i, "j=",j, "topic=", topic, "num=", num_articles
    try:
      fp = open(index_resume_file,'w')
      fp.write(str(i)+'\n')
      fp.close()
    except:
      print "Write to index resume file failed"
   #Delete the file
  os.remove(index_resume_file)
  return num_articles

def process_article_pair(itema, itemb):
  #print "Entered pap with ", a, b

  na = itema['nouns']
  va = itema['verbs']
  nb = itemb['nouns']
  vb = itemb['verbs']

  nva = na + va
  nvb = nb + vb

  js_sim_nv = mylib.jaccard_similarity(nva, nvb)
  if js_sim_nv >= min_similarity and js_sim_nv <= max_similarity:
    noun_sim = mylib.jaccard_similarity(na, nb)
    verb_sim = mylib.jaccard_similarity(va, vb)
  #if True:
    #Now calculate the wv similarity
    #doca = itema['desc']
    #docb = itemb['desc']
    #print doca
    #print "-"*40
    #print docb
    #veca = generate_wordvectors(doca)
    #vecb = generate_wordvectors(docb)
    #similarity = 1 - spatial.distance.cosine(veca,vecb)
    #similarity = math.fabs(similarity)
    print "JS", js_sim_nv, "NS", noun_sim, "VS", verb_sim
    targetcoll.insert({"itema":itema,"itemb":itemb,"js_sim":js_sim_nv,
        "noun_sim":noun_sim, "verb_sim": verb_sim})
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
