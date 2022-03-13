import csv
import json
import pyrebase
from datetime import datetime
import calendar
import urllib.request
import os.path, shutil, filecmp

def init():
    firebaseConfig = readJs('config2.json')
    firebase = pyrebase.initialize_app(firebaseConfig)
    if(connect()):
        #print("Connected")
        return firebase.database()
    else:
        print("No Internet")

def downloadJson(): # dl json file from firebase
    db = init()
    data = db.child("users").get()
    data = data.val()
    print("downloading.... ")
    loadJs(data, "userdata.json", 5)
    print("download userdata completed")

def timestamp(user_id):     # timestamp yes just timestamp...
    db = init()
    now = datetime.now()  # get current datatime
    dt = now.strftime("%d/%m/%Y %H:%M")  # format datetime
    last_day_in_month = calendar.monthrange(now.year, now.month)[1]  # check how many day in current month
    timestamp_ls = db.child("users").child(user_id).child("timestamp").child(now.strftime('%Y')).child(now.strftime('%B')).order_by_key().get()  # get timestamp list
    user_name = db.child("users").child(user_id).child("username").get()
    user_dict = {}

    if (timestamp_ls.val() is None):  # if no timestamp add record1
        record = 1
        db.child('users').child(user_id).child('timestamp').child(now.strftime('%Y')).child(now.strftime('%B')).order_by_key().update({f'record0{record}': f"{dt}"})
        db.child('users').child(user_id).child('timestamp').order_by_key().update({f'lastStamp': f"{dt}"})
    else:
        last_record = list(timestamp_ls.val())[-1]  # get lastest timestamp
        pos = last_record[-2:]  # get lastest no of timestamp eg. record_30 got "30"
        record = int(pos) + 1
        curr_day = (list(timestamp_ls.val().values()))[-1][:2]  # get current day
        db.child('users').child(user_id).child('timestamp').child(now.strftime('%Y')).child(now.strftime('%B')).update({f'record{str(record).zfill(2)}': f"{dt}"})
        db.child('users').child(user_id).child('timestamp').order_by_key().update({f'lastStamp': f"{dt}"})

    # user_dict.update({user_name.val(): d})
    # write_csv(user_dict, 'user.csv')

def readJs(filename): # read json file and return dict
    with open(filename) as json_file:
        d = json.load(json_file)
    return d

def loadJs(data, filename, ind): # load json file
    json_object = json.dumps(data, indent= ind)
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

def getDictKey(ls, indx):

    enum = enumerate(ls)
    d = dict((i,j) for j,i in enum)
    k = list(d.keys())[list(d.values()).index(indx)]
    return k

def uploadImg(folder, filename, file): # upload img to firebase storage
    firebaseConfig = readJs('config.json')
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    storage.child(f"{folder}/{filename}").put(file)


def dl_img(dst_folder):# download all img from firebase storage
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


def write_csv(data,filename):# write csv file but no use... 
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def get_user_key(db): # get user's key(uid) in firebase database 
    ls = list(db.keys())
    haveFaceid = []
    for usr in ls:
        if db[usr]["faceId"] == "exist":
            #print(usr)
            haveFaceid.append(usr)
    # ls.insert(0, "0")#insert 0 at front for handle mac addr indexing
    return haveFaceid#ls

def mac_format(mac_str): # change hex to decimal
    h = mac_str.replace(":", " ")
    h = ','.join([f"{int(i,16)}" for i in h.split()])
    return h.lower()

def mapping(): #mapping just mapping...
    downloadJson()
    data = readJs("userdata.json")
    u_ls = get_user_key(data)
    mac = []
    mac_mapped = []
    k = 0
    for usr in u_ls:
        dict = data[usr]["macAddress"]
        v = 0
        for i in dict.values():
            v += 1
            i = mac_format(i)
            mac.append(i)
            mac_mapped.append(f"{k}_{v}")
        k += 1
    return mac, mac_mapped


def updateMac():    #mapping downloaded data and generate 2 file  
    print("downloading user's mac addr and mapping. . . ")
    mac, mapped = mapping()
    with open('/home/pi/Desktop/mkspiffs/mkspiffs-0.2.3-7-gf248296-arduino-esp8266-/data/mac.txt', 'w') as f:
        for line in mac:
            f.write(line)
            f.write('\n')
    with open('/home/pi/Desktop/mkspiffs/mkspiffs-0.2.3-7-gf248296-arduino-esp8266-/data/mapped.txt', 'w') as f:
        for line in mapped:
            f.write(line)
            f.write('\n')


def connect(host='https://firebase.google.com/'): # checking internet connection
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

def copy_to(src, dst):  #copy file to tmp folder for check are they same?
    files = os.listdir(src)
    for fname in files:
        shutil.copy2(os.path.join(src, fname), dst)

class dircmp(filecmp.dircmp): # compare 2 dir
 
    def phase3(self):
        """
        Find out differences between common files.
        Ensure we are using content comparison with shallow=False.
        """
        fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files,shallow=False)
        self.same_files, self.diff_files, self.funny_files = fcomp

def is_same(dir1, dir2):    # check all file in 2 dir is exacly same file return boolean?
    """
    Compare two directory trees content.
    Return False if they differ, True is they are the same.
    """
    compared = dircmp(dir1, dir2)
    if (compared.left_only or compared.right_only or compared.diff_files
        or compared.funny_files):
        return False
    for subdir in compared.common_dirs:
        if not is_same(os.path.join(dir1, subdir), os.path.join(dir2, subdir)):
            return False
    return True

def print_txt(s): # print pretty txt lol
  print("="*30)
  print(f"\n {s}\n")
  print("="*30)
