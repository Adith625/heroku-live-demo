from boltiot import Bolt
import json
import datetime
import time
import pymongo
from pymongo import MongoClient
with open("/home/mint/Desktop/python/API_KEYS.json") as api_keys:
  api_keys=api_keys.read()
api_keys=json.loads(api_keys)
server=pymongo.MongoClient(api_keys["mongodb"])
bolt_api = api_keys["bolt"]["bolt_api"]
device_id = api_keys["bolt"]["device_id"]
bolt = Bolt(bolt_api,device_id)
date_temp = datetime.datetime.now()
day = date_temp.strftime("%j")
month=date_temp.strftime("%m")
year=date_temp.strftime("%Y")
db = server[year]
coll=db[month]
day=int(day)
def exit(tag):
  print("user_"+tag+" has exited")
  temp = datetime.datetime.now()
  exit_time = {"hr":temp.strftime("%H"),"min":temp.strftime("%M")}
  user="user_" +tag
  data = {"exit_time":exit_time}
  doc = coll.find_one({"_id":day})
  length = len(doc[user])
  length = length-1
  doc[user][length].update(data)
  coll.update_one({"_id":day},{"$set":doc})

def enter(tag):
  print("user_"+tag+" has entered")
  temp=datetime.datetime.now()
  enter_time =  {"hr":temp.strftime("%H"),"min":temp.strftime("%M")}
  user = "user_"+tag
  data ={"enter_time":enter_time}
  doc = coll.find_one({"_id":day})
  doc[user].append(data)
  coll.update_one({"_id":day},{"$set":doc})

def tag_detected(tag):
  temp_date = datetime.datetime.now()
  new_day(temp_date)
  doc = coll.find_one({"_id":day})
  length=len(doc["user_"+tag])
  if(length==0):
   enter(tag)
   return
  length=length-1
  presence=len(doc["user_"+str(tag)][length])
  if(presence==2):
   enter(tag)
  elif(presence==1):
   exit(tag)

def add_exit(i):
 global coll
 global day
 data={"exit_time":{"hr":"24","min":"00"}}
 doc=coll.find_one({"_id":day})
 status=len(doc["user_"+i])
 status=status-1
 doc["user_"+i][status].update(data)
 coll.update_one({"_id":day},{"$set":doc})

def add_entry(i):
 data={"enter_time":{"hr":"00","min":"00"}}
 doc=coll.find_one({"_id":day})
 doc["user_"+i].append(data)
 coll.update_one({"_id":day},{"$set":doc})

def new_year(temp_date):
    temp_year=temp_date.strftime("%Y")
    global year
    if(temp_year!=year):
     print("new_year")
     global db
     global server
     year=temp_year
     db=server[year]

def new_month(temp_date):
     temp_month=temp_date.strftime("%m")
     global month
     if(temp_month!=month):
       print("new_month")
       global coll
       global db
       month=temp_month
       coll=db[month]
       new_year(temp_date)

def new_day(temp_date):
   global day
   global coll
   temp_day=temp_date.strftime("%j")
   temp_day=int(temp_day)
   if(temp_day!=day):
    usr_list=[]                     #list of users' exit added
    print("newday")
    doc=coll.find_one({"_id":day})
    for i in range(4):
     i=str(i)
     usr="user_"+i
     presence=len(doc[usr])
     if presence==0:
      continue
     presence=presence-1
     presence=len(doc[usr][presence])
     if (presence==1):
      add_exit(i)
      print("added exit to user_"+i)
      usr_list.append(int(i))
    new_month(temp_date)
    data={"_id":temp_day,"user_0":[],"user_1":[],"user_2":[],"user_3":[]}
    coll.insert_one(data)
    day=temp_day
    for j in usr_list:
     add_entry(str(j))
     print("added entry to user_"+j)

while(True):
  time.sleep(5)
  response = bolt.serialRead(10)
  ans = json.loads(response)
  if(ans['success']==1):
    if(ans['value'] != ""):
      tag = ans['value']
      tag_detected(tag)
  else:
    print(response)
