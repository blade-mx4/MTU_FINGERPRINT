/* 
Always make sure the functions decelared here and in the function.ino match 
And the params most match too
*/

#ifndef FUNCTION_H 
#define FUNCTION_H  
#include<Arduino.h> 

namespace wifi {
      void wifi_udp_info(const char *ip ,const char *name , int port );
      bool init(const char * name , const char *pwd) ;
      void udp_send(String input) ;

}
#endif 