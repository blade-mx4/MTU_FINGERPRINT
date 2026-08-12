# ========================================== Server ============================================= # 

This is the Concept for Moving the image through out a server durint


# ============== IMPLEMENTATION ============== # 

# ========================= Moving to server during Enrollment ============================== #

1. Option 1 
    Using : getImages.py -> script_to_send_saved_img _to server -> flask_server 

    1. script_to_send_saved_img _to server : functions 
        a. calls the function to init imag capture 
        b. sending images in the format  
            
            img + name + matric + special_id  
        c. Sends to the flask server  
        d. Logs to help check id 
        e. GUI convertion 


# Final : 
    Flask server : 
        Waiting for images 
        Db implementation 




# ========================== Sensor to server Movement ======================================= #
1. Esp32 sending images to the Server{not sure if am uing flask or udp }




# =================================== Verifications ============================================== # 

This part is for sending the imag from the server db to the model for verification 

# ======================= SKETCH ======================== #

    img_sent(from esp32 , with special id for each members ) -----> FLASK --------------->
                                                                   using id 
                                                                    |
                                                                    |                       Send imgs as pairs ------------------------------- > Model
                                                                    V
                                                                   
                                                                    DB    ---------------> 


