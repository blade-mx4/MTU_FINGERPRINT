#include<HardwareSerial.h>
#include<fpm.h> 

// ====================Configs and Global Param ===================== // 

#define RX 16 
#define TX 17 

HardwareSerial serial(2) ; 
FPM finger(&serial) ;

#define PRINTF_BUF_SZ   60
char printfBuf[PRINTF_BUF_SZ];

void info(void) {
    Serial.begin(115200) ;
    serial.begin(57600,SERIAL_8N1,RX,TX) ;
    if (finger.begin()) {
        Serial.print("Sensor Connected") ;
    }else{
        Serial.print("Sensor Disconnected") ;
        while(1) yield ;
    }

}

uint32_t get_img(void){ 
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

    /* Send some arbitrary signature to the PC, to indicate the start of the image stream */
    Serial.write(0xAA);
    
    uint32_t totalRead = 0;
    uint16_t readLen = 0;
    
    /* Now, the sensor will send us the image from its image buffer, one packet at a time.
     * We will stream it directly to Serial. */
    bool readComplete = false;

    while (!readComplete) 
    {
        bool ret = finger.readDataPacket(NULL, &Serial, &readLen, &readComplete);
        
        if (!ret)
        {
            snprintf_P(printfBuf, PRINTF_BUF_SZ, PSTR("readDataPacket(): failed after reading %u bytes"), totalRead);
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