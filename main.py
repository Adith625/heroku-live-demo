from boltiot import Bolt
import json
import datetime
import time
import pymongo
from environs import Env
env = Env()
env.read_env()
server = pymongo.MongoClient(env.str("MongoDB"))
Bolt_Api = env.str("Bolt_Api")
Device_Id = env.str("Device_Id")
bolt = Bolt(Bolt_Api, Device_Id)
date_temp = datetime.datetime.now()
day = date_temp.strftime("%j")
month = date_temp.strftime("%m")
year = date_temp.strftime("%Y")
db = server[year]
coll = db[month]
day = int(day)
if coll.find_one({"_id": int(day)}) is None:
    coll.insert_one({"_id": int(day), "user_0": [], "user_1": [], "user_2": [], "user_3": []})


def user_exit(tag_id):
    print("user_" + tag_id + " has exited")
    temp = datetime.datetime.now()
    exit_time = {"hr": temp.strftime("%H"), "min": temp.strftime("%M")}
    user = "user_" + tag_id
    data = {"exit_time": exit_time}
    doc = coll.find_one({"_id": day})
    len_ = len(doc[user])
    len_ = len_ - 1
    doc[user][len_].update(data)
    coll.update_one({"_id": day}, {"$set": doc})


def user_enter(tag_id):
    print("user_" + tag_id + " has entered")
    temp = datetime.datetime.now()
    enter_time = {"hr": temp.strftime("%H"), "min": temp.strftime("%M")}
    user = "user_" + tag_id
    data = {"enter_time": enter_time}
    doc = coll.find_one({"_id": day})
    doc[user].append(data)
    coll.update_one({"_id": day}, {"$set": doc})


def tag_detected(tag_id):
    temp_date = datetime.datetime.now()
    new_day(temp_date)
    doc = coll.find_one({"_id": day})
    len_ = len(doc["user_" + tag_id])
    if len_ == 0:
        user_enter(tag_id)
        return
    len_ = len_ - 1
    presence = len(doc["user_" + str(tag_id)][len_])
    if presence == 2:
        user_enter(tag_id)
    elif presence == 1:
        user_exit(tag_id)


def add_exit(i):
    global coll
    global day
    data = {"exit_time": {"hr": "24", "min": "00"}}
    doc = coll.find_one({"_id": day})
    status = len(doc["user_" + i])
    status = status - 1
    doc["user_" + i][status].update(data)
    coll.update_one({"_id": day}, {"$set": doc})


def add_entry(i):
    data = {"enter_time": {"hr": "00", "min": "00"}}
    doc = coll.find_one({"_id": day})
    doc["user_" + i].append(data)
    coll.update_one({"_id": day}, {"$set": doc})


def new_year(temp_date):
    temp_year = temp_date.strftime("%Y")
    global year
    if temp_year != year:
        print("new_year")
        global db
        global server
        year = temp_year
        db = server[year]


def new_month(temp_date):
    temp_month = temp_date.strftime("%m")
    global month
    if temp_month != month:
        print("new_month")
        global coll
        global db
        month = temp_month
        coll = db[month]
        new_year(temp_date)


def new_day(temp_date):
    global day
    global coll
    temp_day = temp_date.strftime("%j")
    temp_day = int(temp_day)
    if temp_day != day:
        usr_list = []  # list of users' exit added
        print("new_day")
        doc = coll.find_one({"_id": day})
        for i in range(4):
            i = str(i)
            usr = "user_" + i
            presence = len(doc[usr])
            if presence == 0:
                continue
            presence = presence - 1
            presence = len(doc[usr][presence])
            if presence == 1:
                add_exit(i)
                print("added exit to user_" + i)
                usr_list.append(int(i))
        new_month(temp_date)
        data = {"_id": temp_day, "user_0": [], "user_1": [], "user_2": [], "user_3": []}
        coll.insert_one(data)
        day = temp_day
        for j in usr_list:
            add_entry(str(j))
            print("added entry to user_" + str(j))


while True:
    time.sleep(5)
    response = bolt.serialRead("10")
    ans = json.loads(response)
    if ans['success'] == 1:
        if ans['value'] != "":
            tag = ans['value']
            tag_detected(tag)
    else:
        print(response)
