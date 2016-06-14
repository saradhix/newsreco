import pprint
import sys, os
import pymongo
import itertools
import json


sys.path.insert(0, os.path.abspath('../..'))
from lsh import LSHCache


if __name__ == '__main__':
    cache = LSHCache()
    items_to_read = 300
    top_matches_count = 10 

    conn = pymongo.MongoClient()
    db = conn.test
    coll = db.articles

    docs_result = coll.find().limit(items_to_read)
    docs=[]
    for doc in docs_result:
        docs.append(doc['description'])
    print "Done fetching docs"

    dups = {}
    for i, doc in enumerate(docs):
        dups[i] = cache.insert(doc.split(), i)

    for i, duplist in dups.items():
        if duplist:
            print "-"*40
            print 'orig [%d]: ' % (i)
            print duplist
            print "-"*40
            for dup in duplist:
                print'\tdup : [%d] ' % (dup)
        else:
            #print 'no dups found for doc [%d] : %s' % (i, docs[i])
            pass
