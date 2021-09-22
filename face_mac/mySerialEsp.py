import serial, time

#def startEsp():
device = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
queue = []*3 # queue 3

def runQ():
    time.sleep(0.5)
    data = device.readline()
    queue.append((data.decode('utf-8').strip())) #decode from binary to int
    newQ = list(dict.fromkeys(queue[-3:]))  #create queue not fill same number
    print('Queue list : ' + str(queue[-3:])) #print lastest detected num
    #print('current queue is '+ newQ[-1])
    return newQ[-1] #return lastest number in queue
