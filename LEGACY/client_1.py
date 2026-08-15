

"""
# ===================== OLD CODE ========================== #
filename = 'Victor'
def post_img(port,baud_rate,file_name) :                        #<-- Fucntion for Img Sending 
    file_name = f"{file_name}.bmp"                              #<-- TradeMarked 

    try :                                                       #<--  Error Handling 
                                                                #<-- Add a send reset function Here and some error message 
        check = getFingerprintImage(port,baud_rate,file_name)   #<--  Apperently the console outputs image
                                                                #<-- So i can easily use Serial to read the console in gui later 
        if check == True :                                      #<-- Just to check and prevent confilt 
            with open(file_name , 'rb') as img :
                file = { 
                    "file" : img                                #<--- Dictionary recognized by flask for sending img 
                }
        response = rq.post(url=url , files=file ) 

        return print(response.json()) 
    except Exception as e : print("Error => ", e) 

     
def post_id(Name,Surname,Matric,ID) :
    payload = {
    "Name"   : Name,
    "Surname": Surname ,
    "Matric" : Matric,
    "ID"     : ID                                              #<----------- Apply random ID gen from matric and name ?

    }
    feed  = rq.post(url_2 , json = payload)
    return print(feed.json())


if __name__ == "__main__" :

       #<-------- Not putting exit_ok = True to return that the dir exist 
    #post_img('Victor')
    post_id() 

"""