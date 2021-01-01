import cv2, os
import numpy as np 
from PIL import Image

def train_classifier(data_dir):
	path = [os.path.join (data_dir, f) for f in os.listdir(data_dir)]
	faces=[]
	ids =[]

	for image in path:
		img = Image.open(image).convert("L")	#L-> gray scale
		imageNp = np.array(img, 'uint8')	#grayscale unsignedInt 8bit 0-255
		id=int(os.path.split(image)[1].split(".")[1])	#split id trained 
		faces.append(imageNp)	#add trained in faces 
		ids.append(id)	#add trained id

	ids = np.array(ids)

	clf = cv2.face.LBPHFaceRecognizer_create()
	clf.train(faces, ids)
	clf.write("job.xml")

train_classifier("dataset")
