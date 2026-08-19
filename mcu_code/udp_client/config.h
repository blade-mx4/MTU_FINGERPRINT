/* 
Always make sure the functions decelared here and in the function.ino match 
And the params most match too
*/

#ifndef FUNCTION_H 
#define FUNCTION_H  
#include<Arduino.h> 

// ================= Wifi Functions ==================== //
namespace wifi { // didnt want to use class and also didnt want to use function 
                //Result of my compromise 

      void wifi_udp_info(const char *ip ,const char *name , int port );
      bool init(const char * name , const char *pwd) ;
      void udp_send(String input) ;c:\Users\blade_mx4\Documents\code\MTU-FINGERPRINT\mcu_code\udp_client\function.ino

}

// ================== img -> udp ===================== //

#endif 