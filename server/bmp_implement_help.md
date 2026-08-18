# Small Helper Guide in implementing the bmp header for udp transfer


The post on stack overflow gave me an idea for using udp for transmitting the image from esp32 to udp server 
```
You would need to split the img into muitple packets when sendin 
and some logic to put them back together " You would likely need a header format " <-- This line
```
since there is a bmp header format in the getImages.py 
i can  use that and concate with a udp.server # but how do i simulate bytes transfer before going to esp32 