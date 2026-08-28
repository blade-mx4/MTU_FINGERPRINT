#include "config.h"
/*
PS  : 
    The id is sent first to the so it cn be used to find the img 
    and the img later 
    So the pyseide has to read the id first before the img captue is init at this point 

*/

void setup () {
    Serial.begin(115200) ;
    info() ; // check if sensor is connected 
}


void loop() {

    Serial.print(" Input ID : ") ;
    while (Serial.available() == 0 ) { ; } // existential loop  
    
    int id = Serial.readStringUntil('\n').toInt() ;
    Serial.print(id) ;
    getimg() ;
    while (true){ yield(); } // pause the code for testing sake 
}


/*
Basically user input the id from serial console {pyserial} 
then the model prints {Godman}


*/