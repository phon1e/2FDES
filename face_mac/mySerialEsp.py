import serial, time

#def startEsp():
device = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
queue = []*3 # queue 3

def runQ():
    time.sleep(0.5)
    data = device.readline()
    queue.append((data.decode('utf-8').strip()))
    newQ = list(dict.fromkeys(queue[-3:]))
    print('Queue list : ' + str(queue[-3:]))
    #print('current queue is '+ newQ[-1])
    return newQ[-1]
