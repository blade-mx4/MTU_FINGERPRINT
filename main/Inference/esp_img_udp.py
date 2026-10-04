"""
This was Ai gen - code 
I would have to implement the code in c++ due to my inabilty to implement it in python  
And plus for the full set up this is slow we r already bottle necked by the sensor baudrate
"""

import socket
import struct

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 288
IMAGE_DEPTH = 8

HOST = "0.0.0.0"
PORT = 4000

# 4-bit packed pixels: 2 pixels per byte
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


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"Server listening on UDP {HOST}:{PORT}...")

    raw_buffer = bytearray()

    try:
        while len(raw_buffer) < RAW_SENSOR_BYTES:
            data, addr = server.recvfrom(10000)
            raw_buffer.extend(data)
            print(f"Received packet: {len(data)} bytes ({len(raw_buffer)}/{RAW_SENSOR_BYTES})")

        raw_buffer = raw_buffer[:RAW_SENSOR_BYTES]
        print("Raw frame complete. Unpacking 4-bit pixels to 8-bit grayscale...")

        unpacked_raster = unpack_4bit_pixels(raw_buffer)
        bmp_header = assemble_bmp_header(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_DEPTH)

        with open("test.bmp", "wb") as f:
            f.write(bmp_header)
            f.write(unpacked_raster)

        print("Image saved as test.bmp (File size: ~74.8 KB).")

    finally:
        server.close()