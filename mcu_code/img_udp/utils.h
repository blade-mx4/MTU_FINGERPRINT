#include <WiFi.h>
#include<HardwareSerial.h>
#include <NetworkUdp.h>
#include <fpm.h> 

NetworkUDP udp ;

//================== Configs ======================// 

#define PRINTF_BUF_SZ   60
char printfBuf[PRINTF_BUF_SZ];
#define RX_PIN 16
#define TX_PIN 17


const char *networkName = "ABADdon";
const char *networkPswd = "blazeday";
// const char *udpServerIp = "192.168.0.101";
const char * IP [] = {"192.168.0.100" ,"192.168.0.101", "192.168.0.102"} ;
const int udpServerPort = 4000;

const char *ip_check(){
    
    for (const char *ip : IP){
        udp.beginPacket(ip,port) ;
        if (udp.available() !=0 ){
            return ip ;
        }
        else{
            Serial.println(".") ;
        }
    }

    udp.end() ;

}





uint32_t imageToUdp(const char *IP , int PORT ){
    FPMStatus status;
    
    /* Take a snapshot of the finger */
    Serial.println("\r\nPlace a finger.");
    
    do {
        status = finger.getImage();
        
        switch (status) 
        {
            case FPMStatus::OK:
                Serial.println("Image taken.");
                break;
                
            case FPMStatus::NOFINGER:
                Serial.println(".");
                break;
                
            default:
                /* allow retries even when an error happens */
                snprintf(printfBuf, PRINTF_BUF_SZ, "getImage(): error 0x%X", static_cast<uint16_t>(status));
                Serial.println(printfBuf);
                break;
        }
        
        yield();
    }
    while (status != FPMStatus::OK);
    
    /* Initiate the image transfer */
    status = finger.downloadImage();
    
    switch (status) 
    {
        case FPMStatus::OK:
            Serial.println("Starting image stream...");
            break;
            
        default:
            snprintf(printfBuf, PRINTF_BUF_SZ, "downloadImage(): error 0x%X", static_cast<uint16_t>(status));
            Serial.println(printfBuf);
            return 0;
    }
    
    uint32_t totalRead = 0;
    uint16_t readLen = 0;
    
    /* Now, the sensor will send us the image from its image buffer, one packet at a time. */
    bool readComplete = false;

    while (!readComplete) 
    {
        /* Start composing a packet to the remote server */
        udp.beginPacket(IP,PORT); // <-- receives from the function
        
        bool ret = finger.readDataPacket(NULL, &udp, &readLen, &readComplete);
        
        if (!ret){

            snprintf_P(printfBuf, PRINTF_BUF_SZ, PSTR("readDataPacket(): failed after reading %u bytes"), totalRead);
            Serial.println(printfBuf);
            return 0;
        }
        
        /* Complete the packet and send it */
        if (!udp.endPacket())
        {
            snprintf_P(printfBuf, PRINTF_BUF_SZ, PSTR("imageToUdp(): failed to send packet, count = %u bytes"), totalRead);
            Serial.println(printfBuf);
            return 0;
        }
        
        totalRead += readLen;
        
        yield();
    }

    Serial.println();
    Serial.print(totalRead); Serial.println(" bytes transferred.");
    return totalRead;
}
