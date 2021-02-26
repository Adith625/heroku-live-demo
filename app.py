import datetime
import json
import pymongo
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from environs import Env
env = Env()
env.read_env() 
# server = pymongo.MongoClient(env.str("MongoDB"))
date = datetime.datetime.now()
# db = server[date.strftime("%Y")]
# coll = db[date.strftime("%m")]
app = Flask(__name__)
app.secret_key = env.str("Secret_Key")
debug = env.bool("Debug")


@app.route('/')
def home():
    return redirect(url_for('chart'))


# @app.route('/login', methods=["POST", "GET"])
# def login():
#     if "user_type" in session:
#         return redirect(url_for('chart'))
#     if request.method == "POST":
#         user = request.form.get("user_type")
#         psswd = request.form["psswd"]
#         if user == "admin" and psswd == "admin" or user == "user" and psswd == "user":
#             session["user_type"] = user
#             flash(user + " login successful", "info")
#             return redirect(url_for('chart'))
#         else:
#             flash("Incorrect password", "alert")
#             return redirect(url_for('login'))
#     else:
#         return render_template("login.html")

def random_data():
 file_data={"_id":int(date.strftime("%j")),"user_0":[],"user_1":[],"user_2":[],"user_3":[]}
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
 return file_data
# @app.route("/logout")
# def logout():
#     if "user_type" in session:
#         session.pop("user_type", None)
#         flash("Logout successful", "info")
#     return redirect(url_for('login'))


@app.route('/chart', methods=["POST", "GET"])
def chart():
    admin="admin"
    # if "user_type" in session:
    #     if session["user_type"] == "admin":
    #         admin = True
    #     elif session["user_type"] == "user":
    #         admin = False
    # else:
    #     flash("please login", "alert")
    #     return redirect(url_for('login'))
    date_temp = datetime.datetime.now()
    if request.method == "POST":
        v = request.form["date"]
        z = v.split("/")
        y = datetime.datetime(int(z[2]), int(z[0]), int(z[1]))
        y = y.strftime("%j")
        if date_temp.strftime("%j") == y:
            return redirect(url_for('chart'))
        file_data=random_data()
        f = -1
        file_data = json.dumps(file_data)
        return render_template('chart.html', file=file_data, status=f, min_date=365, date=v, admin=admin)
    else:
        file_data = random_data()
        f = {}
        for i in range(4):
                usr="user_"+str(i)
                r = {usr: random.choice([True,False])}
                f.update(r)
        file_data = json.dumps(file_data)
        f = json.dumps(f)
        v = date_temp.strftime("%m") + "/" + date_temp.strftime("%d") + "/" + date_temp.strftime("%Y")
        return render_template('chart.html', file=file_data, status=f, min_date=365, date=v, admin=admin)


def add_exit(tag, file_data):
    tag = str(tag)
    usr = "user_" + tag
    temp = datetime.datetime.now()
    exit_time = {"hr": temp.strftime("%H"), "min": temp.strftime("%M")}
    data = {"exit_time": exit_time}
    length = len(file_data[usr])
    length = length - 1
    file_data[usr][length].update(data)
    return file_data


def add_exit1(tag, file_data):
    tag = str(tag)
    usr = "user_" + tag
    exit_time = {"hr": 24, "min": 59}
    data = {"exit_time": exit_time}
    length = len(file_data[usr])
    length = length - 1
    file_data[usr][length].update(data)
    return file_data


if __name__ == "__main__":
    app.run(debug=debug)
