import mySvModule


url = 'https://sendfrompytest-default-rtdb.firebaseio.com/'
key = '-MqHz5m_algE-XHj4WXM'
path = f'/dbUser/{key}/users'


d = mySvModule.readDb(url,path)

i = 0
ids = '4444444443'
print("Read from firebase")

for i in range(3):
    if ids in d[i]['mac']:
          print(f'found {ids} in {d[i]["mac"]}')
          print(f'checked {d[i]["username"]}')

# output
# found 4444444443 in ['0000000001', '4444444443', '4444444445']
# checked 044_uname

db = mySvModule.readJs("data.json")
print("\nRead from json")
for i in range(3):
    if ids in db['users'][str(i)]['mac']:
        print(f'Found {ids} in { db["users"][str(i)]["mac"]}' )
        print(f'checked {db["users"][str(i)]["username"]}')

#output
#Read from json
#Found 4444444443 in ['0000000001', '4444444443', '4444444445']
#checked 044_uname
