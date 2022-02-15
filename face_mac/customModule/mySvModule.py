import csv
import json
import pyrebase
from datetime import datetime
import calendar
import urllib.request

def init():
    firebaseConfig = readJs('config.json')
    firebase = pyrebase.initialize_app(firebaseConfig)
    print( 'server connected' if connect() else 'no internet!' )
    return firebase.database()

def timestamp(user_id):
    db = init()
    now = datetime.now()  # get current datatime
    dt = now.strftime("%d/%m/%Y %H:%M")  # format datetime
    timestamp_ls = db.child("users").child(user_id).child("timestamp").child(now.strftime('%B')).order_by_key().get()  # get timestamp list

    if (timestamp_ls.val() is None):  # if no timestamp add record1
        record = 1
        d = db.child('users').child(user_id).child('timestamp').child(now.strftime('%B')).order_by_key().update({f'record0{record}': f"{dt}"})
    else:
        last_record = list(timestamp_ls.val())[-1]  # get lastest timestamp
        pos = last_record[-2:]  # get lastest no of timestamp eg. record_30 got "30"
        record = int(pos) + 1
        d = db.child('users').child(user_id).child('timestamp').child(now.strftime('%B')).update({f'record{str(record).zfill(2)}': f"{dt}"})
        write_csv(d, 'users.csv')
        
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

def write_csv(data,filename):
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
def connect(host='https://firebase.google.com/'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
