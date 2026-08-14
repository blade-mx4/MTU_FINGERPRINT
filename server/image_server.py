"""
Server - Side for receiving image
Might use that __init__.py to add the files and other useful files to the it 
to make a modular kind of server 

Security Flawed Bastard 
"""
import os 
from flask import Flask , jsonify ,json ,request
import pandas as pd 

# ============================== CONFIG and HYPER =========================== # 

app = Flask(__name__)
path = ''
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

@app.route('/' ,methods = ['POST'])
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
         "ID"   :ID ,
         "Name" : Name ,
         "Surname": Surname ,
         "Matric" : Matric ,
         "Dept"   : Dept , 
         "File"   :file

      })

if __name__ == "__main__" : app.run(port=90 , debug=True)




"""
# =============== Image Receive ================= #
@app.route('/upload' , methods = ['POST'])
def upload() :
    if request.method == "POST" : 
        if 'file' not in request.files : 
         return jsonify(
            {
               "Message :" : "No Image Uploaded"
            }
         ),400 

        file = request.files['file'] 

        if not file : return jsonify({"Message" : "Error"}) , 400 

        if file : 
           path = os.path.join(app.config['Folder'],file.filename) 
           file.save(path) 
           return jsonify(
              {
                 "Message"  : "File Saved" ,
                 "Path"     : path ,
                 "FileName" : file.filename 
              }
           ),200 

@app.route('/ID' ,methods = ["POST"]) #<-- Test function to collect json and save to a textfile db prototype
def id (): #<=== Receive the json of the students and save to a file 
   if request.is_json : 
      data = request.get_json() 

      name = data.get('Name')
      surname = data.get('Surname')
      matric = data.get('Matric')
      id = data.get("ID")

      db_csv(name,surname,matric,id)  #<----------- csv_creation

      return jsonify(
         {
            "Name"      : name ,
            "Surname"   : surname,
            "Matric"    : matric ,
            "ID"        : id

         }
      ),200
   
   else : return jsonify({"Message" : "Error"})
if __name__ == "__main__" : app.run(port=90 ,debug=True)
    """ 
