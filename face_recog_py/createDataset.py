import cv2
import numpy as np 
from PIL import Image

#Create haar cascade
face_casc = cv2.CascadeClassifier("cascade/haarcascade_frontalface_default.xml")
eyes_casc = cv2.CascadeClassifier("cascade/haarcascade_eye.xml")
vdo = ["vdo1.mp4", "vdo2.mp4"]
#training create dataset
def create_dataset(img,id,img_id):
    cv2.imwrite("dataset/pic."+str(id)+"."+str(img_id)+".jpg",img)

#create draw boundary in vdo
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray,scaleFactor,minNeighbors,minSize=(30, 30))
    coords = []

    for (x,y,w,h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img,"Jobs",(x,y-4), cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)
        coords = [x,y,w,h]
    return img, coords

#create detect function draw by cascade file
def detect(img, face_casc, img_id):
    img, coords = draw_boundary(img, face_casc, 1.1, 10, (0,0,255))
    if len(coords) == 4:    #check all x y w h-> detect face
        id=1  
        result = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]   #set y+=h, x+=w
        create_dataset(result, id, img_id ) #for train
    return img

#opening vdo set w,h = 640x480
img_id = 0
cap = cv2.VideoCapture(vdo[0])  
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while(True):
    ret, frame = cap.read()
    frame = detect(frame, face_casc, img_id)
    cv2.imshow('frame', frame)
    img_id+=1
    if cv2.waitKey(10) & 0xFF == 27:        #press Esc = quit
        break
    
cap.release()
cv2.destroyAllWindows()

