/*
I noticed packet where dropping during stream so tcp should go 
*/

#include <WiFi.h>
#include<HardwareSerial.h>
#include <NetworkUdp.h>
#include <fpm.h> 


HardwareSerial finger_serial(2) ;
FPM finger(&finger_serial) ;
  

// ============================================== //

void setup(){
  Serial.begin(115200) ; 
  finger_serial.begin(57600, SERIAL_8N1, RX_PIN, TX_PIN) ;
  WiFi.mode(WIFI_STA) ; 
  WiFi.begin(networkName ,networkPswd);
   
  if (!finger.begin() && WiFi.waitForConnectResult() != WL_CONNECTED ){
    Serial.println( "Sensor Not Connected OR WIFI ERROR ") ; 
    while (1){ yield(); }
  }
  Serial.println("Shit Went Down Well " ) ; 
  
}

void loop (){
//  imageToUdp() ;
//  while(1){ yield(); }
//  delay(2000);
}
