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
#include<chrono>

// using namespace std ;
using namespace boost ;
using namespace boost :: asio ; 
using namespace boost :: asio :: ip ; 


using system :: error_code ;
namespace os = std :: filesystem ;
using std::cout;

// ==== Configs and Hyper Params ==== //  

std :: string host = "127.0.0.1"; // 0.0.0.0 for test 
int port    = 4000 ;
os::path cwd_dir = os ::current_path() ;
Log::Logger Console("file.txt" ,true) ;

os::path img_dir = "IMGFORTF"  ;
os::path img_folder = cwd_dir /img_dir ;   


void img_load(tcp :: socket &Server) {  
    os::create_directory(img_folder); 

    std :: string img_name = "test.bmp" ;
 
    system :: error_code ErRoR ;
    std :: ofstream File(img_folder/img_name, std :: ios ::binary ) ; // file path for img_1 
    
    try {
        if (!File.is_open()) {
            std :: cerr << "File Error "<<"\n" ; Console.log_file("FILE RELATED ERROR",LEVEL ::ErROR) ;
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
                // return  ;
                break ;
            }

            else if (ErRoR) {
                std :: cerr << "ERORR :  " << ErRoR.message() << "\n";  
                Console.log_file("IMAGE RECIVEING FAILED",LEVEL::ErROR) ;
                return ;
            }      
        }
        File.close() ;
        }catch(std :: exception &e) {
            std :: cerr << "Error : " << e.what() << "\n" ;
            Console.log_file("IMG READ FUNCTION NOT WORKIN",LEVEL::CRITICAL) ;
            return  ;

        }
    // return true ;
}

void load_img_2(tcp :: socket &Server){
    // ------------------------ Receive 2nd Img ------------------------- //
    std :: string img_name = "test_2.bmp" ;
    std :: ofstream File_1(img_folder/img_name, std :: ios ::binary ) ; // file path for img_2 
    
    system :: error_code Error;
    try{ 
        if (!File_1.is_open()){
            std :: cerr << "File Error "<<"\n" ; Console.log_file("FILE RELATED ERROR",LEVEL ::ErROR) ;
        }
        char buff_2[8192] ;
        
      

        while (true ) {
            size_t img_2_bytes  = Server.read_some(buffer(buff_2),Error) ;
            if (img_2_bytes > 0) {
                File_1.write(buff_2,img_2_bytes) ; 

            }
            if (Error == error ::eof) {
                std :: cout<<"RECIEVED IMG _2 " << '\n' ; 
                break ;
            }
            else if (Error){
                std :: cerr <<"ERROR : "<<Error.message() << '\n' ;
                break ;
            }
        }
    }

    catch(std:: exception  &e ){
        std ::cerr << "ERORR" << Error.message() << '\n' ;
    }

}



// ==== Main to test function to be written here ====// 
int main() { 
    cout<<"===== Server Started ==== " <<"\n"<<"Listening..."<<" IP : " <<host <<" Port : " << port << "\n";
    Console.log_file("SERVER STARTED",LEVEL::INFO) ;

    io_context io ;
    steady_timer time(io , std :: chrono::seconds(2)); 

    ip ::address Host = make_address(host) ; // converting the host to a acceptable ip for boost 
    tcp::endpoint socket_address (Host , port) ;
    tcp::acceptor socket (io,socket_address) ;//bind to the endpoint 
    
    try {
        tcp :: socket Server(io) ;
        socket.accept(Server) ;
        img_load(Server) ;
        
        std :: cout << " WAITING FOR 2nd Img " << '\n';

        tcp :: socket Server_2(io) ;  
        socket.accept(Server_2) ;
        load_img_2(Server_2) ;

    
        // while (img_load(Server) != true ){
        //     //existential loop 
        // }


    
    }

    catch(std :: exception &e) {
        std :: cerr << "ERROR : "<< e.what()  << "\n" ;
        Console.log_file("SERVER CRASH",LEVEL ::CRITICAL) ;
    }
    
}