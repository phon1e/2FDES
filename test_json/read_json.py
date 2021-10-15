import json

faceId_list = []    

with open('data.json') as json_file:
    data = json.load(json_file)

for i in range(1,3):

	faceId_list.append((data["users"][str(i)][0]["mac"]))

print(faceId_list)
