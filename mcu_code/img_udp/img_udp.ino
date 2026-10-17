#include "utils.h"

// ============================================== //

void setup(){
  Serial.begin(115200) ;
  finger_serial.begin(57600 , SERIAL_8N1 , RX_PIN , TX_PIN); 
  Serial.println("Starting") ;
  WiFi.mode(WIFI_STA)  ;
    if (!WiFi.begin(networkName ,networkPswd)){
    Serial.println("Not Connected  ");
    Serial.println("REtrying..........") ;
    
  }
  else if (!finger.begin()){
    Serial.println("Sensor Error ") ;
    Serial.println("REtrying..........") ;
//    setup() ;
  }

  Serial.println("Setup ops ok ") ; 
    
}


void loop (){
  imageToUdp(udpServerIp,Port) ;
  delay(2000) ;

}
