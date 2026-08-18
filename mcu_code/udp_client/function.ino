/*
Custom Function For Wifi and udp Server
And to reduce over head like using .BeginPacket and endPacket just to 
send to the server 


*/

#include<WiFi.h> 
#include<NetworkUdp.h> 

NetworkUDP udp ; 


namespace wifi {
      bool init (const char *name , const char *pwd) {
        WiFi.mode(WIFI_STA) ;
        WiFi.begin(name , pwd) ;
        Serial.begin(115200) ;
        while (true) {
          
          if (WiFi.waitForConnectResult() != WL_CONNECTED ){
            Serial.println("Connection Error") ;
            delay(2000);
            return false ;
          }
          else {
            Serial.println("Connected") ;
            return true ;
            break ;
          }


        }
      }
      void udp_send(String input ){
        udp.beginPacket(ip ,port) ;
        udp.print(input) ; Serial.println("Transmitting Packet ....."); // <-- For Debug 
        udp.endPacket() ; 
      }
}


