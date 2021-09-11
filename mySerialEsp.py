import serial, time, threading 

device = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
queue = []*5 #create list q size 5

def runQ():
  time.sleep(0.5)
  data = device.readline() #read line from serial monitor
  queue.append((data.decode('utf-8').strip())) #cut space and some byte format off 
  newQ = list(dict.fromkeys(queue[-3:]))  #remove same value in list and choose lastest 3 element 
  print('Queue list: ' + str(queue[-3:])) #print lastest 3 element in list 
  return newQ[-1] #return lastest 1 element in list 
