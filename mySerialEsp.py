import serial
import time

def getQ():
  device = serial.Serial(port='/dev/ttyUSB0', baudrate = 9600, timeout =.1)
  queue =[]*5
  
  def write_read():
    time.sleep(0.5)
    data = device.readline()
    return data
  while True:
    value = write_read()
    queue.append((value.decode("utf-8").strip()))
    print(queue[-3:])
    print('current queue is' + str(newQ[-1]))
