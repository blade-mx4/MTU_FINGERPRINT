"""
This Script runs through a singular pizero conected to let say 4 esp32

            [    esp32 --> pizero/pi --wifi--> Server  ]

then loops through automatically throughthe available ports and connectes automatically
instead of hardcoding ports{which works}
also allowing multiport connection from different ports with threading 


todo : 

"""
#May turn this into a module 
from serial import Serial 
import serial.tools.list_ports 
from threading import Thread
from time import sleep
from Client import getImage

BAUDRATE = 115200
def port_look() -> list :   #<-- Search for port available and returns list of port   
    global port             #<-- Since am using the PORTNO as an IP Address like system to help the pi route back data to the port no
    port_list = []  
    for port in serial.tools.list_ports.comports() : 
        available = port.device 
        port_list.append(available)
        if available == None : break 
    return port_list              #<--- returns the comport list eg { comport 10,comport 11 } #print(port_list)


def ser_init(port_name : str ) -> bool  : #<--- serial port connection init 
    global ser #<--  So other functions can acces it 
    while True :
        try :
            # for i in range(len(port_look())) :  #<-- To just keep an open range of ports then close when range gaped
            ser = Serial(port=port_name, baudrate=BAUDRATE,timeout=None) 
            if ser.is_open : 
                print(f"Connected -> [{port_name}]")
                return True
                
        except Exception as e : 
            print(f"ERROR -> [ {e} ] ")         #<-- Essential for debugging pyserial error r suprizingliy detailed 
            sleep(1)                             #<-- Anti os Spamming

def multi_port() :                                 #<-- threading implementation
    port_list = port_look() 
    threads = []                                  #<-- thread pool , felt like calling it that nothing u can do about it 

    for port in port_list : 
        t = Thread(target=ser_init, args=(port,)) #<--  heads up due to iteration port is a str
        threads.append(t)
        t.start()
    for t in threads : t.join()                     #<--  race condition prevention 

def main() : 
    multi_port() #<-- initalize multithrading 
    if ser_init() == True : 
        if ser.is_open : 
            line = ser.read_until(b' Input ID : ').decode('utf-8')
            print(line)

            sleep(1) 

            user_input = input("Enter ID : ").strip()
            ser.write((user_input + '\n').encode()) 

            sleep(0.1)

            response = ser.read(ser.in_waiting or 1 ).decode(errors='replace') #<--  to read the remaining bytes 
            print(response) 
            

if __name__ == "__main__" : 
    