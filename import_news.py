#from __future__ import print_function
import sys
import pymongo
import itertools
import json

news_file = 'newsarticles.txt'

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles
coll.remove()

fp = open(news_file, 'r')

#map(print, fp.read().split('\n')[0:2])

#map(print, itertools.repeat(fp.readline(),3))
count = 0
for line in fp:
  #print line
  article_id = (line[0:8]).strip()
  article = line[8:]
  json_obj = json.loads(article)
  #print json_obj['lang']
  #print json_obj
  #print "Article id= %s" % article_id
  if json_obj['lang'] == 'en':
      coll.insert(json_obj)
      count = count + 1
      if count % 1000 == 0:
          print "Inserted %d documents" % count
print "Inserted %d documents" % count
