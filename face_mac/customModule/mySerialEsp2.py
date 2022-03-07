import serial, time, collections

portName = '/dev/ttyUSB0'
# portName = 'COM5'
max_size = 5
queue = collections.deque([]*max_size, maxlen=max_size)
device = None

def portAvailalbe():
    try:
        global device
        device = serial.Serial(port=portName, baudrate=9600, timeout=.1)
        return True
    except:
        return False

def getQ():
    if len(queue) > 0:
        return queue[0]
    else:
        return "null"

def runQ():
    while True:
        data = device.readline()
        data = data.decode('utf-8').strip() #decode from binary to int
        if(data != b'' or data != ""):
            queue.append(data) 
            print(f"data : {data}")
            #print(queue[0])
            #return queue[0]
        #else:
            #return "null"
        time.sleep(0.2)

def test_run():
    portAvailalbe()
    while True:
        runQ()
        
#test_run()


