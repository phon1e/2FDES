from firebase import firebase as fb
import json, firebase_admin
import pyrebase

def init():
    firebaseConfig = readJs('config.json')
    firebase = pyrebase.initialize_app(firebaseConfig)
    return firebase.database()


def insertDb(url,path, data):
    firebase = fb.FirebaseApplication(url, None)
    result = firebase.put(path,"users", data)


def readDb(config_file):
    db = init()
    return db.get()

def timestamp(user_id, record, time):
    db = init()
    d = db.child('users').child(f"{user_id}").child('timestamp').update({f"record{record}":f"{time}"})
    print(f'updated',d)


def deleteDb(url, path, key):
    init()
    db = fb.database()

    firebase = fb.FirebaseApplication(url, None)
    result = firebase.delete(path, key)
    print('record deleted')

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
def uploadImg(config_file, folder, filename, file):
    config = readJs(config_file)
    firebase = pyrebase.initialize_app(config)
    storage.child(f"{folder}/{filename}").put(file)
