import urllib.request
import os
import sys
import os.path, shutil, filecmp

sys.path.insert(1,'/home/pi/Desktop/2fdes/')

import mySvModule


src_mac = "/home/pi/Desktop/mkspiffs/mkspiffs-0.2.3-7-gf248296-arduino-esp8266-/data"
dst_mac = "/home/pi/Desktop/mkspiffs/mkspiffs-0.2.3-7-gf248296-arduino-esp8266-/tmp"

def wait_for_internet():
    mySvModule.print_txt("Waiting for internet connection. . .")
    while True:
        try:
            response = urllib.request.urlopen('https://firebase.google.com/', timeout = 1)
            print("connected")
            return
        except: 
            urllib.request.UnknownHandler
            pass


def main():

    main_dir = "/home/pi/Desktop/2fdes"
    sub_dir = "/home/pi/Desktop/mkspiffs/mkspiffs-0.2.3-7-gf248296-arduino-esp8266-"
        
    
    os.chdir(main_dir)
    mySvModule.print_txt("LOADING AND MAPPING MAC ...")
    os.system("python mapping_mac.py")
    
    mySvModule.print_txt("CHCEKING MAC DATA CHANGES...")
    
    if not mySvModule.is_same(src_mac, dst_mac):
        mySvModule.print_txt("FOUND MAC DATA CHANGES ...")
        os.chdir(sub_dir)
        mySvModule.print_txt("UPLOADING DATA TO ESP8266. . . ")
    
        os.system('''./mkspiffs -b 0x1000 -p 0x100 -s 0x00200000 -d 5 --create ./data spiffs.bin''')
        os.system('''esptool.py --baud 921600 --port /dev/ttyUSB0 write_flash 0x00200000 ./spiffs.bin -u''')
        mySvModule.copy_to(src_mac,dst_mac)
    mySvModule.print_txt("NO MAC DATA CHANGES ...")
    os.chdir(main_dir)
    
    mySvModule.print_txt(" STARTING THE MAIN SYSTEM. . .")
    os.system("python mFileV12_1.py")


wait_for_internet()
main()
