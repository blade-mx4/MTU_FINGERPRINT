#pragma once // <-- To prevent duplicate def 
/* 
Declearation For All the Function From Each Folder 

Always make sure the functions decelared here and in the function.ino match 
And the params most match too
*/

#ifndef FUNCTION_H 
#define FUNCTION_H  
#include<Arduino.h> 

// ================= Wifi Functions ==================== //
//extern const char *ip ; // callable varibale for c++ 
//extern const char port ;

//template<typename T> 

namespace Udp { // Just flex some oop here 
      // auto bind(auto IP) ;
      void wifi_udp_info(const char *ip ,const char *name , int port );
      bool init(const char * name , const char *pwd) ;
      void udp_send(String input) ;
}

// ================== img -> udp ===================== //

#endif 