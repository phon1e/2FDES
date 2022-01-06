from firebase import firebase as fb
import json

def insertDb(url,path, myData, key):
    if all(isinstance(i, str) for i in [url, path, myData, key]):
        firebase = fb.FirebaseApplication(url, None)
        result = firebase.post(path, myData)
    raise TypeError('All must be String ! !')

def readDb(url,path):
    if all(isinstance(i, str) for i in [url, path]):
        firebase = fb.FirebaseApplication(url, None)
        result = firebase.get(path, '')
        return result
    raise TypeError('All must be String ! !')

def updateDb(url, path, user, key, val ):
    # if all(isinstance(i, str) for i in [url, path, user, key, val]):
    firebase = fb.FirebaseApplication(url, None)
    result = firebase.put(f'{path}/{user}', key, val)
    print(f'updated\n {result}')
    #print(f"{type(url)} {type(path)} {type(user)} {type(key)} {type(val)}")
    # else: print('All must be String ! !')

def deleteDb(url, path, key):
    if all(isinstance(i, str) for i in [url, path,key]):
        firebase = fb.FirebaseApplication(url, None)
        result = firebase.delete(path, key)
        print('record deleted')
    raise TypeError('All must be String ! !')

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

def getKeyDict(ls, indx):
    enum = enumerate(ls)
    d = dict((i,j) for j,i in enum)
    k = list(d.keys())[list(d.values()).index(indx)]
    return k
