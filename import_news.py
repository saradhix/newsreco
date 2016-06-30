#from __future__ import print_function
import sys
import pymongo
import itertools
import json

news_file = 'output'

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
  try:
    json_obj = json.loads(article)
  except Exception as inst:
    continue
  lang = json_obj.get('lang','U')
  #print json_obj
  #print "Article id= %s" % article_id
  if lang =='en':
      coll.insert(json_obj)
      count = count + 1
      if count % 1000 == 0:
          print "Inserted %d documents" % count
print "Inserted %d documents" % count
