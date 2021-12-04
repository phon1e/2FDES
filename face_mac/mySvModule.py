
def insertDb(url,path, myData, key):
    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)
    path = '/dbUser/User'
    result = firebase.post(path, myData)
    # key = '-MpztlIWjJcoY81LOBHv'
    result = firebase.delete(path,key)

def readDb(url,path):

    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)

    result = firebase.get(path, '')
    # print(result['-MpztlIWjJcoY81LOBHv']['faceId'])
    return result


def updateDb(url, path, user, key, val ):
    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)

    result = firebase.put(f'{path}/{user}', key, val)

    print(result)

def deleteDb(url, path, key):
    from firebase import firebase
    firebase = firebase.FirebaseApplication(url, None)
    result = firebase.delete(path, key)

    print('record deleted')
