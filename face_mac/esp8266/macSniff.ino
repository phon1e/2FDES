#include <iostream>
#include <fstream>
#include<iostream>
#include<iomanip>
#include<string>
#include "./esppl_functions.h"

using namespace std;
/*
 * Define you friend's list size here
 */
#define LIST_SIZE 3
/*
 * This is your friend's MAC address list
 */
uint8_t friendmac[LIST_SIZE][ESPPL_MAC_LEN] = {
   {0xfa,0x6c,0xb6,0x92,0x9c,0x39}//iphone 2.4 GHz
  ,{0x66,0x38,0xf3,0xe9,0x08,0x99}//iphone 5 Ghz
  ,{0xfc,0x1d,0x43,0x31,0x94,0xc5}//ipad
  
  };
/*
 * This is your friend's name list
 * put them in the same order as the MAC addresses
 */
String friendname[LIST_SIZE] = {
    "1_1"
   ,"1_2"
   ,"2_1"
  };

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
    if (maccmp(info->sourceaddr, friendmac[i]) || maccmp(info->receiveraddr, friendmac[i])) {
    
      Serial.printf(" \n%s ", friendname[i].c_str());
      //Serial.printf("\n%d", i);
      //sprintf(buffer,"%s",friendmac[i]);
      //Serial.println(buffer);

    }
  }
}

String x;

void setup() {
  delay(1);
  Serial.begin(9600);
  
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
