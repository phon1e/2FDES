import urllib.request
import os

def connect(host='https://firebase.google.com/'):
    try:
        urllib.request.urlopen(host)
        print("connected to the internet")
        return True
    except:
        return False



def print_txt(s):
  print("="*30)
  print(f"\n {s}\n")
  print("="*30)


def main():
	main_dir = "/home/pi/Desktop/2fdes"
	sub_dir = "/home/pi/Desktop/mkspiffs/mkspiffs-0.2.3-7-gf248296-arduino-esp8266-"

	os.chdir(main_dir)
	print_txt("LOADING AND MAPPING MAC ...")

	os.system("python mapping_mac.py")
	os.system('''./mkspiffs -b 0x1000 -p 0x100 -s 0x00200000 -d 5 --create ./data spiffs.bin
	''')
	os.system('''esptool.py --baud 921600 --port /dev/ttyUSB0 write_flash 0x00200000 ./spiffs.bin -u
	''')

	os.chdir(sub_dir)
	print_txt("UPLOADING DATA TO ESP8266. . . ")
	os.chdir(main_dir)

	print_txt(" STARTING THE MAIN SYSTEM. . .")
	os.system("python mFileV12_1.py")


if (connect()):
	main()
