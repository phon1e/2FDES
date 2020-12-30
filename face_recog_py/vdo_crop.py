import cv2

#Create haar cascade
face_casc = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyes_casc = cv2.CascadeClassifier("haarcascade_eye.xml")

#create draw boundary in vdo
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray,scaleFactor,minNeighbors,minSize=(30, 30))
    coords = []

    for (x,y,w,h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img,text,(x,y-4), cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)
        coords = [x,y,w,h]
    return img, coords

#create detect function draw by cascade file
def detect(img, face_casc, eyes_casc):
    img, coords = draw_boundary(img, face_casc, 1.1, 10, (0,0,255),"Face")
    img, coords = draw_boundary(img, eyes_casc,1.1,10,(255,0,0), "Eyes")
    return img

#opening vdo set w,h = 640x480
cap = cv2.VideoCapture("vdo1.mp4")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while(True):
    ret, frame = cap.read()
    frame = detect(frame, face_casc, eyes_casc)
    cv2.imshow('frame', frame)

    if cv2.waitKey(10) & 0xFF == 27:        #press Esc = quit
        break
#check vdo fps
if True:
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Fps using cap.get(cv2.CAP_PROP_FPS:{0}".format(fps))
    
cap.release()
cv2.destroyAllWindows()

