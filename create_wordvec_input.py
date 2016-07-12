import pymongo
import sys

conn = pymongo.MongoClient()
db = conn.test
coll = db.articles_new

#docs = coll.find().limit(items_to_read)
docs = coll.find()
doclist=[]
documents=[]
print "Starting to read"
cx = 0
file_name = 'word_vec_english.txt'
f = open(file_name, 'w')
for doc in docs:
  cx = cx + 1
  print cx, "documents updated"
  objid = doc['_id']
  description = doc['desc']
  f.write(description.encode('utf-8')+'\n')
  if cx % 10000 == 0:
    print cx, "documents updated"
    sys.exit()

print "Done"
f.close()
