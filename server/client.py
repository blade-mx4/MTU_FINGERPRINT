"""
Client to send the images from the sensor to the flask server  

# ===================== NOTES =================================#

#================== FUNTIONS ===================#

# File_name can normally be the name of student             |   |   
# Not just image but the Student details                    |   | 
# Specail id gen must be implemented here                   | x |
# Add error handling                                        | x | 

"""
from getImage import getFingerprintImage
import requests as rq  
import os 
import json 

# ====================== CONFIGS and HYPER PARAM ============================== #

url =   'http://127.0.0.1:90'                             #<-- Route to upload images 



def post_data_img(port,baud_rate,file_name,Name,Surname,Matric : int ,Dept, ID : int) : 
    file_name = f"{file_name}.bmp"
    data = {
        "ID"      : ID ,
        "Name"    : Name ,
        "Surname" : Surname ,
        "Matric"  : Matric , 
        "Dept"    : Dept
    }
    try : 
        if getFingerprintImage(port,baud_rate,file_name) == True : 
            student_data = {"student_data" : json.dumps(data)}
            student_img = {"student_img" : open(file_name ,'rb')} 
            feed = rq.post(
                url ,
                data=student_data ,
                files=student_img 
            ) 
            return print(feed.json()) 
    except Exception as e : print(f"ERROR[{e}]") 
if __name__ == "__main__" : post_data_img('COM9' , 115200 ,'img','Agu','vuc',24010305032,'CYB',192)


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