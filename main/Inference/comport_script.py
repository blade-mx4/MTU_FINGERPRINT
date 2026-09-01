from serial import Serial 
from serial.tools import list_ports 
from time import sleep 
from threading import Thread 



# ==== Configs ==== #
BAUDRATE = 115200 



def port_find() ->list[str]:
    port_list  = [] 
    for port in list_ports.comports(): 
        ports = port.device
        port_list.append(ports)
    print(port_list)
    return port_list 


def ser_init(port : str ):
        try : 
            ser = Serial(port=port,baudrate=BAUDRATE , timeout=None)

            if ser.is_open : 
                print(port)
                while True : 
                    ser.read()
        except Exception as e : 
            print(f"Erorr -> {e}")


def thread_er () : 
    ports_list = port_find () 
    thread = []

    for port in ports_list : 
        t = Thread(target=ser_init , args=(port,))
        thread.append(t)
        t.start() 
    for t in thread :
        t.join()

thread_er()