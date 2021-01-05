from flask import Flask,render_template,request,redirect,url_for,session,flash
import json
import secrets
import datetime
import pymongo
from pymongo import MongoClient
with open("../API_KEYS.json") as api_keys:
  api_keys=api_keys.read()
api_keys=json.loads(api_keys)
server=pymongo.MongoClient(api_keys["mongodb"])
date= datetime.datetime.now()
db=server[date.strftime("%Y")]
coll=db[date.strftime("%m")]
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
@app.route('/')
def home():
  if "user_type" in session:
   return redirect(url_for('chart'))
  else:
    return redirect(url_for('login'))
@app.route('/login',methods=["POST","GET"])
def login():
  # session["user_type"]="user"
  if "user_type" in session:
   return redirect(url_for('chart'))
  if request.method == "POST":
   user = request.form.get("user_type")
   psswd= request.form["psswd"]
   if user=="admin" and psswd=="admin_psswd" or user=="user" and psswd=="user_psswd":
     session["user_type"]=user
     flash("Login successful","info")
     return redirect(url_for('chart'))
   else:
    flash("Incorect password","alert")
    return redirect(url_for('login'))
  else:
   return render_template("login.html") 

@app.route("/logout")
def logout():
  if "user_type" in session:
   session.pop("user_type",None)
   flash("Logout successful","info")
  return redirect(url_for('login'))


@app.route('/chart', methods=["POST","GET"])
def chart():
 if "user_type" in session:
  if session["user_type"]=="admin":
    admin=True
  elif session["user_type"]=="user":
     admin=False
 else:
  flash("please login","alert")
  return redirect(url_for('login'))
 date_temp=datetime.datetime.now()
 dbs=[]
 for yr in server.list_database_names():
  if yr.isdigit():
    dbs.append(int(yr))
 dbs=min(dbs)
 colls=server[str(dbs)].list_collection_names()
 colls = list(map(str,colls))
 min_month=sorted(colls)
 min_month=str(min_month[0])
 min_month=server[str(dbs)][min_month]
 min_day= min_month.aggregate(
   [
     {
       '$group':
       { 
         "_id":{},
         "min_day": { '$min': "$_id" }
       }
       }
     
   ]
  );
 min_day=list(min_day)
 min_day=min_day[0]["min_day"]
 n=int(date_temp.strftime("%j"))-int(min_day)
 for yrs in range(int(date_temp.strftime("%Y"))-dbs):
  n=n+365
  if int(datetime.date(int(dbs+yrs),3,1).strftime("%j"))!=60:
    n=n+1
 global coll
 if request.method=="POST":
  v=request.form["date"]
  z=v.split("/")
  y=datetime.datetime(int(z[2]),int(z[0]),int(z[1]))
  y= y.strftime("%j")
  db=server[z[2]]
  coll=db[z[0]]
  if date_temp.strftime("%j")==y: #is same date is chosen
   return redirect(url_for('chart'))
  file_data=coll.find_one({"_id":int(y)})
  if (file_data is None or file_data=={"_id":int(y),"user_0":[],"user_1":[],"user_2":[],"user_3":[]}):
   # return f"data not present <a href='/chart'>goback</a>"
   flash('Data not present','alert')
   return redirect(url_for("chart"))
  for i in range(4):
    usr = "user_"+str(i)
    b=len(file_data[usr])
    if(b==0):
      continue
    b=b-1
    b=len(file_data[usr][b])
    if(b==1):
      file_data=add_exit1(i,file_data)
  f=-1
  file_data=json.dumps(file_data)
  return render_template('chart.html',file=file_data,status=f,min_date=n,date=v,admin=admin)
 else:                                  #GET
  db=server[date_temp.strftime("%Y")]
  h=date_temp.strftime("%m")
  coll=db[h]
  file_data=coll.find_one({"_id":int(date_temp.strftime("%j"))})
  if file_data is None:
   flash('Data not present','alert')
   return redirect(url_for("logout"))
  f={}
  for i in range(4):
    usr = "user_"+str(i)
    b=len(file_data[usr])
    if b==0:
      r={usr:False}
      f.update(r)
      continue
    b=b-1
    b=len(file_data[usr][b])
    if(b==1):
      r={usr:True}
      f.update(r)
      file_data=add_exit(i,file_data)
    else:
      r={usr:False}
      f.update(r)
  file_data=json.dumps(file_data)
  f=json.dumps(f)
  v=date_temp.strftime("%m")+"/"+date_temp.strftime("%d")+"/"+date_temp.strftime("%Y")
  return render_template('chart.html',file=file_data,status=f,min_date=n,date=v,admin=admin)

def add_exit(tag,file_data):
  tag=str(tag)
  usr = "user_"+tag
  temp = datetime.datetime.now()
  exit_time = {"hr":temp.strftime("%H"),"min":temp.strftime("%M")}
  data = {"exit_time":exit_time}
  length = len(file_data[usr])
  length = length-1
  file_data[usr][length].update(data)
  return(file_data)
def add_exit1(tag,file_data):
  tag=str(tag)
  usr = "user_"+tag
  exit_time = {"hr":24,"min":59}
  data = {"exit_time":exit_time}
  length = len(file_data[usr])
  length = length-1
  file_data[usr][length].update(data)
  return(file_data)
if __name__  == "__main__":
  app.run(debug=True)
