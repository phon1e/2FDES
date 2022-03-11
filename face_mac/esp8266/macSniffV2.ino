#include <string>
#include "./esppl_functions.h"
#include <ESP8266WiFi.h>
#include <FS.h>

#include "./macAddressMapper.h"
#define LIST_SIZE 3

uint8_t userMAC[LIST_SIZE][ESPPL_MAC_LEN];
String userId[LIST_SIZE];

void printUserMappedInfo() {
  for (int i = 0; i < LIST_SIZE; i++) {
    Serial.print("UserId : ");
    Serial.print(userId[i]);
    Serial.print("MAC Address: ");
    for (int j = 0; j < ESPPL_MAC_LEN; j++) {
      Serial.print(userMAC[i][j]);
      Serial.print(",");
    }
    Serial.print("\n");
  }
}

bool maccmp(uint8_t *mac1, uint8_t *mac2) {
  for (int i=0; i < ESPPL_MAC_LEN; i++) {
    if (mac1[i] != mac2[i]) {
      return false;
    }
  }
  return true;
}

void cb(esppl_frame_info *info) {
  char buffer[32];
 
  for (int i=0; i<LIST_SIZE; i++) {
    if (maccmp(info->sourceaddr, userMAC[i]) || maccmp(info->receiveraddr, userMAC[i])) {
      Serial.printf("%s", userId[i].c_str());
      //Serial.printf("\n%d", i);
      //sprintf(buffer,"%s",userMAC[i]);
      //Serial.println(buffer);

    }
  }
}

String x;
const char* mac = "/mac.txt";
const char* mapped = "/mapped.txt";

void setup() {
  delay(1000);
  Serial.begin(115200);
  SPIFFS.begin();
  Serial.println();
  
  File mac_ls = SPIFFS.open(mac, "r");
  File mapped_ls = SPIFFS.open(mapped, "r");
  //Serial.println("reading mac.txt");
  char bufferStr[24];
  int count = 0;
  int maccount = 0;
  for(int i=0; i < mac_ls.size();i++)
  {
    char ch = (char)mac_ls.read();
    bufferStr[count] = ch;
    count++;
    if (ch == '\n' || i+1 == mac_ls.size()) {
      bufferStr[count] = '\0';
      //Serial.print(bufferStr);
      uint8_t* mac = getMAC(bufferStr);
      int j;
      for (j = 0; j < ESPPL_MAC_LEN; j++) {
        userMAC[maccount][j] = mac[j];
      }
      maccount++;
      strcpy(bufferStr, "");
      count = 0;
    }
  }
  mac_ls.close();
  
  //Serial.println("reading mapped.txt");
  int idcount = 0;
  for(int i=0; i < mapped_ls.size();i++)
  {
    char ch = (char)mapped_ls.read();
    bufferStr[count] = ch;
    count++;
    if (ch == '\n' || i+1 == mapped_ls.size()) {
      bufferStr[count] = '\0';
      //Serial.print(bufferStr);
      userId[idcount] = bufferStr;
      idcount++;
      strcpy(bufferStr, "");
      count = 0;
    }
  }
  mapped_ls.close();
  //Serial.println("---User Info---");
  //printUserMappedInfo();
  //Serial.println("---------------");
  
  Serial.setTimeout(1);
  esppl_init(cb);
}

void loop() {
 
  esppl_sniffing_start();
  while (true) {
    for (int i = ESPPL_CHANNEL_MIN; i <= ESPPL_CHANNEL_MAX; i++ ) {
      esppl_set_channel(i);
      while (esppl_process_frames()) {
        //
      }
    }
  }
  while(!Serial.available());
  x = Serial.readString();
  Serial.print(x);
  
}
