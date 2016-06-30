import sys
import pymongo
import itertools
import json
from gensim import models,corpora,similarities
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import RegexpTokenizer
import numpy as np
from scipy import spatial
import mylib
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
   			print "not found! ",  word
   	return np.array(new_list)/(len(filter_words_list)-count)

items_to_read = 200
top_matches_count = 2000

min_similarity = 0.2
max_similarity = 0.8
tokenizer = RegexpTokenizer(r'\w+')
model = models.Word2Vec.load_word2vec_format('word_vec_english.txt.vec')
conn = pymongo.MongoClient()
db = conn.test
collection = db.docpairs

docs = collection.find().limit(items_to_read)
similarities=[]
for doc in docs:
  vecs=[0,0]
  doca=doc['doca'][0]
  docb=doc['docb'][0]
  print doca
  print "*"*20
  print docb
  vecs[0]=generate_wordvectors(doca)
  vecs[1]=generate_wordvectors(docb)
  similarity = 1 - spatial.distance.cosine(vecs[0],vecs[1])
  print "Similarity=",similarity
  print doc['ds'], doc['sim2g'],doc['sim3g'],doc['sim4g']
  similarities.append(abs(similarity))
  print "=="*20
print max(similarities),min(similarities)
