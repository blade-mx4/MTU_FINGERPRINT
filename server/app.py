from flask import Flask 
from image_server import img_server_bp 
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__) 

def Server_Main() :
    app.register_blueprint(img_server_bp) 
    return app 

if __name__ == "__main__" : Server_Main().run(port=9000,debug=True) #<-- Naughty oneliner