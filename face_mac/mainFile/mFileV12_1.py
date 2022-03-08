import numpy as np
import cv2, face_recognition, os, PIL
from datetime import datetime
import mySerialEsp2, time, threading
import concurrent.futures
import mySvModule
import time

path = 'ImagesAttendance/faces'

images = []
classNames = []
faceList = []
markedNameList = []
markedTimeList = []
mac_list = []

mySvModule.downloadJson()
db = mySvModule.readJs("userdata.json")
mySvModule.dl_img(path)
uKey_list = mySvModule.get_user_key(db)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def importImages():
    print("Importing Images...\nFace List:")
    faceList = os.listdir(path)
    print(faceList)
    
    for cl in faceList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        # print(classNames)
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
        np.savez_compressed('endcodeList.npz', data = encodeList)
        print(f'Processing " + "{round((counter / len(images) * 100), 2):.2f} %')
    print("Finished Encoding Images.")
    #return encodeList


encodeListKnown = []


def initialized():
    error_msg = "Error: "
    isError = False
    # check Webcam
    if not cap.isOpened():
        error_msg += " Cannot connect Webcam."
        isError = True
    # check SerialPort
    if not mySerialEsp2.portAvailalbe():
        error_msg += " Cannot connect SerialPort."
        isError = True
    if isError:
        print(error_msg)
        return False
    else:
        importImages()
        global encodeListKnown
        #encodeListKnown = findEncodings(images)
        try:
            encodedData = np.load('endcodeList.npz')
            encodeListKnown = encodedData['data']
            print("Finished Initializer.")
        except:
            findEncodings(images)
            print("call again")
            initialized()
        return True


def returnFunc(func):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(func)
        return future.result()


def current_timeStr():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M")


def hourminToInt(timeStr):
    hourmin_tmp = timeStr.split(' ')[1].split(':')
    hour_tmp = hourmin_tmp[0]
    min_tmp = hourmin_tmp[1]
    return int(hour_tmp[0] * 60 + min_tmp[1])



#def writeTimeStamp(name, mac):
def writeTimeStamp(name):
    # write time stamp
    # 'a+' mode create file if not exist, write at the end of file
    f = open('Attendance.csv', 'a+')
    dt_string = current_timeStr()
    #f.write(f'{name},{dt_string},{mac}\n')
    f.write(f'{name},{dt_string}\n')
    print(f'\nCheck {name} for new attendance.\n')
checkInterval = 1  # check interval () minute(s)        


#def markAttendance(name, mac, uKey):
def markAttendance(name, uKey):
    foundName = False
    for i in range(0, len(markedNameList)):
        if name == markedNameList[i]:
            # found name in markedNameList

            foundName = True
            markedTime = hourminToInt(markedTimeList[i])
            currentTime = hourminToInt(current_timeStr())

            if currentTime - markedTime >= checkInterval:

                mySvModule.timestamp(uKey)
                #writeTimeStamp(name, mac)
                writeTimeStamp(name)
                markedTimeList[i] = current_timeStr()
                break
            else:
                # not mark new attendance
                print(f'\nFound {name} . Not check for new attendance.\n')
    # Not found name in markedNameList
    # mark new attendance
    if foundName is False:
        mySvModule.timestamp(uKey)
        #writeTimeStamp(name, mac)
        writeTimeStamp(name)
        markedNameList.append(name)
        markedTimeList.append(current_timeStr())


def webcam_disp():
    while True:
        sucess, frame = cap.read()

        # time interface
        cv2.putText(frame, current_timeStr(), (10, 50), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(10) & 0xFF == 27:  # press Esc = quit
            break
        time.sleep(frame_delay)
    cap.release()
    cv2.destroyAllWindows()
    print("\nClosing Program.")
    os._exit(0)


# face-recognition preset
font = cv2.FONT_HERSHEY_SIMPLEX
process_delay = 0.25  # delay 250 millisecond
frame_rate = 24
frame_delay = 1 / frame_rate


def sliceStr(s):
    if s != "null":
        pos = s.find("_")
        uID = s[:pos]
        macID = s[pos+1:]
        #print(uID, macID)
        return uID, macID
    else:
        return 0, 0

def face_recog():
    userMac_around = []
    while True:
#       print("Face Recognition Processing...")
        sucess, img = cap.read()
        while not sucess:
            time.sleep(frame_delay)
            sucess, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        # time interface
        cv2.putText(img, current_timeStr(), (10, 50), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        #qReturned = returnFunc(mySerialEsp2.runQ)
        qReturned = mySerialEsp2.getQ()
        if(qReturned != ''):
            
            for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame):
                #start_time = time.time()
                uID, mac_found = sliceStr(qReturned)
                new_encL = []
                
                new_encL.append(encodeListKnown[int(uID)])
                print(f"uID {uID}")
                #matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                #print(f"most similar {matchIndex}")
                #print(f"faceDis {faceDis}")
                #end_time = time.time()
                #proc_time = end_time - start_time
                #print(f"proc_time : {proc_time}")
                #qReturned = returnFunc(mySerialEsp2.runQ)
                
                userKey = mySvModule.getDictKey(uKey_list, int(uID))
                #userMac_around.append(uID)
                
                #print(f" mac {mac_found}")
                #userMac_around = list(dict.fromkeys(userMac_around))
                
                #print(f"current face {matchIndex}")
                valid_user = False
                #print(f"facedis value : {faceDis[matchIndex]}")
                #print(f"current face {matchIndex}")
                #print(f"userMac_around {userMac_around}")
                if faceDis[matchIndex] < 0.33:
                    print("hello still alive")
                    name = db[userKey]["username"]
                    #mac = db[userKey]["macAddress"][f"device{mac_found}"]
                    valid_user = True


                else:
                    name = 'Unknown'
                    valid_user = False
                # draw put name and rectangle on face detected
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), font, 1, (255, 255, 255), 2)
                # save time stamp image
                if valid_user is True:
                    #print(f"userKey: {userKey} type {type(userKey)}")
                    #markAttendance(name, mac, userKey)
                    markAttendance(name, userKey)
                    cv2.imwrite('RecordImages/' + name + '.png', img)
                    mySvModule.uploadImg(f"images/{userKey}/timestamp",f"{name}.png",f"RecordImages/{name}.png")
        
        time.sleep(process_delay)



if __name__ == "__main__":
    # check environment

    if not initialized():
        print("Exit Program due to connection fail.")
        os._exit(0)
    # set thread
    WebcamThread = threading.Thread(target=webcam_disp)
    FaceRecThread = threading.Thread(target=face_recog)
    QueueThread = threading.Thread(target=mySerialEsp2.runQ)
    # start thread
    WebcamThread.start()
    FaceRecThread.start()
    QueueThread.start()

