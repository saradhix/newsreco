import json

data="""{ "x": "en",
"category": "politics",
"id": "5756d4611d41c808255d4fc4",
"categories": ["PK_ALL", "BIHAR_ALL", "IN_ALL", "IN_NEWS_POLITICS", "IN_NEWS"]}"""
print data

print json.loads('{"x":"foo", "y":"bar"}')
print json.loads(data)


