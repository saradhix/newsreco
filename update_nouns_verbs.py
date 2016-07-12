import pymongo
import mylib
import sys

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles_new

items_to_read = 1
#docs = coll.find().limit(items_to_read)
docs = coll.find({"nouns":{"$exists":0}})
print "Items=", docs.count()

#print "Items to read=", items_to_read
cx = 0
for doc in docs:
  cx = cx + 1
  objid = doc['_id']
  article_id = doc['article_id']
  (nouns,verbs) = mylib.get_nouns_and_verbs(doc['desc'])
  result = coll.update_one({"_id":objid}, {"$set": {"nouns": nouns, "verbs":verbs} })
  print article_id, objid
  if cx % 100 == 0:
    print cx, "documents updated with nv"

print "Done"
