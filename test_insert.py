#from __future__ import print_function
import sys
import pymongo
import itertools
import json


conn = pymongo.MongoClient()
db = conn.test
coll = db.test_collection
coll.remove()
json_obj={'name':'Vijay','age':23}
coll.insert(json_obj)
