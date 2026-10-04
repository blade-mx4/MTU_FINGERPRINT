# INFERENCE SYSTEM DESIGN 

so after not being able to do the impossible and being limited by my own imagination 
i had to compromise the wired 

# So basically am implementing  star topoloy  
```
A central  server for img retrival and db stuff 

The esp32 and pizer is a node
```
# PROPOSED DESIGN 1 for infernence 
```
 __________________                                       ___________________                           ________________________
|                  | <-- wired{comport} --> [img , id]   |                   |            {id}         |                        | [  The pizero receives the id from the esp32 and sends via wifi ]
|       esp32      |-------------------------------------|       pizero      | ----------------------> |         Main Server    | [it uses the id to search for the students image and info ]
|__________________|                                     |___________________|                         |________________________|

                                                                |                                                               |
                                                                |                                                               |
                                                                | [img from esp32 ]                      [img & info from db]   |
                                                                |                                                               |
                                                                |               ____________________                            |
                                                                 ------ >       |                   |          <-----------------
                                                                                |       socket      |
        __________________                                                      |___________________|
        |                 |                                                               |
        |    socket       |[send message to user ]                                        | 
        |_________________| [esp32 acts as server waiting for message]                    |
                 ^                                                                        V
                 |                                                              _____________________
                 |                                                              |                   |
                  ----------------- [if imag passes certain threshold]          |        model      |{for multiple channel every thing would have to be multiple instance }
                                                                                |___________________|                                  
```

# PROPOSED DESIGN 2 
design 1 would have a bit of a lag issue so the best is edge compute 


```

This Script runs through a singular pizero conected to let say 4 esp32

            [    esp32 --> pizero/pi --wifi--> Server  ]

then loops through automatically throughthe available ports and connectes automatically
instead of hardcoding ports{which works}
also allowing multiport connection from different ports with threading 


Also after getting the id and img the script has to route the id and img to the server correctly 


```


# IMPLEMENTATON 1 { FLANN ALGO } 

```
with the help of flann and c++ and since i ditched neural net
speed is guranteed the only bottle neck is the sensors img readin speed 


inference steps : 
1. the esp32 send img to piserver over wifi
2. the server does the processin there 
3. send results back via wifi 
pros {of wifi} :
1. info transmission is easier 
2. easy to handle on like serial 
cons : 
1. img may get corrupt during transfer 

                                            +------------------+
    +------------+                          |                  |    DB is stored (here)
    | esp32      |      ===={wifi}=== >     |   pizero server  |
    +------------+                          |                  |
                                            +------------------+





```