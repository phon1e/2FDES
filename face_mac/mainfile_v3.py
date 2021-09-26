#v3
import numpy as np
import cv2, face_recognition, os, PIL
from datetime import datetime
import mySerialEsp, time, threading
import concurrent.futures

path = 'ImagesAttendance/faces'
images = []
classNames = []
faceList = []
cap = cv2.VideoCapture(0)

def importImages():
    print("Importing Images...\nFace List:")
    faceList = os.listdir(path)
    print(faceList)
    for cl in faceList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        #print(classNames)
    print("Finished Import Images.")

def findEncodings(images):
    print("Start Encoding Images...")
    encodeList = []
    counter = 0
    for img in images:
        counter += 1
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        print("Processing "+"{:.2f}".format(round((counter/len(images)*100), 2))+"%")
    print("Finished Encoding Images.")
    return encodeList


encodeListKnown = []

def initialized():
    error_msg = "Error: "
    isError = False
    # check Webcam
    if not cap.isOpened():
        error_msg += " Cannot connect Webcam."
        isError = True
    # check SerialPort
    if not mySerialEsp.portAvailalbe():
        error_msg += " Cannot connect SerialPort."
        isError = True
    if isError:
        print(error_msg)
        return False
    else:
        importImages()
        global encodeListKnown
        encodeListKnown = findEncodings(images)
        print("Finished Initializer.")
        return True
    
def returnFunc(func):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(func)
        return future.result()

def current_timeStr():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M")

def markAttendance(name):
    # write time stamp
    # 'a+' mode create file if not exist, write at the end of file
    f = open('Attendance.csv', 'a+')
    dt_string = current_timeStr()
    f.write(f'{name},{dt_string}\n')
                    
def webcam_disp():
    while True:
        sucess, frame = cap.read()
        # time interface
        cv2.putText(frame, current_timeStr(),(10,50), font,1, (0,255,255), 2, cv2.LINE_AA)

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(10) & 0xFF == 27:    # press Esc = quit
            break
        time.sleep(frame_delay)
    cap.release()
    cv2.destroyAllWindows()

# face-recognition preset
font = cv2.FONT_HERSHEY_SIMPLEX
process_delay = 0.25 # delay 250 millisecond
frame_rate = 30
frame_delay = 1/frame_rate

def face_recog():
    while True:
        print("Face Recognition Processing...")
        sucess, img = cap.read()
        imgS = cv2.resize(img,(0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        # time interface
        cv2.putText(img, current_timeStr(),(10,50), font,1, (0,255,255), 2, cv2.LINE_AA)
        
        faceCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        
        for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            mac_found = returnFunc(mySerialEsp.runQ)
            print('mac founed is :' + mac_found + ' index founded is : '+ str(matchIndex))
            
            # compare between index of mac and index of picture
            # same? recog+timestamp: unknown
            valid_user = False
            if faceDis[matchIndex]< 0.50 and str(matchIndex) == mac_found:
                name = classNames[matchIndex].upper()
                markAttendance(name) #delete comment when use timestamp
                valid_user = True
                print('\ncheck '+ name +' done.')
            else: name = 'Unknown'
            # draw put name and rectangle on face detected
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1,y1),(x2,y2), (0,255,0), 2)
            cv2.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), font,1,(255,255,255),2)
            # save time stamp image
            if valid_user is True:
                cv2.imwrite('RecordImages/'+name+current_timeStr()+'.png', img)                
        time.sleep(process_delay)
        
if __name__ == "__main__":
    # check environment
    
    if not initialized():
        print("Exit Program due to connection fail.")
        os._exit(0)
    # set thread
    WebcamThread = threading.Thread(target = webcam_disp)
    FaceRecThread = threading.Thread(target = face_recog)
    QueueThread = threading.Thread(target = mySerialEsp.runQ)
    # start thread
    WebcamThread.start()
    FaceRecThread.start()
    QueueThread.start()
    
    # wait thread each done
    #t1.join()
    #t2.join()
    #t3.join()
  
