"""
Trying to find the best image features for feeding into the model 
"""
"""
import cv2 


def main() : 
    img = cv2.imread(path)
    gray  = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY) 

    canny = cv2.Canny(gray,255,200)
    _ , imgz = cv2.threshold(gray , 190, 255,cv2.THRESH_TOZERO)
    calche = cv2.createCLAHE(clipLimit=2.0)
    
    cv2.imshow("main",img) 
    cv2.imshow("thresh" , imgz)
    cv2.imshow("egde" , canny)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ =="__main__" :
    main() 

"""
"""
Conclusion :  
Thresholding is the best for detail representation 
Especially for fg and bg differentaton 

And based on the FINGERPRINT RECOGNITION USING MINUTIA SCORE MATCHING thresholding is the first step 
"""

""" 
So basically the original image from the sensor is ass 
And the features from the image dont show enough details that can be said to actually
train a model 

So approach would be calche  

"""

import cv2 



def main () : 
    path = r"C:\Users\blade_mx4\Documents\code\Fingerprint\finger\tets.bmp"
    img = cv2.imread(path , cv2.IMREAD_GRAYSCALE)
    #img = cv2.GaussianBlur(img,(15,15),0)
    calheobj = cv2.createCLAHE(clipLimit= 35,tileGridSize=(1,1)) 
    clahe_img = calheobj.apply(img) 

    _ , thresh = cv2.threshold(clahe_img , 50,255,cv2.THRESH_BINARY)

    cv2.imshow("clahe" , clahe_img)
    cv2.imshow("Original" ,img)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

if __name__ == "__main__" :
    main() 

"""
Other possible tries 

canny + thresh 


"""