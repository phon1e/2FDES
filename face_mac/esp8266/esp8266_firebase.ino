#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>


#define FIREBASE_HOST "***"
#define FIREBASE_AUTH "***"
#define WIFI_SSID "***"
#define WIFI_PASSWORD "***"

FirebaseData firebaseData;
FirebaseJson json;
void setup()
{
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while(WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);  
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.print(WiFi.localIP());
  Serial.println();
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
}

void loop()
{
 if (Firebase.getString(firebaseData, "/users/***/macAddress"))
 {
    Serial.println(firebaseData.stringData());
 }
 if(Firebase.getString(firebaseData, "/users/***/username"))
 {
  Serial.println(firebaseData.stringData());
 }
 else
 {
    Serial.println(firebaseData.errorReason());
  }
}
