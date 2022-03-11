#include <iostream>
#include <fstream>
#include<iostream>
#include<iomanip>
#include<string>
#include "./esppl_functions.h"
#include <ESP8266WiFi.h>
#include <FS.h>

#define LIST_SIZE 5
/*
 * This is your friend's MAC address list
 */
uint8_t fmac[LIST_SIZE][ESPPL_MAC_LEN]; 
String fmap[LIST_SIZE];


uint8_t friendmac[LIST_SIZE][ESPPL_MAC_LEN] = {
   ////{0xd6,0xc6,0x8f,0x74,0x7e,0xeb} iphone 5 GHz
  //,{0xfc,0x1d,0x43,0x31,0x94,0xc5}//ipad
  
  {0x40,0x9c,0x28,0x5f,0x1b,0xc1}// iphone coewifi
  ,{0xfe,0xd5,0x9f,0xa1,0xc2,0x5a}//iphone 2.4 Ghz
  ,{0xb4,0x8b,0x19,0x78,0x40,0xb0}// saint
  ,{0x16,0x0D,0x66,0x74,0x40,0x20}//ipad home 2.4
  ,{0xf2,0x98,0xc6,0xb7,0x73,0x26}//ipad2 home 2.4
  
  };
/*
 * This is your friend's name list
 * put them in the same order as the MAC addresses
 */
String friendname[LIST_SIZE] = {
    "0_1"
   ,"0_2"
   ,"1_1"
   ,"1_2"
   ,"2_1"

  };
char ch; 

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
    //Serial.printf("%d \n", info->sourceaddr);
    //Serial.printf("%d \n", info->receiveraddr);

    if (maccmp(info->sourceaddr, friendmac[i]) || maccmp(info->receiveraddr, friendmac[i])) {
    
      Serial.printf(" \n%s ", friendname[i].c_str());
      //Serial.printf("\n%d", i);
      //sprintf(buffer,"%s",friendmac[i]);
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
  
  //Serial.setTimeout(1);
  //esppl_init(cb);
  
  File mac_ls = SPIFFS.open(mac, "r");
  File mapped_ls = SPIFFS.open(mapped, "r");
  Serial.println("reading mac.txt");
  for(int i=0; i < mac_ls.size();i++)
  {

    Serial.print((char)mac_ls.read());

  }
  mac_ls.close();
  
  Serial.println("reading mapped.txt");
  for(int i=0; i < mapped_ls.size();i++)
  {

    Serial.print((char)mapped_ls.read());

  }
  mapped_ls.close();
  
}

void loop() {
/* 
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
  */
}
