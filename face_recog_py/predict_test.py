import cv2
import numpy as np 
from PIL import Image

#Create haar cascade
face_casc = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyes_casc = cv2.CascadeClassifier("haarcascade_eye.xml")

#training create dataset
def create_dataset(img,id,img_id):
    cv2.imwrite("data/pic."+str(id)+"."+str(img_id)+".jpg",img)

#create draw boundary in vdo
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, clf):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray,scaleFactor,minNeighbors,minSize=(30, 30))
    coords = []

    for (x,y,w,h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        id, conf = clf.predict(gray[y:y+h, x:x+w]) # _ -> confident value

        if id==1 and conf>=20 and conf <=80:  # 10-80%
            cv2.putText(img,"Phonie",(x,y-4), cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)
        else:
            cv2.putText(img,"Unknown",(x,y-4), cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)

        if conf < 100:
            conf = " {0}%".format(round(100 - conf))
        else:
            conf = " {0}%".format(round(100 - conf))
        print(str(conf))

        coords = [x,y,w,h]
    return img, coords

#create detect function draw by cascade file
def detect(img, face_casc, img_id, clf):
    img, coords = draw_boundary(img, face_casc, 1.1, 10, (0,0,255),clf)
    #img, coords = draw_boundary(img, eyes_casc,1.1,10,(255,0,0), "Eyes")
    id = 1
    if len(coords) == 4:    #check all x y w h-> detect face
        id=1  
        result = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]   #set y+=h, x+=w
        #create_dataset(result, id, img_id ) #for train
    return img

#opening vdo set w,h = 640x480
img_id = 0
cap = cv2.VideoCapture(0)  
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("model/job.xml")      #read file from tained file

while(True):
    ret, frame = cap.read()
    frame = detect(frame, face_casc, img_id, clf)
    cv2.imshow('frame', frame)
    img_id+=1

    if cv2.waitKey(10) & 0xFF == 27:        #press Esc = quit
        break

  #check vdo fps
fps = cap.get(cv2.CAP_PROP_FPS)
print("Fps using cap.get(cv2.CAP_PROP_FPS:{0}".format(fps))
    
    
cap.release()
cv2.destroyAllWindows()

