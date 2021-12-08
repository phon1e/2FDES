from firebase import firebase as fb
improt json

def insertDb(url,path, myData, key):

    firebase = fb.FirebaseApplication(url, None)
    #path = '/dbUser/User'
    result = firebase.post(path, myData)
    # key = '-MpztlIWjJcoY81LOBHv'
    result = firebase.delete(path,key)

def readDb(url,path):

    firebase = fb.FirebaseApplication(url, None)
    result = firebase.get(path, '')
    # print(result['-MpztlIWjJcoY81LOBHv']['faceId'])
    return result


def updateDb(url, path, user, key, val ):
    firebase = fb.FirebaseApplication(url, None)
    result = firebase.put(f'{path}/{user}', key, val)

    print(result)

def deleteDb(url, path, key):

    firebase = fb.FirebaseApplication(url, None)
    result = firebase.delete(path, key)
    print('record deleted')

def readJs(filename):
    import json
    with open(filename) as json_file:
        d = json.load(json_file)
    return d

def loadJs(data, filename, ind):
    json_object = json.dumps(data, indent= ind)
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

