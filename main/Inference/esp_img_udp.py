"""
Async UDP FOR PROTOTYPE IF THEY R READY I MOVE TO c++ 
just use pybind or just give them in pure py  
"""
import socket 
import struct 
import time 

# == Configs == # 
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 288 
IMAGE_DEPTH = 8

HOST = "0.0.0.0"
PORT = 4000

RAW_SENSOR_BYTES = (IMAGE_WIDTH * IMAGE_HEIGHT) // 2  # 36,864 bytes

def assemble_bmp_header(width: int, height: int, depth: int = 8) -> bytes:
    bmp_header = struct.Struct("<2s3L LLl2H6L")
    bmp_palette_entry = struct.Struct("4B")  # Format: Blue, Green, Red, Reserved

    byte_width = ((depth * width + 31) // 32) * 4
    num_colours = 2**depth
    palette_size = bmp_palette_entry.size * num_colours
    image_size = byte_width * height
    file_size = bmp_header.size + palette_size + image_size
    raster_offset = bmp_header.size + palette_size

    BMP_INFOHEADER_SZ = 40
    TYPICAL_DPI = 2835  # ~72 DPI

    # Top-down bitmap (negative height)
    header_bytes = bmp_header.pack(
        b"BM",
        file_size,
        0,
        raster_offset,
        BMP_INFOHEADER_SZ,
        width,
        -height,
        1,
        depth,
        0,
        image_size,
        TYPICAL_DPI,
        TYPICAL_DPI,
        0,
        0,
    )

    palette_bytes = bytearray()
    for i in range(num_colours):
        # Grayscale palette (B=i, G=i, R=i, Reserved=0)
        palette_bytes.extend(bmp_palette_entry.pack(i, i, i, 0))

    return header_bytes + bytes(palette_bytes)


def unpack_4bit_pixels(raw_data: bytes) -> bytes:
    """Unpack 4-bit packed pixel nibbles (0-15) into 8-bit grayscale values (0-255)."""
    unpacked = bytearray(len(raw_data) * 2)
    for i, b in enumerate(raw_data):
        high_nibble = (b >> 4) & 0x0F
        low_nibble = b & 0x0F
        # Scale 0..15 range to 0..255
        unpacked[i * 2] = high_nibble * 17
        unpacked[i * 2 + 1] = low_nibble * 17
    return bytes(unpacked)


def Server () :  
    raw_buffer = bytearray() 
    _socket_ = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    # _socket_.setblocking(False) 
    _socket_.bind((HOST , PORT )) 
    print("================== Server =================== ")
    print(f"IP  : {HOST}" , "\n" ,
          f"PORT: {PORT}")
    print(" ============================================= ")
    try :
        """
Major Operational Bug 
If the user forgets to their finger on the sensor
it re-reads and sends half packets on the next loop 
the fix : 
    function checks the current byte and recalls the server 
        """
        while len(raw_buffer) < RAW_SENSOR_BYTES : 
            data , addr = _socket_.recvfrom(8192)  
            raw_buffer.extend(data)
            print(f"{len(raw_buffer)} / {RAW_SENSOR_BYTES}")

        raw_buffer = raw_buffer[:RAW_SENSOR_BYTES]
        print(" IMG RECEIVED ")

        unpacked_raster = unpack_4bit_pixels(raw_buffer) 
        bmp_header = assemble_bmp_header(IMAGE_WIDTH ,IMAGE_HEIGHT ,IMAGE_DEPTH )

        with open("test.bmp" , "wb") as file :
            file.write(bmp_header)
            file.write(unpacked_raster)
        _socket_.close()
        """
Matchin ops 
Server Communication With esp32         
        """
        time.sleep(3)       #<-- sleep for 2 sec 
        Server()            #<-- this is my first time using recursion and i one shot it faaaaaaaaaaaaaaaaaaawwwwwwwwwwwwwwwwwwwwwwkkkkkkkkk

        

    except Exception as e : print(f"ERROR :{e}") 
    except KeyboardInterrupt :print()

if __name__ =="__main__" :
    Server() 