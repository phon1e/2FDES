import mySvModule, time, json
from datetime import datetime as dt

url = 'https://sendfrompytest-default-rtdb.firebaseio.com/'
key = '-MrB7NvyVN1y8S8bVHbY'
path = f'/users/{key}/'

def testRead():
    start1 = time.time()
    d = mySvModule.readDb(url,path)
    ids = '0xfc,0x1d,0x43,0x31,0x94,0xc5'
    print("Read from firebase")


    for i in range(1,3):
        if ids in d[f'user{i}']['mac']:
              print(f'found {ids} in {d[f"user{i}"]["mac"]}')
              print(f'checked {d[f"user{i}"]["uname"]}')
    end1 = time.time()
    diff1 = end1 - start1
    print(f'execution time {diff1:.6f} sec' )

    # output
    # found 4444444443 in ['0000000001', '4444444443', '4444444445']
    # checked 044_uname
    start2 = time.time()


    mySvModule.loadJs(d, 'new.json', 5)
    db = mySvModule.readJs("new.json")
    print("\nRead from json")
    for i in range(1,3):
        if ids in db[f"user{i}"]['mac']:
            print(f'Found {ids} in { db[f"user{i}"]["mac"]}' )
            print(f'checked {db[f"user{i}"]["uname"]}')

    end2 = time.time()
    diff2 = end2 - start2
    print(f'execution time {diff2:.6f} sec' )


    print(f"\ndiff read time between local and server : {(diff1 - diff2):.6f} sec")
    # output
    #     Found
    #     4444444443 in ['0000000001', '4444444443', '4444444445']
    #     044
    #     _uname

    #print(f'read from firebase db {d}')
    #print(f'read from loaded file {js}')

# update mac to db
def testModify():
    c = 0
    mac_list = mySvModule.readJs("new.json")

    ######### update mac from json file to db ###########
    for i in mac_list[c]['mac']:
        mySvModule.updateDb(url, path, f'{c}/mac',str(c),str(i) )
        c+=1


    ########## add new mac to db ###############
    # mySvModule.updateDb(url, path, '0/mac','3','123')

    ########## delete specific mac from db #####

    mySvModule.deleteDb(url,f"{path}/0/mac",'3')



def timeUpdate():
    d = mySvModule.readDb(url, path)
    ids = '0xe6,0xbc,0x50,0x29,0xc6,0xb3' #'0xfc,0x1d,0x43,0x31,0x94,0xc5'
    print("Read from firebase")

    for i in range(1,3):
        if ids in d[f"user{i}"]['mac']:
            print(f'found {ids} in {d[f"user{i}"]["mac"]}')
            print(f'checked {d[f"user{i}"]["uname"]}')



    mySvModule.loadJs(d, 'new.json', 5)
    db = mySvModule.readJs("new.json")
    print("\nRead from json")
    for i in range(1, 3):
        if ids in db[f"user{i}"]['mac']:
            now = dt.now()
            s = now.strftime("%d/%m/%Y %H:%M")
            mySvModule.updateDb(url,path,f'{f"user{i}"}/timeStamp',str(i),s)

# mydata = mySvModule.readJs('read.json')

# mySvModule.insertDb(url,'/users/',mydata)

# d = mySvModule.readDb(url, f"/users/{key}")
# mySvModule.loadJs(d,'read.json',5)

    ####### testing #########
# testModify()
testRead()
# timeUpdate()

def findMacFromJson():
    import mySvModule, time, json

    d = mySvModule.readJs("new.json")

    print(d)
    txt = "0x12,0xa9,0x67,0x05,0xb6,0xf9"

    for c in range(1, 3):
        for i in d[f"user{c}"]["mac"]:
            if (txt in i):
                print(f"Found {txt} in user{c}")

