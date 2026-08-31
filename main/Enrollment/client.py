"""
Stumbled across re library python and looks helpfull in string search and sort of 

"""
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
import pandas as pd 
from threading import Thread 
import logging as log

# ====================== CONFIGS and HYPER PARAM ============================== #

url =   'http://127.0.0.1:9000/image_server/upload'                             #<-- Route to upload images 
db_dir  = 'DB' #<-- folder name 
cwd_dir = os.getcwd() 
cw_fldr =  os.path.join(cwd_dir , db_dir)
os.makedirs(db_dir,exist_ok=True)

log_folder_mk = os.makedirs('Enrollment_LOG',exist_ok=True)    #<--- Folder for log
log_file = os.path.join(cw_fldr,'Enrollment_LOG')

log_file = f"{log_file}/Enrollment.log"


# ======================================= #

class Client : 
    def __init__(self,port,baud_rate,file_name,ID : int , Name:str , Surname:str , Matric : int ,Dept : str,  Level :int ):
        self.port = port 
        self.baud_rate = baud_rate 
        self.filename = file_name 
        self.ID = ID 
        self.Name = Name 
        self.Surname = Surname 
        self.Matric = Matric 
        self.Dept = Dept 
        self.Level = Level        

    def main_csv(self) : 
        try :
            level = [100,200,300,400,500]
            self.Matric = str(self.Matric)

            if self.Level not in level :
                return print("INVALID LEVEL")
            else : pass 

            if len(self.Matric) == 11 : pass 
            else : return print("INVALID Matric")

            if self.Name and self.Surname == None : return print(" Input Complete Name ")
            else : pass 


            data = {
                "ID"      : [self.ID], 
                "Name"    : [self.Name] ,
                "Surname" : [self.Surname],
                "Matric"  : [self.Matric],
                "Level"   : [self.Level],
                "Dept"    : [self.Dept],

            }

            Data = pd.DataFrame(data)
            path = f"{cw_fldr}/DB.csv"
            Data.to_csv(path,index=False)
            print(f"CSV CREATED -> {path}")
            return True 
        except Exception as e : print(f"ERROR [ {e} ]")

    def post_data_img(self) :
        self.filename = f"{self.filename}.bmp"
    
        data = {
            "ID"      : [self.ID], 
            "Name"    : [self.Name] ,
            "Surname" : [self.Surname],
            "Matric"  : [self.Matric],
            "Level"   : [self.Level],
            "Dept"    : [self.Dept],
        }
        try : 
            if getFingerprintImage(portNum=self.port,baudRate=self.baud_rate,outputFileName=self.filename) == True :
                student_data = {
                    "student_data" : json.dumps(data)
                }
                student_img = {
                    "student_img"  : open(self.filename, 'rb')
                }
                post = rq.post(
                    url = url ,
                    data=student_data ,
                    files=student_img
                )
                if self.main_csv() == True : 
                    return print(post.json()) , True

        except Exception as e :
            print(f"ERROR =>[ {e} ]")

client = Client('COM9' , 115200 ,'diasasmond',212,'Diond','vuc',24010305032,'SWE',200)
client.post_data_img()