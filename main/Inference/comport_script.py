"""
Heavy Implementation of Threading is Needed Here

"""
import logging as log 
from serial import Serial 
from serial.tools import list_ports 
from time import sleep
import threading
from getImage import getFingerprintImage
import os 

# ==== Configs ==== #
BAUDRATE = 115200 
cw_dir = os.getcwd() 

log_folder = os.path.join(cw_dir , '')

log.basicConfig(
    filename=

)

class COM_PORT() : #<-- removes self  
    def port_find() : 
        port_list = []
        for port in list_ports.comports() :
            ports = port.device
            port_list.append(ports)
        return port_list

    def ser_int(port) : # Connect to the port and read from it 
        try : 
            ser = Serial(port=port , baudrate = BAUDRATE , timeout=None)

            if ser.is_open : 
                line =  ser.read_until(b' Input ID : ').decode('utf-8')
                print(line)


            user_input = input("ENTER ID : ").strip()
            """
            
            Once Users has inputed ID the id is taking in by a function to search a
            hash map for the location of the img that was enrolled 
            and also the details of the student tied to the id 
            
            then send the img to the server for the model inference 
            and the id to the esp32 personal client 

            """
            ser.write((user_input + '\n').encode())
            sleep(0.01)

            response = ser.read(ser.in_waiting or 1 ).decode(errors='replace')
            print(response)
            
            sleep(0.05) #=========
            ser.close()           #=========== small wait to preent wat i cant see 
            sleep(0.05) #=========

            getFingerprintImage(portNum=port , baudRate=BAUDRATE,outputFileName=f"{user_input}.bmp")

            """
            After this a function to send the img to the server also as the code is goin on 
            
            """


        except Exception as e    :
            print(f"ERORR ==== > {e}") 

        except KeyboardInterrupt : return False     


# === Class Define === #

port_search = COM_PORT.port_find() 


print(port_search)

def thread_er() : 
    thread_pool = [] 
    for port in port_search : 
        t = threading.Thread(target= COM_PORT.ser_int, args=(port,))
        thread_pool.append(t)
        t.start() 

    for t in thread_pool : t.join()

thread_er()