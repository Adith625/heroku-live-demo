import json
import random
import datetime
import pymongo
from pymongo import MongoClient
server=pymongo.MongoClient("mongodb://localhost:27017")
date_temp = datetime.datetime.now()
day = date_temp.strftime("%j")
month=date_temp.strftime("%m")
year=date_temp.strftime("%Y")
db = server[year]
coll=db[month]
file_data={"_id":int(day),"user_0":[],"user_1":[],"user_2":[],"user_3":[]}
for i in range(4):
  usr="user_"+str(i)
  val=random.randint(0,4)
  num=0
  for a in range(val):
    num=num+val
    if a == 0:
     hr=random.randint(0,val)
     min=random.randint(0,59)
    else:
     hr=random.randint(num,num+val)
     if(hr==file_data[usr][a-1]["exit_time"]["hr"]):
       min=random.randint(int(file_data[usr][a-1]["exit_time"]["min"]),59)
     else:
       min=random.randint(0,59)
    enter_time = {"hr":str(hr),"min":str(min)}
    num=num+val
    hr=random.randint(int(enter_time["hr"]),num)
    if (hr==int(enter_time["hr"])):
     min=random.randint(int(enter_time["min"]),59)
    else:
     min=random.randint(0,59)
    exit_time = {"hr":str(hr),"min":str(min)}
    data = {"enter_time":enter_time,"exit_time":exit_time}
    file_data[usr].append({"enter_time":enter_time,"exit_time":exit_time})
print(file_data)
coll.delete_one({"_id":int(day)})
coll.insert_one(file_data) 
