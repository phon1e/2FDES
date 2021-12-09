import mySvModule, time, json

url = 'https://sendfrompytest-default-rtdb.firebaseio.com/'
key = '-MqHz5m_algE-XHj4WXM'
path = f'/dbUser/{key}/users'

def test():
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

# update mac to db
def test2():
    c = 0
    mac_list = {'0': '0xe6,0xbc,0x50,0xb3,0x29,0xc6',
                '1': '0x12,0xa9,0x67,0x05,0xb6,0xf9',
                '2': '0xfc,0x1d,0x43,0x31,0x94,0xc5'}

    for i in mac_list.values():
        mySvModule.updateDb(url, path, '0/mac',str(c),str(i) )
        c+=1
test2()
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
