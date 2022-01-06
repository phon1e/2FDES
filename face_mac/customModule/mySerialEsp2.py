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

def runQ():
    time.sleep(1)
    data = device.readline()
    queue.append((data.decode('utf-8').strip())) #decode from binary to int
    items = list(dict.fromkeys(queue))
    print(f'Queue list : {str(items)}')
    #print(f'returned {queue[0]}')
    return queue[0]

def test_run():
    portAvailalbe()
    while True:
        runQ()
   

#test_run()
