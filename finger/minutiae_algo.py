import cv2 
import numpy as np 

path = r"C:\Users\blade_mx4\Documents\Datasets\Fingerptint Samples\Real\ID 1\bmp\1_1_left_real_ZK9500.bmp"
img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)

k_size = (5,5)               # kernale size that slides over the img like cnn basically to look at the img
sigma = 4                   # how wide the gausiian smaller concentrates on the centre 
theta_range = np.deg2rad(90) # the oreientation of the filter 
lambd = 10                # controls the spatial freq of the patterns dectected {smaller finer patterns}
gamma = 1              # apect ration of the filter  = 1 {circular} < 1 {elipse }
psi = np.pi/2

kernel = cv2.getGaborKernel(k_size , sigma ,theta_range ,gamma,psi ,ktype=cv2.CV_32F)
filtered_img = cv2.filter2D(img , cv2.CV_32F ,kernel)

filtered_img = cv2.normalize(filtered_img , None ,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
cv2.imshow("" , img)
cv2.imshow("2" , filtered_img)
cv2.waitKey(0)
cv2.destroyAllWindows()