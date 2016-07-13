import pymongo
import mylib
import sys

conn = pymongo.MongoClient()
db = conn.test
coll = db.article_pairs_nvjs
target = db.article_list
target.remove()
items_to_read = 1
#docs = coll.find().limit(items_to_read)
article_ids = coll.distinct("itema.article_id")
print "Items=", len(article_ids)
#print "Items to read=", items_to_read
cx = 0
for article_id in article_ids:
  related_articles=[]
  cx = cx + 1
  itembs = coll.find({"itema.article_id":article_id})
  num_related = itembs.count()
  for item in itembs:
    related_articles.append(item['itemb']['article_id'])
  target.insert({"article_id": article_id, "related_articles": related_articles,
    "num_related": num_related})
  print "Updated %s with %d related" % ( article_id, num_related)
  if cx % 100 == 0:
    print cx, "clusters updated with related articles"

print "Done"
