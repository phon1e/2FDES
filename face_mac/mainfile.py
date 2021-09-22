import numpy as np
import cv2, face_recognition, os, PIL
from datetime import datetime
import mySerialEsp, time, threading #mySerialEsp ==>  mySerialEsp.py file 
import concurrent.futures



def getQ():
    while True:
        currQ = mySerialEsp.runQ()
        #print('current queue is  ' + str(currQ) +'\n ----------- \n')
        return currQ
        
def useQ():
    with concurrent.futures.ThreadPoolExecutor() as executor: #return mac index during while loop
        future = executor.submit(getQ)
        val = future.result()
        return str(val)
    
#path = 'ImagesAttendance/{file}'.format(file = currQ)
path = 'ImagesAttendance/faces' #อันนี้ใช้ภาพหน้าใส่ใน folder/faces ได้เลยไ่ต้องใช้ xml xmlนั้นอีกแบบนึง แบบนี้มันแม่นกว่าเลยใช้ไก่อน
images = []
classNames = []
myList = os.listdir(path)
print(myList)

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M")

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

def findEncodings(images):  #encode หน้าใช้ api ไม่ต้องใช้ xml
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        return encodeList
    
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f: #create aAttendance.csv
        myDataList = f.readlines()
        nameList = []
         
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            
            if name not in line:
                f.writelines(f'\n{name},{dt_string}') #time stamp
              
              
encodeListKnown = findEncodings(images)

print('Encoding Complete')

cap = cv2.VideoCapture(0)

def face_recog():
    while True:
        font = cv2.FONT_HERSHEY_SIMPLEX
        sucess, img = cap.read()
        imgS = cv2.resize(img,(0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        cv2.putText(img, dt_string,(10,50), font,1, (0,255,255), 2, cv2.LINE_AA)
        
        faceCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        
        
        for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
            
            if faceDis[matchIndex]< 0.50:
                name = classNames[matchIndex].upper()

                print('current found :' + useQ())
                if str(matchIndex) == useQ(): #compare pic index(instread xml) and mac index pim thai maidai
                    print("\n found match mac address ! \n")
                    markAttendance(name)  #pic index == mac index ==> timestamp
                else:
                    print("finding. . .\n")
                
            else: name = 'Unknown'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1,y1),(x2,y2), (0,255,0), 2)
            cv2.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), font,1,(255,255,255),2)
            
        
        cv2.imshow('Webcam', img)
        
        if cv2.waitKey(10) & 0xFF == 27:        #press Esc = quit
            break


if __name__ == "__main__":
    t1 = threading.Thread(target = face_recog)
    t2 = threading.Thread(target = getQ)
    #start thread
    t1.start()
    t2.start()
    #wait thread each done
    
    t1.join()
    t2.join()
  

