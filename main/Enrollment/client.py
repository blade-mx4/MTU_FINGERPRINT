import csv
from getImage import getFingerprintImage
import requests as rq  
import os 
import json 
import pandas as pd 
import logging as log

# ====================== CONFIGS and HYPER PARAM ============================== #

url =   'http://127.0.0.1:9000/image_server/upload'                             #<-- Route to upload images 
db_dir  = 'DB' #<-- folder name 
cwd_dir = os.getcwd() 
cw_fldr =  os.path.join(cwd_dir , db_dir)
os.makedirs(db_dir,exist_ok=True)


img_folder = 'IMG_DB'                                         #<-- File for image_only 
img_folder_path = os.path.join(cwd_dir,img_folder)
os.makedirs(img_folder_path,exist_ok=True)                    #<--- Folder for img_only 


log_folder_mk = os.makedirs('Enrollment_LOG',exist_ok=True)    #<--- Folder for log
log_file = os.path.join(cwd_dir,'Enrollment_LOG')
log_file = f"{log_file}/Enrollment.log"

# ======= Logger ======== #
log.basicConfig(
    filename = log_file ,
    level = log.DEBUG ,
    encoding='utf-8'
)
Log = log.getLogger(__name__)
# ====================== #

class Client : 
    def __init__(self,port,baud_rate,ID : int , Name:str , Surname:str , Matric : int ,Dept : str,  Level :int  ):
        self.port = port 
        self.baud_rate = baud_rate 
        self.filename = ""  # file name would be id for easy search 
        self.ID = ID 
        self.Name = Name 
        self.Surname = Surname 
        self.Matric = Matric 
        self.Dept = Dept 
        self.Level = Level        
        self.record = []    #<-- Global compilation of students recorded to prevent double recording matric would be the uniqe id 
     
    def csv_main_init(self) -> bool :
        """ Main Csv Creator That the pandas appends to later in the code """
        path = f"{cw_fldr}/DB.csv"
                
        if os.path.exists(path) : return 

        else : 
            header = [
                "ID "     , 
                "Name"    ,
                "Surname" ,
                "Matric"  ,
                "Level"   ,
                "Dept"    ,
            ]
            with open(path, 'w') as f : 
                csv_write = csv.writer(f)
                csv_write.writerow(header)
            Log.info(f"[Created MAIN CSV ]") 

    def main_csv(self) :
        self.csv_main_init() #<-- creates csv headers 
        try :
            level = [100,200,300,400,500]   #paramter check 
            self.Matric = str(self.Matric)

            if self.Level not in level :
                Log.error("ERORR : [ INVALID LEVEL PASSED BY USER ]")
                return print("INVALID LEVEL")
                           
            else : pass 

            if len(self.Matric) == 11 : pass 
            else : 
                Log.error("ERROR : [ INVALID MATRIC PASSED BY USER ]")
                print("INVALID Matric" , f" Matric passed  {len(self.Matric)} not equal to 11 ")
                return 
            
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
            Data.to_csv(path,index=False,mode='a',header=False)
            print(f"CSV CREATED -> {path}")
            log.info(" [ MAIN DB_CSV FILE CrEATED ] ") 
            return True

        except Exception as e : 
            Log.error(f"ErROR [ {e} ]")
            return print(f"ERROR [ {e} ]")

    def check_record(self)  :
        """
        Create a simple list to check if a student has been recorded before 
        ppl can be funny so i have to do this 
        """
        if self.Matric in self.record :
            return print("This User has Been Recoreded")
        
#I can either use pandas to check 
#use normal 
        else : pass 
           
    def post_data_img(self , img_folder_path : str ) :
            
        self.filename = f"{self.ID}.bmp"  # <== Would have to save the files[img file ] to id for easy search  
        img_path = f"{img_folder_path}/{self.filename}" #<-- this fixes the messy img aroung the code repo  

        data = {
            "ID"      : self.ID, 
            "Name"    : self.Name,
            "Surname" : self.Surname,
            "Matric"  : self.Matric ,
            "Level"   : self.Level ,
            "Dept"    : self.Dept ,
        }
        if self.main_csv() == True : pass #<-- has to create the db and also check if the parameters passed r correct fixes the invalid matric still passed problem 
        else : return Exception 

        self.check_record()

        try : 
            if getFingerprintImage(portNum=self.port,baudRate=self.baud_rate,outputFileName=img_path)  : 
                student_data = {
                    "student_data" : json.dumps(data)
                }
                student_img = {
                    "student_img"  : open(img_path, 'rb')
                }
                post = rq.post(
                    url = url ,
                    data=student_data ,
                    files=student_img
                )
                if True: 
                    self.record.append(self.Matric) 
                    Log.info("INFO : [Successfull execution ]")
                    return print(post.json()) , True
 
        except Exception as e :
            print(f"ERROR =>[ {e} ]")
            Log.error(f"ErROR [ {e} ]")
        

if __name__ == "__main__" :         #Change file name to int 
    client = Client('COM9',115200 ,221,'sdfbc','fsds',24023234220,'StytWE',100)
    client.post_data_img(img_folder_path) 

"""
Some GUI NOTES : 
1. Basically i would have to see the image to determine if the img is good enough to enter the db
2. 
"""