import cv2
import os

"""
WO forget the multiprocessing and threading even performance in py i wont add 
"""
IMG_DIR_PATH  = "C:/Users/blade_mx4/Documents/Datasets/Real/ID 2/jpg"
THRESHOLD = .4 # the bigger the less strict the algo is   

def algo(path :str ) :
    img =  cv2.imread(path)

    kp_1,kp_2 ,mp = None ,None ,None 
    best_score = 0
    match_point = [] 
    key_point = 0 
    matched_img  = None
    _img_ = None 

    sift_algo = cv2.SIFT_create() 
    count = 0
    for file in [file for file in os.listdir(IMG_DIR_PATH)] : 
        print(file , count)
        inference_img  = cv2.imread( os.path.join(IMG_DIR_PATH ,file)) 
        key_p_1 , des_1 = sift_algo.detectAndCompute(img ,None)
        key_p_2 , des_2 = sift_algo.detectAndCompute(inference_img , None)
        count += 1
        matching_algo = cv2.FlannBasedMatcher({"algorithm" : 1 , "tree" : 5 } , {}).knnMatch(des_1 , des_2,k=2) 

        for p,q in matching_algo : 
            if p.distance < THRESHOLD *q.distance :
                match_point.append(p) 

        if len(key_p_1) < len(key_p_2) : key_point = len(key_p_1)    

        else : key_point = len(key_p_2)

        if len(match_point) / key_point * 100 > best_score : 
            best_score = len(match_point) / key_point *100 
            matched_img = file
            kp_1 , kp_2 ,mp = key_p_1,key_p_1,match_point
    # matched = cv2.drawMatched(img ,kp_1,inference_img,kp_2,mp,None) 

    return str(best_score) , matched_img 
"""
this shi is slow even with 9 img  
fuck it 
just to plug it into the socket
"""

if __name__ == "__main__" :
    path = "C:/Users/blade_mx4/Documents/Datasets/Real/ID 2/jpg/2_2_left_real_ZK9500.jpg"
    print(algo(path))
 