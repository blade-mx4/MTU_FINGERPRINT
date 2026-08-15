"""
# ============================== Old code ==================================== #
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
