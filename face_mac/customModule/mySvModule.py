from firebase import firebase as fb
import json

def insertDb(url,path, myData, key):    #add new db to server
    firebase = fb.FirebaseApplication(url, None)
    result = firebase.put(path, key, myData)


def readDb(url,path):   #read db from server
    firebase = fb.FirebaseApplication(url, None)
    result = firebase.get(path, '')
    return result


def updateDb(url, path, user, key, val ):   #update value in db
    firebase = fb.FirebaseApplication(url, None)
    result = firebase.put(f'{path}/{user}', key, val)
    print(f'updated\n {result}')


def deleteDb(url, path, key):   #delete specific path in db
    firebase = fb.FirebaseApplication(url, None)
    result = firebase.delete(path, key)
    print('record deleted')

def readJs(filename):   #read json file
    if (isinstance(filename,str)):
        with open(filename) as json_file:
            d = json.load(json_file)
        return d
   raise TypeError('All must be String ! !')

def loadJs(data, filename, ind):    #load json file from server and save as new file.
    json_object = json.dumps(data, indent= ind)
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

def getKeyDict(ls, indx):   # input ls to auto create dict and return key of specific indx.
    enum = enumerate(ls)
    d = dict((i,j) for j,i in enum)
    k = list(d.keys())[list(d.values()).index(indx)]
    return k
