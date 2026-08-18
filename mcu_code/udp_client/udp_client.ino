#include "header.h"

// =============== Config and Global Param ================= // 

const char * network_name = "Blade_net" ;  
const char * pwd = "upperechelon" ;

const char * ip = "192.168.0.100" ;
const int port = 8080 ;


void setup() {
  wifi :: init(network_name , pwd) ;
}


void loop() {

}