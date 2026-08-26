"""
This Script runs through a singular pizero conected to let say 4 esp32

            [    esp32 --> pizero/pi --wifi--> Server  ]

then loops through automatically throughthe available ports and connectes automatically
instead of hardcoding ports{which works}

todo : 



"""

import serial 
import serial.tools.list_ports 

def port_look() -> list :   #<-- Search for port available and put it in a list  
    global port             #<-- Since am using the PORTNO as an IP Address like system to help the pi route back data to the port no
    port_list = []  
    for port in serial.tools.list_ports.comports() : 
        available = port.device 
        port_list.append(available)
        if available == None : break 
    return port_list #print(port_list)


def ser_init() -> bool : 
    while True :
        try :
            for i in range(len(port_look())) :
                ser = serial.Serial(port=port_look()[i] , baudrate=9600,timeout=None) 
                if ser : 
                    print("Connected -> ")
                    return True
                    
        except Exception as e : 
            print("Connection Exception....")#print(f"ERROR -> [{e}]")
            #return False          


if __name__ == "__main__" : 
    ser_init()