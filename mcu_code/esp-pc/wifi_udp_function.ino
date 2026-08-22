/*
Custom Function For Wifi and udp Server
And to reduce over head like using .BeginPacket and endPacket just to 
send to the server 
*/

#include<WiFi.h> 
#include<NetworkUdp.h> 

using namespace std  ;

NetworkUDP udpClient ; 

namespace Udp {

    void wifi_udp_info(const char *ip ,const char *name , int port ) { //To print wifi and up info to help in debuggin
      Serial.print("================ WIFI INFO ======================== ") ;
      Serial.print("WIFI Name : ") ; Serial.print(name) ;
      Serial.print("Server IP: ") ;  Serial.print(ip) ;
      Serial.print("Server Port : ") ; Serial.print(port) ;
    }
    
    bool init (const char *name , const char *pwd) {  // Checking if Connected  not yet implemeted the loop to keep tryin 
      WiFi.mode(WIFI_STA) ;
      WiFi.begin(name , pwd) ;
      Serial.begin(115200) ;
      
      while (WiFi.waitForConnectResult() != WL_CONNECTED ){ // Checking for if connected 
        Serial.println("Connection Error") ;
        delay(2000);
        return false ;
      }
        Serial.println("Connected") ;
        return true ; 
    }
    
    void udp_send(String input ){
      udpClient.beginPacket(ip ,port) ;
      udpClient.print(input) ; Serial.println("Transmitting Packet ....."); // <-- For Debug 
      udpClient.endPacket() ; 
    }

} 


