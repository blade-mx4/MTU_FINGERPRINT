"""
Server - Side for receiving image
Might use that __init__.py to add the files and other useful files to the it 
to make a modular kind of server 

Security Flawed Bastard 
"""
import os 
from quart import Blueprint, jsonify ,json ,request
import pandas as pd 


# ============================== CONFIG and HYPER =========================== # 

img_server_bp = Blueprint('image_server_api',__name__,url_prefix='/image_server')#<-- url_prefix makes add localhost:9000/img_server/uploads

cw_dir = os.getcwd()
parent_dir = 'DB_STUDENTS'
os.makedirs(parent_dir ,exist_ok=True)
 
file_path = os.path.join(cw_dir , parent_dir)   #C:\Users\blade_mx4\Documents\code\MTU-FINGERPRINT\main\Enrollment\DB_STUDENTS


print("=======================>",file_path)

#next time use path with mkdirs for precise folder creation
# ================================ SEVER FUNCTIONS ============================= #

def db_csv(ID : int,Name : str ,Surname : str ,Matric :int ,Dept : str , Level :int ) :  #<--- Y should i stress with csv library when pandascan do it 
   global student_folder 
   Data = {
      "ID"      : [ID],
      "Name"    : [Name] ,
      "Surname" : [Surname],
      "Matric"  : [Matric],
      "Dept"    : [Dept],
      "Level"    :[Level]
   }

   data = pd.DataFrame(Data) 

   student_folder = os.path.join(file_path , f'{Name}_{Surname}')
   os.makedirs(student_folder,exist_ok=True)
           
   
   data.to_csv(f"{student_folder}/{Name}_{Surname}.csv",index=False)



# ============================================================================= #

@img_server_bp.route('/upload' ,methods = ['POST'])
async def student_id() : 
   global student_folder 
   try :
      # =============== Receive ID from incoming json ================ #
      
      student_data_async =  await request.form
      student_data = json.loads(student_data_async['student_data'])
      ID = student_data.get("ID")
      Name = student_data.get("Name")
      Surname = student_data.get("Surname")
      Matric = student_data.get("Matric")
      Level = student_data.get("Level")
      Dept = student_data.get("Dept")
      
      # ================= RECEIVE img from incoming json =========== #
      file =  (await request.files).get("student_img")

      if file : 
         db_csv(ID,Name,Surname,Matric,Dept,Level)

     
         
         # student_folder = os.path.join(file_path , f'{Name}')
         # os.makedirs(student_folder,exist_ok=True)

         print("=================",student_folder)
         
         await file.save(f"{student_folder}/{file.filename}")
         
      # ==  Saving File to path == #
      return  jsonify({
            "ID"   :ID ,
            "Name" : Name ,
            "Surname": Surname ,
            "Matric" : Matric ,
            "Level"  :Level,
            "Dept"   : Dept , 
            
         }),200                                
   except Exception as e : 
      print(f'ErOrR [ {e} ]')
      return jsonify({
         "Error" : e
      })
#if __name__ == "__main__" : img_server_bp.run(port=90 , debug=True)




