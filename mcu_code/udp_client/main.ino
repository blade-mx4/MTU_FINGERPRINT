#include "wifi_udp_function.h" // kind of looks sexxy 

// =============== Config and Global Param ================= // 

const char * network_name = "Blade_net" ;  
const char * pwd = "upperechelon" ;

const char * ip = "192.168.0.102" ;
const int port = 8080 ;



void setup() {
  Serial.begin(115200) ;
  wifi :: wifi_udp_info(ip , network_name ,port ) ; 
  wifi :: init(network_name , pwd) ;
}


void loop() {

}