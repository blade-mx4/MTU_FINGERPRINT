/*
Apperently there are billions of ways to write servers in boost asio but this is the style i choose
C++ tcp Server for receiving img 

 g++ Server.cpp Log.cpp -o Server_LOG.exe -lws2_32 -lmswsock 
*/
#include<iostream>
#include<boost/asio.hpp> 
#include<filesystem>
#include<fstream>
#include "LOG.h" // Implementing my Logging library 

using namespace std ;
using namespace boost ;
using namespace boost :: asio ; 
using namespace boost :: asio :: ip ; 


using system :: error_code ;
namespace os = std :: filesystem ;
using std::cout;

// ==== Configs and Hyper Params ==== //  

string host = "127.0.0.1"; // 0.0.0.0 for test 
int port    = 4000 ;

Log::Logger Console("file.txt" ,true) ; 


void img_load(tcp :: socket &Server) {
    os::path cwd_dir = os ::current_path() ;
    os::path img_dir = "img_inference"  ;
    os::path img_folder = cwd_dir /img_dir ;
    
    os::create_directory(img_folder); 
    string img_name = "test.bmp" ;

    system :: error_code ErRoR ;
    ofstream File(img_folder/img_name, std :: ios ::binary ) ;
    
    try {
        if (!File.is_open()) {
            cerr << "File Error "<<"\n" ; Console.log_file("FILE RELATED ERROR",LEVEL ::ErROR) ;
            return ;
        }

        char buff[8192] ;

        while (true){ 
            size_t img_bytes = Server.read_some(buffer (buff),ErRoR) ; //boost ::asio::buffer

            if (img_bytes > 0 ){
                File.write(buff , img_bytes) ;

            }
            if (ErRoR == error::eof ) { // boost :: asio ::erroro
            //    cout<< " File Uploaded SuccessFully ! " <<"\n";
                Console.log_file("FILE UPLOADED SUCCESSFULLY " , LEVEL ::INFO) ;
                break ;

            }
            else if (ErRoR) {
                std :: cerr << "ERORR :  " << ErRoR.message() << "\n";  
                Console.log_file("IMAGE RECIVEING FAILED",LEVEL::ErROR) ;
            }

        }

    }
    catch(std :: exception &e) {
        cerr << "Error : " << e.what() << "\n" ;
        Console.log_file("IMG READ FUNCTION NOT WORKIN",LEVEL::CRITICAL) ;
    }



}

// ==== Main to test function to be written here ====// 
int main() { 
    cout<<"===== Server Started ==== " <<"\n"<<"Listening..."<<" IP : " <<host <<" Port : " << port << "\n";
    Console.log_file("SERVER STARTED",LEVEL::INFO) ;

    io_context io ;
    ip ::address Host = make_address(host) ; // converting the host to a acceptable ip for boost 
    tcp::endpoint socket_address (Host , port) ;
    tcp::acceptor socket (io,socket_address) ;//bind to the endpoint 
    
    try {
        while (true){
        
        tcp :: socket Server(io) ; 
        socket.accept(Server) ;

        img_load(Server) ;
        }


    }
    catch(std :: exception &e) {
        std :: cerr << "ERROR : "<< e.what()  << "\n" ;
        Console.log_file("SERVER CRASH",LEVEL ::CRITICAL) ;
    }
    
}