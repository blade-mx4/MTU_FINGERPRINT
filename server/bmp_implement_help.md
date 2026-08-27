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
