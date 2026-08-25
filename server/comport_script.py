import serial 
import serial.tools.list_ports 


def port_look() :
    port_list = []  
    for port in serial.tools.list_ports.comports() : 
        available = port.device 
        port_list.append(available)
        if available == None : break 
    return port_list #print(port_list)
