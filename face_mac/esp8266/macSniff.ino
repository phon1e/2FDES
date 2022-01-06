#include <iostream>
#include <fstream>
//#include<SPI.h>
//#include<SD.h>
#include "./esppl_functions.h"

//using namespace std;
/*
 * Define you friend's list size here
 */
#define LIST_SIZE 3
/*
 * This is your friend's MAC address list
 */
uint8_t friendmac[LIST_SIZE][ESPPL_MAC_LEN] = {
   {}//iphone 5GHz
  ,{}//iphone 2.4Ghz
  ,{}//ipad
  
  };
/*
 * This is your friend's name list
 * put them in the same order as the MAC addresses
 */
String friendname[LIST_SIZE] = {
   "wiroon's iphone 5GHz"
   ,"wiroon's iphone 2.4GHz"
  ,"wiroon's ipad "
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
  
  for (int i=0; i<LIST_SIZE; i++) {
    if (maccmp(info->sourceaddr, friendmac[i]) || maccmp(info->receiveraddr, friendmac[i])) {
   
      //Serial.printf("\n%s id is %d :)", friendname[i].c_str(), i);
      Serial.printf("\n%d", i);
      
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
