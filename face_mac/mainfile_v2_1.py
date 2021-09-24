#v2_1

import numpy as np
import cv2, face_recognition, os, PIL
from datetime import datetime
import mySerialEsp, time, threading
import concurrent.futures

path = 'ImagesAttendance/faces'
images = []
classNames = []
myList = os.listdir(path)

def current_timeStr():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M")

frame_rate = 30
frame_delay = 1/frame_rate

def useQ():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(mySerialEsp.runQ)
        val = future.result()
        return str(val)
    
def findEncodings(images):
    encodeList = []
    
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
    
def markAttendance(name):
    with open('Attendance.csv', 'r') as f:
        data = f.readline().split(',')
        data_count = data[1]
    with open('Attendance.csv', 'a') as f:
        dt_string = current_timeStr()
        f.write(f'{name},{dt_string}\n')

        

def webcam_disp():
    
    if not cap.isOpened():
        raise IOError("Error: Cannot open Webcam.")
    
    while 1:
        sucess, frame = cap.read()
        
        #time interface
        cv2.putText(frame, current_timeStr(),(10,50), font,1, (0,255,255), 2, cv2.LINE_AA)

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(10) & 0xFF == 27:    #press Esc = quit
            break
        time.sleep(frame_delay)
    cap.release()
    cv2.destroyAllWindows()

#face-recognition preset
font = cv2.FONT_HERSHEY_SIMPLEX
process_delay = 0.25 #delay 250 millisecond

def face_recog():
    
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        #print(classNames)
        
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')
    
    counter = 1
    while 1:
        #print("From face_recog processing...\n" + str(counter))
        if not cap.isOpened():
            print("Error: Webcam is not Opened!")
            break
        sucess, img = cap.read()
        imgS = cv2.resize(img,(0, 0), None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        #time interface
        cv2.putText(img, current_timeStr(),(10,50), font,1, (0,255,255), 2, cv2.LINE_AA)
        
        faceCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        
        for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            
            print('mac founed is :' + useQ() + ' index founded is : '+ str(matchIndex))
            
            #compare between index of mac and index of picture
            #same? recog+timestamp: unknown
            valid_user = False
            if faceDis[matchIndex]< 0.50 and str(matchIndex) == str(useQ()):
                name = classNames[matchIndex].upper()
                #markAttendance(name) #delete comment when use timestamp
                valid_user = True
                print('\ncheck '+ name +' done.')

            else: name = 'Unknown'
            
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
 
            cv2.rectangle(img, (x1,y1),(x2,y2), (0,255,0), 2)
            cv2.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), font,1,(255,255,255),2)
            
        cv2.imshow('Webcam', img)
        
        if cv2.waitKey(10) & 0xFF == 27:        #press Esc = quit
            break
        time.sleep(frame_delay)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cap = cv2.VideoCapture(0) 
    t1 = threading.Thread(target = webcam_disp)
    t2 = threading.Thread(target = face_recog)
    t3 = threading.Thread(target = mySerialEsp.runQ)
    #start thread
    t1.start()
    t2.start()
    t3.start()
    
