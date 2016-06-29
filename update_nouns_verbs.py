import pymongo
import mylib

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles

items_to_read = 1
#docs = coll.find().limit(items_to_read)
docs = coll.find()
doclist=[]
documents=[]
#print "Items to read=", items_to_read
cx = 0
for doc in docs:
  cx = cx + 1
  print cx, "documents updated"
  objid = doc['_id']
  nouns_and_verbs = mylib.get_nouns_and_verbs(doc['description'])
  result = db.articles.update_one({"_id":objid}, {"$set": {"nv": nouns_and_verbs} })
  if cx % 1000 == 0:
    print cx, "documents updated"

print "Done"