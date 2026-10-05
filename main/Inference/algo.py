import cv2 
import os 

"""
Prototype implementation of the flann algo in py 
we have already lost 6 sec to sensor baudrate so using py is not an option 

"""
img_file_path = r"C:\Users\blade_mx4\Documents\Datasets\Fingerptint Samples\Real\ID 1\bmp"

def flan__Algo(path_1 ) : 
    kp1,kp2,mp = None ,None ,None 
    match_point = [] 
    key_point = 0 

    img = cv2.imread(path_1) 

    sift =cv2.SIFT_create() 
    for inf_file in os.listdir(img_file_path) :
        img_  = os.path.join(img_file_path ,img_)
        img_2 = cv2.imread(img_) 

    key_p_1 ,des_1 = sift.dectectAndCompute(img ,None)     
    key_p_2 ,des_2 = sift.dectectAndCompute(img_2 ,None) 

    flann  = cv2.FlannBasedMatcher({'algorithm' : 1,'trees' : 5} , {}).knnMatch(des_1 ,des_2 , k=2 )

    for p,q in flann : 
        if p.distance < .4 * q.distance : 
            match_point.append(p)
    if len(key_p_1) < len(key_p_2) : 
        key_point = len(key_p_1) 
    else : 
        key_point = len(key_p_2) 

    if len(match_point) / key_point * 100 > 0 : 
        score = len(match_point) / key_point * 100 
        kp1 , kp2 ,mp = key_p_1 , key_p_2 , match_point
    return score  
