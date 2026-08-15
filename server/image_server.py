"""
Server - Side for receiving image
Might use that __init__.py to add the files and other useful files to the it 
to make a modular kind of server 

Security Flawed Bastard 
"""
import os 
from flask import Blueprint, jsonify ,json ,request
import pandas as pd 


# ============================== CONFIG and HYPER =========================== # 

img_server_bp = Blueprint('image_server_api',__name__,url_prefix='/image_server')#<-- url_prefix makes add localhost:9000/img_server/uploads
path = ''   #<--- Making it empty ? dont want to remove this cause i sorted out the use of globals but fuck it 
# ================================ SEVER FUNCTIONS ============================= #

def db_csv(ID : int,Name,Surname,Matric :int ,Dept ) :  #<--- Y should i stress with csv library when python can do it 
   #Add logic for matric less than 10 
   parent_dir = './DB'
   os.makedirs(parent_dir,exist_ok=True)  
   global path
   Data = {
      "ID"      : [ID],
      "Name"    : [Name] ,
      "Surname" : [Surname],
      "Matric"  : [Matric],
      "Dept"    : [Dept]
   }

   data = pd.DataFrame(Data) 

   path = os.path.join(parent_dir,(Name)) 

  
   os.makedirs(path,exist_ok=True)
   
   data.to_csv(f"{path}/{Name}_{Surname}.csv",index=False)



# ============================================================================= #

@img_server_bp.route('/upload' ,methods = ['POST'])
def student_id() : 
   # =============== Receive ID from incoming json ================ #
   student_data = json.loads(request.form["student_data"]) 
   ID = student_data.get("ID")
   Name = student_data.get("Name")
   Surname = student_data.get("Surname")
   Matric = student_data.get("Matric")
   Dept = student_data.get("Dept")

   # ================= RECEIVE img from incoming json =========== #
   file = request.files.get("student_img")

   if file : 
    db_csv(ID,Name,Surname,Matric,Dept)

    file.save(f"{path}/{file.filename}")
   # ==  Saving File to path == #
   return jsonify({
         "Mesaage" : "SuccessFully Enrolled Student ",
         "Status" :True,
         "ID"   :ID ,
         "Name" : Name ,
         "Surname": Surname ,
         "Matric" : Matric ,
         "Dept"   : Dept , 
      }),200                                

#if __name__ == "__main__" : img_server_bp.run(port=90 , debug=True)




