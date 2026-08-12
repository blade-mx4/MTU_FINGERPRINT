"""
Client to send the images from the sensor to the flask server  
"""
from getImage import getFingerprintImage
import requests as rq  
import os 
# ====================== CONFIGS and HYPER PARAM============================== #

url =   'http://127.0.0.1:90/upload' #<-- Route to upload images 
url_2 = 'http://127.0.0.1:90'        #<-- Route Send id 

# File_name can normally be the name of student 
# Not just image but the Student details  
# Specail id gen must be implemented here 
# Add error handling

def dir(Name,Matric) :
    os.makedirs(f'./{Name}_{Matric}')   #<------------- F



filename = 'Victor'
def post_img(port,baud_rate,file_name) :    #<--- HTTP for message Sending 
    file_name = f"{file_name}.bmp"  #<-- TradeMarked 
    #<------------------------ Add a send reset function Here and some error message 
    getFingerprintImage(port,baud_rate,file_name)   #<--  Apperently the console outputs image
                                                    #<-- So i can easily use Serial to read the console in gui later 

    with open(file_name , 'rb') as img :

        file = { 
            "file" : img #<--- Dictionary recognized by flask for sending img 
        }
        response = rq.post(url=url , files=file ) 

    return print(response.json()) 

def post_id(Name,Surname,Matric,ID) :
    payload = {
    "Name"   : Name,
    "Surname": Surname ,
    "Matric" : Matric,
    "ID"     : ID       #<----------- Apply random ID gen from matric and name ?

    }
    feed  = rq.post(url_2 , json = payload)
    return print(feed.json())


if __name__ == "__main__" :

    os.makedirs()   #<-------- Not putting exit_ok = True to return that the dir exist 
    post_img('COM9' , 115200 ,'Victor')
    post_id('Victor','Surname','Martic',192)