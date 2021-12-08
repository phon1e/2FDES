import mySvModule, time, json

start1 = time.time()

url = 'https://sendfrompytest-default-rtdb.firebaseio.com/'
key = '-MqHz5m_algE-XHj4WXM'
path = f'/dbUser/{key}/users'


d = mySvModule.readDb(url,path)
mySvModule.loadJs(d, 'new.json',5)

js = mySvModule.readJs('new.json')

i = 0
ids = '4444444443'
print("Read from firebase")


for i in range(3):
    if ids in d[i]['mac']:
          print(f'found {ids} in {d[i]["mac"]}')
          print(f'checked {d[i]["username"]}')
end1 = time.time()
diff1 = end1 - start1
print(f'execution time {diff1} sec' )

# output
# found 4444444443 in ['0000000001', '4444444443', '4444444445']
# checked 044_uname
start2 = time.time()

db = mySvModule.readJs("new.json")
print("\nRead from json")
for i in range(3):
    if ids in db[i]['mac']:
        print(f'Found {ids} in { db[i]["mac"]}' )
        print(f'checked {db[i]["username"]}')

end2 = time.time()
diff2 = end2 - start2
print(f'execution time {diff2} sec' )

print(f'\ndifference time between 2 method : {diff1 - diff2} sec')
# output
#     Found
#     4444444443 in ['0000000001', '4444444443', '4444444445']
#     044
#     _uname

#print(f'read from firebase db {d}')
#print(f'read from loaded file {js}')