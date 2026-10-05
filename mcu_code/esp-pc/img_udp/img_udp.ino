/*
I noticed packet where dropping during stream so tcp should go 
*/

#include <WiFi.h>
#include<HardwareSerial.h>
#include <NetworkUdp.h>
#include <fpm.h> 

//================== Configs ======================// 
#define PRINTF_BUF_SZ   60
char printfBuf[PRINTF_BUF_SZ];
#define RX_PIN 16
#define TX_PIN 17

const char *networkName = "ABADdon";
const char *networkPswd = "blazeday";
const char *udpServerIp = "192.168.0.101";
const int udpServerPort = 4000;
NetworkUDP udp;

HardwareSerial finger_serial(2) ;
FPM finger(&finger_serial) ;
  

// ============================================== //

void setup(){
  Serial.begin(115200) ; 
  finger_serial.begin(57600, SERIAL_8N1, RX_PIN, TX_PIN) ;
  WiFi.mode(WIFI_STA) ; 
  WiFi.begin(networkName ,networkPswd);
   
  if (!finger.begin() && WiFi.waitForConnectResult() != WL_CONNECTED ){
    Serial.println( "Sensor Not Connected OR WIFI ERROR ") ; 
    while (1){ yield(); }
  }
  Serial.println("Shit Went Down Well " ) ; 
  
}

void loop (){
  imageToUdp() ;
//  while(1){ yield(); }
  delay(2000);
}


void wifi_status(){
  
}



uint32_t imageToUdp(void)
{
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
        udp.beginPacket(udpServerIp, udpServerPort);
        
        bool ret = finger.readDataPacket(NULL, &udp, &readLen, &readComplete);
        
        if (!ret)
        {
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
