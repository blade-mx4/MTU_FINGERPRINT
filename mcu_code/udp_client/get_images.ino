#include<fpm.h>
#include<HardwareSerial.h> 

// ========================= Configs and Global Params ========================== //
#define RX_PIN 16 
#define TX_PIN 17

HardwareSerial serial(2) ; 
FPM finger(&serial) ; 

// --- Packet Header -- //  
#define byte 0xAA 
#define header 5 

#define print_buf_sz 80 
char printBuf[print_buf_sz] 


void write_header (uint16_t ID , uint16_t seq ) {
        uint8_t hdr[header] ; 
        hdr[0] = byte ;
        hdr[1] = (uint8_t)
}