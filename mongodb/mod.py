import json
import random
import datetime
import pymongo
from pymongo import MongoClient
with open("../API_KEYS.json") as api_keys:
    api_keys=api_keys.read()
api_keys=json.loads(api_keys)
server=pymongo.MongoClient(api_keys["mongodb"])
date_temp = datetime.datetime.now()
day = date_temp.strftime("%j")
month=date_temp.strftime("%m")
year=date_temp.strftime("%Y")
db = server[year]
coll=db[month]
if __name__ == '__main__':
    file_data={"_id":int(day),"user_0":[],"user_1":[],"user_2":[],"user_3":[]}
    for i in range(4):
        usr="user_"+str(i)
        a=random.randint(0,5)
        for b in range(a):
            hr=random.randint(0,23)
            min=random.randint(0,59)
            enter_time = {"hr":str(hr),"min":str(min)}
            hr=random.randint(hr,23)
            if (hr==int(enter_time["hr"])):
                min=random.randint(min,59)
                if(min==int(enter_time["min"])):
                    min=min+random.randint(1,59-min)
            else:
                min=random.randint(0,59)
                exit_time = {"hr":str(hr),"min":str(min)}
                data = {"enter_time":enter_time,"exit_time":exit_time}
                file_data[usr].append(data)
    coll.delete_one({"_id":int(day)})
    coll.insert_one(file_data) 
else:
    file_data=coll.find_one({"_id":int(day)})
    if file_data is None:
        data={"_id":int(day),"user_0":[],"user_1":[],"user_2":[],"user_3":[]}
        coll.insert_one(data)