/* 
Always make sure the functions decelared here and in the function.ino match 

*/


#ifndef FUNCTION_H 
#define FUNCTION_H  
#include<Arduino.h> 

namespace wifi {
      bool init(const char * name , const char *pwd) ;
      void udp_send(String input) ;



}





#endif 