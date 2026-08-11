MTU FINGERPRINT IMPLEMENTATIOn and Proposed Solution 

# All my failures r here and all success is here 
#

# Image Extraction From the seneor has been solved {thanks to opensource } 

# What is left is a matching Algorithm 

	Proposed Technique :
	
	# Neural Net : 
		Pro's :
		# I wont die in the hands of some unknown math 
		  higher than my iq 
		# Easier to modify 
		Con's :
		# Is there any ? 
		# Inference is the worst but tensorflowlite might help 
		  but not sure in terms of accuracy { but scaling models to like 1b should help but unnecessary for little data } 
		# Less Cons
		 
	# Fingerprint algo from scratch 
		Pro's :
		# Dont even know where to start 
		# For clout chasing and feats 
		# Learn maths i would never use again 
		Con's 
		# It would flop obviously 
		# Hard 
  
	# ML Algo 
		# Almost like NN but them algo dumb as f and i cant tweak parameters 
 

# Feature Extraction Pipeline 
	# Grayscaling 
	# Edge Extraction 
	# Ridges Extraction 
	# And any algo to extract finger features better 

# Training { IF NN still going to fold }
	# Data Augmentation Constant  
	Proposed Techniques :
		# 1 Feeding different representation of the same image into the neural net i.e grayscale , canny edge , other technique into the model 
		# 2 Normal datapipeline with image augmentation 


# SYSTEM DESIGN  1

# ======================================== ENROLLMENT  ======================================= 


#							Capture -> Model train - > Store 

# ===================================== Inference     ======================================

#							Capture -> Server -> Model 
#										|		^	-- > Comapre images with using cosine silimarites as output 
#									    v		|
#									Database -->

# =================================== New Implementation ==================================== 

#	the best wat to one shot this is siamese network 
#	
#	 		 	===========	model concept  ============ 
#	img_1 ->
#			| --> model --outputs --> similarites between the 2 image 
#	img_2 -> 
# 	img_1 is the stored image from the person . img_2 is the image to be inferenced this basically changes the whole narative / system design 

# SYSTEM DESIGN 2

# Apperently no enrollment only sample collection alos still need clean data so i would try and build a ui and algo to figure out if an image is good enough 

# The Enrollment phase {name , dept , matric , samples} <- Attached to each person 
# 		   	 capture	 	
#				|
#				v
#			    DB 


# Inference / Deployed 

# infered {id/fing_img} -> server -> db  
#									  |
#									  V
#									model -> outputs 	