import serial, time, collections, threading

portName = '/dev/ttyUSB0'
# portName = 'COM5'
max_size = 5
#queue = collections.deque([]*max_size, maxlen=max_size)
queue = []
device = None
#lock = threading.Lock()

def portAvailalbe():
    try:
        global device
        device = serial.Serial(port=portName, baudrate=115200, timeout=.1)
        return True
    except:
        return False

def getQ():
    empty = []
    if len(queue) > 0:
        return queue;
    else:
        return empty;

def runQ():
    while True:
        data = device.readline()
        
        data = data.decode('utf-8').strip() #decode from binary to int
        #print(f"before add data {data}")
        if(data != b'' and data != "" and len(data) > 2):
            #lock.acquire()
            #print(f"after add data {data}")
            #queue.append(data)
            if len(queue) >= max_size:
                queue.pop(0)
            if len(queue) > 0:
                found = False
                for item in queue:
                    if item == data:
                        found = True
                        break
                if not found:
                    queue.append(data)
            else:
                queue.append(data)
            #rint(f"data : {data}")
            #print(queue[0])
            #return queue[0]
        #else:
            #return "null"
            #lock.release()
        #getQ()
        time.sleep(0.2)

def test_run():
    portAvailalbe()
    while True:
        runQ()
        
        
#test_run()



