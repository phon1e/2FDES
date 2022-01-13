from firebase import firebase as fb
import json
import pyrebase
from datetime import datetime
import calendar

def init():
    firebaseConfig = readJs('config.json')
    firebase = pyrebase.initialize_app(firebaseConfig)
    return firebase.database()

def timestamp(user_id):
    db = init()
    now = datetime.now()  # get current datatime
    dt = now.strftime("%d/%m/%Y %H:%M")  # format datetime
    last_day_in_month = calendar.monthrange(now.year, now.month)[1]  # check how many day in current month
    last_time_stamp = db.child("users").child(user_id).child("timestamp").order_by_key().get()  # get timestamp list

    if (last_time_stamp.val() is None):  # if no timestamp add record1
        record = 1
        d = db.child('users').child(user_id).child('timestamp').update({f'record{record}': f"{dt}"})
    else:
        last_record = list(last_time_stamp.val())[-1]  # get lastest timestamp
        pos = last_record[6:]  # get lastest no of timestamp eg. record30 got "30"
        record = int(pos) + 1  # last record + 1 for next timestamp eg. record30 --> record31
        curr_day = (list(last_time_stamp.val().values()))[-1][:2] # get current day
        
        if (curr_day >= last_day_in_month):  # check if current record >= days in current month then set record to 1
            record = 1

        d = db.child('users').child(user_id).child('timestamp').update({f'record{record}': f"{dt}"})

def readJs(filename):
   if (isinstance(filename,str)):
        with open(filename) as json_file:
            d = json.load(json_file)
        return d
   raise TypeError('All must be String ! !')

def loadJs(data, filename, ind):
    json_object = json.dumps(data, indent= ind)
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

def getDictKey(ls, indx):
    enum = enumerate(ls)
    d = dict((i,j) for j,i in enum)
    k = list(d.keys())[list(d.values()).index(indx)]
    return k

def uploadImg(folder, filename, file):
    firebaseConfig = readJs('config.json')
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()

    storage.child(f"{folder}/{filename}").put(file)
