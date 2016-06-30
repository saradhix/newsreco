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
  objid = doc['_id']
  nouns_and_verbs = mylib.get_nouns_and_verbs(doc['desc'])
  result = db.articles.update_one({"_id":objid}, {"$set": {"nv": nouns_and_verbs} })
  print cx, "documents updated"

print "Done"
