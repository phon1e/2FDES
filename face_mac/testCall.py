import mySvModule, time, json

url = 'https://sendfrompytest-default-rtdb.firebaseio.com/'
key = '-MqHz5m_algE-XHj4WXM'
path = f'/dbUser/{key}/users'

def testRead():
    start1 = time.time()
    d = mySvModule.readDb(url,path)
    i = 0
    ids = '0xfc,0x1d,0x43,0x31,0x94,0xc5'
    print("Read from firebase")


    for i in range(3):
        if ids in d[i]['mac']:
              print(f'found {ids} in {d[i]["mac"]}')
              print(f'checked {d[i]["username"]}')
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
    for i in range(3):
        if ids in db[i]['mac']:
            print(f'Found {ids} in { db[i]["mac"]}' )
            print(f'checked {db[i]["username"]}')

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
    # mac_list = {'0': '0xe6,0xbc,0x50,0xb3,0x29,0xc6',
    #             '1': '0x12,0xa9,0x67,0x05,0xb6,0xf9',
    #             '2': '0xfc,0x1d,0x43,0x31,0x94,0xc5'}
    mac_list = mySvModule.readJs("new.json")

    ######### update mac from json file to db ###########
    for i in mac_list[c]['mac']:
        mySvModule.updateDb(url, path, f'{c}/mac',str(c),str(i) )
        c+=1

    ########## add new mac to db ###############
    # mySvModule.updateDb(url, path, '0/mac','3','123')

    ########## delete specific mac from db #####

    # mySvModule.deleteDb(url,f"{path}/0/mac",'3')

    ####### testing #########
# test2()
# test()

'''             
###################### test() output on window and pi4 ##################### 
output:
Read from firebase
found 0xfc,0x1d,0x43,0x31,0x94,0xc5 in ['0xe6,0xbc,0x50,0xb3,0x29,0xc6', '0x12,0xa9,0x67,0x05,0xb6,0xf9', '0xfc,0x1d,0x43,0x31,0x94,0xc5']
checked 415_uname
execution time 0.866708 sec

Read from json
Found 0xfc,0x1d,0x43,0x31,0x94,0xc5 in ['0xe6,0xbc,0x50,0xb3,0x29,0xc6', '0x12,0xa9,0x67,0x05,0xb6,0xf9', '0xfc,0x1d,0x43,0x31,0x94,0xc5']
checked 415_uname
execution time 0.001995 sec

diff read time between local and server : 0.864713 sec

################# test2() output ###################
output:

updated
 0xe6,0xbc,0x50,0xb3,0x29,0xc6
updated
 0x12,0xa9,0x67,0x05,0xb6,0xf9
updated
 0xfc,0x1d,0x43,0x31,0x94,0xc5

'''
###############################################################################################################################################################
##################################################### Find mac in json file ###################################
import mySvModule, time, json

d = mySvModule.readJs("new.json")

print(d) # print all in json
found_mac = "0x12,0xa9,0x67,0x05,0xb6,0xf9" #assume found this addr


for c in range(1,3):
    for i in d[f"user{c}"]["mac"]: 
        if(found_mac in i):
            print(f"Found {found_mac} in user{c}")

'''
output 

{'user1': {'email': '6110110415@gmail.com', 'faceId': '415_faceId', 'mac': ['0xe6,0xbc,0x50,0xb3,0x29,0xc6', '0x12,0xa9,0x67,0x05,0xb6,0xf9', '0xfc,0x1d,0x43,0x31,0x94,0xc5'], 'timeStamp': ['18/12/2021 10:27', '24/12/2021 09:56'], 'uname': 'uname1'}, 'user2': {'email': '6110110044@gmail.com', 'faceId': '044_faceId', 'mac': ['0xe6,0xbc,0x50,0x29,0xc6,0xb3', '0x12,0xa9,0x67,0x05,,0xf9,0xb6', '0xfc,0x1d,0xc5,0x43,0x31,0x94'], 'timeStamp': ['18/12/2021 10:27', None, '24/12/2021 09:57'], 'uname': 'uname2'}}
Found 0x12,0xa9,0x67,0x05,0xb6,0xf9 in user1
'''


