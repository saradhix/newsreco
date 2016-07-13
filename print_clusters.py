import pymongo
import mylib
import sys

def get_article_data(article_id):
  acoll = db.articles_new
  article = acoll.find_one({"article_id": article_id})
  return article['desc']

conn = pymongo.MongoClient()
db = conn.test
coll = db.article_list
docs = coll.find()
print "Items=", docs.count() 
#print "Items to read=", items_to_read
cx = 0
for doc in docs:
  article_id_first = doc['article_id']
  article = get_article_data(article_id_first)
  related_articles=doc['related_articles']
  cluster_size = len(related_articles)
  print "Cluster ID ", cx, "Articles in cluster", cluster_size
  print article
  cx = cx + 1
  for article_id in related_articles:
    article = get_article_data(article_id)
    print article
    print "-"*50
  print "+"*50
print "Done"
