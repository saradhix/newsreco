#from __future__ import print_function
import sys
import pymongo
import itertools
import json

user_read_file = 'user_read_articles_set2'

conn = pymongo.MongoClient()
db = conn.test
coll = db.user_read_articles
coll.remove()

fp = open(user_read_file, 'r')

count = 0
for line in fp:
  #print line
  user_id = (line[0:36]).strip()
  articles_list_str = line[36:] 
  try:
    articles_list = json.loads(articles_list_str)
    json_obj={}
    json_obj['user_id']=user_id
    json_obj['articles_list']=articles_list
  except Exception as inst:
    continue
  coll.insert(json_obj)
  count = count + 1
  if count % 1000 == 0:
    print "Inserted %d documents" % count
print "Inserted %d documents" % count
