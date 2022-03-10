import csv
import json
import pyrebase
from datetime import datetime
import calendar
import urllib.request

def init():
    firebaseConfig = readJs('config2.json')
    firebase = pyrebase.initialize_app(firebaseConfig)
    return firebase.database()


def downloadJson():
    db = init()
    data = db.child("users").get()
    data = data.val()
    print("downloading.... userdata")
    loadJs(data, "userdata.json", 5)
    print("download complete")

def timestamp(user_id):
    db = init()
    now = datetime.now()  # get current datatime
    dt = now.strftime("%d/%m/%Y %H:%M")  # format datetime
    last_day_in_month = calendar.monthrange(now.year, now.month)[1]  # check how many day in current month
    timestamp_ls = db.child("users").child(user_id).child("timestamp").child(now.strftime('%Y')).child(now.strftime('%B')).order_by_key().get()  # get timestamp list
    user_name = db.child("users").child(user_id).child("username").get()
    user_dict = {}

    if (timestamp_ls.val() is None):  # if no timestamp add record1
        record = 1
        d = db.child('users').child(user_id).child('timestamp').child(now.strftime('%Y')).child(now.strftime('%B')).order_by_key().update({f'record0{record}': f"{dt}"})
    else:
        last_record = list(timestamp_ls.val())[-1]  # get lastest timestamp
        pos = last_record[-2:]  # get lastest no of timestamp eg. record_30 got "30"
        record = int(pos) + 1
        curr_day = (list(timestamp_ls.val().values()))[-1][:2]  # get current day
        d = db.child('users').child(user_id).child('timestamp').child(now.strftime('%Y')).child(now.strftime('%B')).update({f'record{str(record).zfill(2)}': f"{dt}"})

    user_dict.update({user_name.val(): d})
    write_csv(user_dict, 'user.csv')

def readJs(filename):
    with open(filename) as json_file:
        d = json.load(json_file)
    return d

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
    firebaseConfig = readJs('config2.json')
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    storage.child(f"{folder}/{filename}").put(file)


def dl_img(dst_folder):
    db = init()
    firebaseConfig = readJs('config2.json')
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()

    u = db.child("users").get()
    all_user = u.val().keys()
    all_user_ls = list(all_user)

    for usr in all_user_ls:
        storage.child(f"images/{usr}/face.png").download(" ", f"{dst_folder}/{usr}.png")
        storage.child(f"images/{usr}/face.jpeg").download(" ", f"{dst_folder}/{usr}.jpeg")


def write_csv(data,filename):
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for k, v in data.items():
            writer.writerow([k, v])

def get_user_key(db):
    ls = list(db.keys())
    new_ls = []
    for usr in ls:
        if db[usr]["faceId"] == "exist":
            new_ls.append(usr)
    #ls.insert(0, "0") #insert 0 at front for handle mac addr indexing
    print(f"new_ls {new_ls}")
    return new_ls

def mac_format(mac_str): # change A2:B3 => 0xa5.0xb3
    h = mac_str.replace(":", " ")
    h = ','.join([f"0x{i}" for i in h.split()])
    return h    #return 0x format

def connect(host='https://firebase.google.com/'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
