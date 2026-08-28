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

# ====================== CONFIGS and HYPER PARAM ============================== #

url =   'http://127.0.0.1:9000/image_server/upload'                             #<-- Route to upload images 


db_dir  = 'DB' #<-- folder name 
cwd_dir = os.getcwd() 

cw_fldr =  os.path.join(cwd_dir , db_dir)

os.makedirs(db_dir,exist_ok=True)


def CSV_DB(id:int ,name : str , surname : str , matric : int ,dept : str , level : int ) ->bool :
    """
    Function for creating main csv 
    
    """ 
    try :   #<-- Error Handling for inputs  
        
        # ====================== Conditionals =============================== # 
        Level = [100,200,300,400,500]        #<-- Level Error Checker
        matric = str(matric)                 #<-- Had to converit to string to be able to check the length 

        if level not in  Level : 
            return print("INVALID Level " )  #<--- Acompanied by a Error Message Box
        else : pass 

        if len(matric) == 11 :   #<-- Matric Error checker    
            pass 
        else : return print("Invalid Matric ")  #<-- intended 1 line but compromise

        if name and surname == None : return print("NO Name Provided") 
        else : pass 


        data = {
            "ID"     :[id],
            "Name"   :[name] ,
            "Surname":[surname] ,
            "Matric" :[matric],
            "Dept"   :[dept] ,
            "Level"  :[level] 
        }

        Data = pd.DataFrame(data)
        path = f"{cw_fldr}/DB_GLOBAL.csv" 
        Data.to_csv(path,index=False,header=False,mode='a')  #<-- SO since am using csv -> sql i can use this to append to existing files
        print("CSV Created")

    except Exception as e : print(f"ERROR{e}") 



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
            if CSV_DB(ID,Name,Surname,Matric,Dept,Level) == True :
                return print(feed.json()) , True
        
    except Exception as e : print(f"ERROR[{e}]") 
if __name__ == "__main__" : post_data_img('COM9' , 115200 ,'diasasmond',212,'Diond','vuc',24010305032,'SWE',200)

