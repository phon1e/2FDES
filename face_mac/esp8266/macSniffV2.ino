#include <string>
#include "./esppl_functions.h"
#include <ESP8266WiFi.h>
#include <FS.h>

#include "./macAddressMapper.h"
//#define LIST_SIZE 3
#define MAX_UID_SIZE 5

int usercount = 0;
//uint8_t userMAC[LIST_SIZE][ESPPL_MAC_LEN];
//String userId[LIST_SIZE];
uint8_t** userMAC;
char** userId;

void printUserMappedInfo() {
  for (int i = 0; i < usercount; i++) {
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
 
  for (int i=0; i<usercount; i++) {
    if (maccmp(info->sourceaddr, userMAC[i]) || maccmp(info->receiveraddr, userMAC[i])) {
      //Serial.printf("%s", userId[i].c_str());
      Serial.print(userId[i]);
      //Serial.printf("\n%d", i);
      //sprintf(buffer,"%s",userMAC[i]);
      //Serial.println(buffer);

    }
  }
}

const char* mac = "/mac.txt";
const char* mapped = "/mapped.txt";

void setup() {
  delay(1000);
  Serial.begin(115200);
  SPIFFS.begin();
  Serial.println();

  File linecnt_ls = SPIFFS.open(mac, "r");
  File mac_ls = SPIFFS.open(mac, "r");
  File mapped_ls = SPIFFS.open(mapped, "r");
  char bufferStr[24];
  int count = 0;
  int maccount = 0;
  int linecount = 0;
  // Count number of line in file
  for(int i = 0; i < linecnt_ls.size();i++)
  {
    char ch = (char)linecnt_ls.read();
    if (ch == '\n' || i+1 == linecnt_ls.size()) {
      linecount++;
    }
  }
  linecnt_ls.close();
  // Initialize User Information
  usercount = linecount;
  userMAC = (uint8_t**)malloc(sizeof(uint8_t*)*usercount);
  userId = (char**)malloc(sizeof(char*)*usercount);
  for(int i = 0; i < usercount; i++) {
    userMAC[i] = (uint8_t*)malloc(sizeof(uint8_t)*ESPPL_MAC_LEN);
    userId[i] = (char*)malloc(sizeof(char)*MAX_UID_SIZE);
  }
  // Read User MAC Address
  //Serial.println("reading mac.txt");
  for(int i = 0; i < mac_ls.size();i++)
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
  // Read User ID
  //Serial.println("reading mapped.txt");
  int idcount = 0;
  for(int i = 0; i < mapped_ls.size();i++)
  {
    char ch = (char)mapped_ls.read();
    bufferStr[count] = ch;
    count++;
    if (ch == '\n' || i+1 == mapped_ls.size()) {
      bufferStr[count] = '\0';
      //Serial.print(bufferStr);
      strcpy(userId[idcount], bufferStr);
      idcount++;
      strcpy(bufferStr, "");
      count = 0;
    }
  }
  mapped_ls.close();
//  Serial.println("---User Info---");
//  printUserMappedInfo();
//  Serial.println("---------------");
  
  Serial.setTimeout(1);
  esppl_init(cb);
}

String x;
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
