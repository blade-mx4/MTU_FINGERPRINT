"""
Ported from flask -> quarts | async server implemented 
Client to send the images from the sensor to the flask / quarts server  

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

url =   'http://127.0.0.1:9000/image_server/upload'                             #<-- Route to upload images 



#==============================================================================#

def post_data_img(port,baud_rate,file_name,ID : int , Name:str , Surname:str , Matric : int ,Dept : str,  Level :int ) : 
    file_name = f"{file_name}.bmp"
    data = {
        "ID"      : ID ,
        "Name"    : Name ,
        "Surname" : Surname ,
        "Matric"  : Matric ,
        "Level"   : Level, 
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
if __name__ == "__main__" : post_data_img('COM9' , 115200 ,'img',212,'Adu','vuc',24010305032,'CYB',200)

