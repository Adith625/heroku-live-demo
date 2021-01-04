import json
import datetime
import pymongo
from pymongo import MongoClient
with open("/home/mint/Desktop/python/API_KEYS.json") as api_keys:
  api_keys=api_keys.read()
api_keys=json.loads(api_keys)
server=pymongo.MongoClient(api_keys["mongodb"])
date_temp = datetime.datetime.now()
day = date_temp.strftime("%j")
month=date_temp.strftime("%m")
year=date_temp.strftime("%Y")
db = server[year]
coll=db[month]
data={"_id":int(day),"user_0":[],"user_1":[],"user_2":[],"user_3":[]}
coll.delete_one({"_id":int(day)})
coll.insert_one(data)
print(month)