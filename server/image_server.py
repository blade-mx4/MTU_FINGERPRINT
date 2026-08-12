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
Folder = './Finger_Images' 
os.makedirs(Folder,exist_ok=True) 
app.config['Folder'] = Folder 



# ================================ SEVER FUNCTIONS ============================= #

# =============== Image Receive ================= #
@app.route('/upload' , methods = ['POST','GET'])
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

def db_csv(Name,Surname,Matric) :  #<--- Y should i stress with csv library when python can do it 
   #Add logic for matric less than 10 

   Data = {
      "Name"    : [Name] ,
      "Surname" : [Surname],
      "Matric"  : [Matric] 
   }

   data = pd.DataFrame(Data)  
   os.makedirs('./DB',exist_ok=True)
   path = f"./DB"
   file_name = f"{Name}_{Surname}_{Matric}"

   DB  = data.to_csv(f"{path}/{file_name}.csv" , index=False)  

@app.route('/' ,methods = ["POST"]) #<-- Test function to collect json and save to a textfile db prototype
def id (): #<=== Receive the json of the students and save to a file 
   if request.is_json : 
      data = request.get_json() 

      name = data.get('Name')
      surname = data.get('Surname')
      matric = data.get('Matric')

      db_csv(name,surname,matric)  #<----------- Folder Creation function 

      return jsonify(
         {
            "Name"   : name ,
            "Matric" :matric ,

         }
      ),200
   
   else : return jsonify({"Message" : "Error"})
if __name__ == "__main__" : app.run(port=90 ,debug=True)
    