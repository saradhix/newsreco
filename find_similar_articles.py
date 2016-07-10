import pymongo
import mylib
import sys

max_days = 30
offset = max_days*24*60*60*1000 
#Number of microseconds in max_days
def main():

  conn = pymongo.MongoClient()
  db = conn.test
  coll = db.articles_new

  items_to_read = 1
  #articles = coll.find().limit(items_to_read)
  articles = coll.find()
  for article in articles:
    find_similar_articles(article)

def find_similar_articles(article):

  article_id = article['article_id']
  start_ts = article['ts']
  print "Entered find_similar_articles with article_id", article_id
  end_ts = int(start_ts) + offset
  print "Start ts=", start_ts, "End ts=", end_ts
  #It is better to cluster articles based on the topic


if __name__ == "__main__":
  # execute only if run as a script
  main()
