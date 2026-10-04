# import os 
import cv2 

# ==== Configs ==== #
path_1 =  r"C:\Users\blade_mx4\Documents\code\MTU-FINGERPRINT\main\Enrollment\1_normal_.bmp"
path_2 =  r"C:\Users\blade_mx4\Documents\code\MTU-FINGERPRINT\main\Enrollment\4_normal_.bmp"
best_score = 0 

img = cv2.imread(path_1)
img2 = cv2.imread(path_2)

kp1,kp2,mp = None , None ,None #kp = keypoint , mp = matchin point 

sift = cv2.SIFT_create()

key_p_1 ,des_1 = sift.detectAndCompute(img ,None)
key_p_2 ,des_2 = sift.detectAndCompute(img2 ,None)

matcher = cv2.FlannBasedMatcher({'algorithm' : 1,'trees' : 5}, {'check':50}).knnMatch(des_1 ,des_2,k =2)

match_point = []

for p,q in matcher : 
    if p.distance < .4* q.distance : 
        match_point.append(p)
  

key_point = 0 

if len(key_p_1) < len(key_p_2) :
    key_point = len(key_p_1)
else : 
    key_point = len(key_p_2) 

if len(match_point) / key_point * 100 > best_score : 
    best_score = len(match_point) / key_point * 100 
    kp1 , kp2 ,mp = key_p_1 ,key_p_2,match_point

matched = cv2.drawMatches(img  , kp1, img2 , kp2 ,  mp ,None)
# cv2.imshow("img" ,img)
# cv2.imshow("img_2",img2)

# cv2.imshow("" ,matched)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("score :" ,str(best_score))