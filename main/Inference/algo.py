import cv2 
import os 

"""
Prototype implementation of the flann algo in py 
we have already lost 6 sec to sensor baudrate so using py is not an option 

"""
img_file_path = r"C:\Users\blade_mx4\Documents\Datasets\Fingerptint Samples\Real\ID 1\bmp"

def flan__Algo(path_1 ) : 
    kp1,kp2,mp = None ,None ,None 
    img = cv2.imread(path_1) 

    sift =cv2.SIFT_create() 
    for inf_file in os.listdir() :

    key_p_1 ,des_1 = sift.dectectAndCompute(img ) 
