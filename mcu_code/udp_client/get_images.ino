#include <fpm.h>
#include <WiFi.h>
#include <NetworkUdp.h>


// ======================= Configs and Global Param ============================== // 

#define SENSOR_RX_PIN 16
#define SENSOR_TX_PIN 17
HardwareSerial serial(2);

FPM finger(&serial);
FPMSystemParams params;

const char * ip = "192.168.0.102" ;
const int port = 8080 ;




/* --- Packet header --- */
#define MAGIC_BYTE   0xAA
#define HEADER_SZ    5   /* magic(1) + sessionId(2) + seq(2) */

/* for convenience */
#define PRINTF_BUF_SZ   80
char printfBuf[PRINTF_BUF_SZ];

NetworkUdp udpClient ;

void Finger_Status(){
  while (true) {
  if (finger.begin()){
    Serial.print("Sensor Connected ") ;
    break ;
    }
  else{
    Serial.print("Sensor Not Found") ;
    delay(2000) ;
    }
  
  }

}



/* Writes the 5-byte header (magic + sessionId + seq) into the
 * in-flight UDP packet, big-endian for the multi-byte fields. */
void writeHeader(uint16_t sessionId, uint16_t seq)
{
    uint8_t hdr[HEADER_SZ];
    hdr[0] = MAGIC_BYTE;
    hdr[1] = (uint8_t)(sessionId >> 8);
    hdr[2] = (uint8_t)(sessionId & 0xFF);
    hdr[3] = (uint8_t)(seq >> 8);
    hdr[4] = (uint8_t)(seq & 0xFF);
    udpClient.write(hdr, HEADER_SZ);
}

uint32_t imageToUdp(void){
    FPMStatus status = FPMStatus :: NOFINGER ;

    while(status != FPMStatus::OK) {
      status = finger.getImage() ;
      if (status == FPMStatus ::OK ){
        Serial.println("Image Taken") ;
        break ;
      }
      else if (status == FPMStatus::NOFINGER) {
        Serial.println("No Finger") ;
      }
      else {
         snprintf(printfBuf, PRINTF_BUF_SZ, "getImage(): error 0x%X", static_cast<uint16_t>(status)) ;
         break ; 
      }
      yield() ;
    }

    while(status != FPM::Status::OK) {
      status = finger.downloadImage() ; 

      if(status == FPMStatus::OK) {
        Serial.println("Starting Image Stream ") ;
        break ;
      }else {
        Serial.print("Error") ;
        return 0 ;
      }

      uint16_t id = (uint16_t)millis() ;
      uint16_t seq = 0 ;

      uint32_t totalRead = 0 ;
      uint16_t readLen = 0 ;

      bool readDone = false ;

      while(!readDone) {
                  
      }

    }



}
uint32_t imageToUdp(void){

    FPMStatus status = FPMStatus::NOFINGER; /* seed with any non-OK value so the loop runs at least once */

    /* Take a snapshot of the finger */
    Serial.println("\r\nPlace a finger.");

    while (status != FPMStatus::OK)
    {
        status = finger.getImage();

        if (status == FPMStatus::OK)
        {
            Serial.println("Image taken.");
        }
        else if (status == FPMStatus::NOFINGER)
        {
            Serial.println(".");
        }
        else
        {
            /* allow retries even when an error happens */
            snprintf(printfBuf, PRINTF_BUF_SZ, "getImage(): error 0x%X", static_cast<uint16_t>(status));
            Serial.println(printfBuf);
        }

        yield();
    }

    /* Initiate the image transfer */
    status = finger.downloadImage();

    if (status == FPMStatus::OK)
    {
        Serial.println("Starting image stream...");
    }
    else
    {
        snprintf(printfBuf, PRINTF_BUF_SZ, "downloadImage(): error 0x%X", static_cast<uint16_t>(status));
        Serial.println(printfBuf);
        return 0;
    }

    /* A new session ID per capture lets the server tell captures apart,
     * even if a previous transfer was incomplete. millis() truncated to
     * 16 bits is good enough -- it just needs to look "different enough"
     * from the last one. */
    uint16_t sessionId = (uint16_t)millis();
    uint16_t seq = 0;

    uint32_t totalRead = 0;
    uint16_t readLen = 0;

    /* Now, the sensor will send us the image from its image buffer, one packet at a time. */
    bool readComplete = false;

    while (!readComplete)
    {
        /* Start composing a packet to the remote server */
        udpClient.beginPacket(ip,port);

        /* Header first -- doesn't depend on the outcome of this read,
         * since the server infers "last packet" from total bytes received. */
        writeHeader(sessionId, seq);

        bool ret = finger.readDataPacket(NULL, &udpClient, &readLen, &readComplete);

        if (!ret)
        {
            snprintf_P(printfBuf, PRINTF_BUF_SZ, PSTR("readDataPacket(): failed after reading %u bytes"), totalRead);
            Serial.println(printfBuf);
            udpClient.endPacket();
            return 0;
        }

        /* Complete the packet and send it */
        if (!udpClient.endPacket())
        {
            snprintf_P(printfBuf, PRINTF_BUF_SZ, PSTR("imageToUdp(): failed to send packet, count = %u bytes"), totalRead);
            Serial.println(printfBuf);
            return 0;
        }

        totalRead += readLen;
        seq++;

        yield();
    }

    Serial.println();
    Serial.print(totalRead); Serial.print(" bytes transferred, session 0x");
    Serial.println(sessionId, HEX);
    return totalRead;
}