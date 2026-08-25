import serial 
import serial.tools.list_ports 


def port_look() :   #<-- Search for port available and put it in a list  
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
                    print("Connected")
                    return True
                    
        except Exception as e : 
            print(f"ERROR -> [{e}]")
            










if __name__ == "__main__" : 
    ser_init()