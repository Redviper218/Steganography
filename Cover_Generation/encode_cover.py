import numpy as np
from PIL import Image
import time 
from cover_funcs import img_to_arr, img_from_arr, hash_text\
					,get_key_from_password, encrypt,text_from_arr


def encode(secret_file_name,password,output = 'coded_img',img_ext = 'tiff'):
	output+='.'+img_ext
	import math
	print(">>> loading the file")
	secret_file = np.fromfile(secret_file_name,dtype = 'uint8')

	seed = secret_file.size
	hashed_pas = hash_text(password)
	hashed_key = get_key_from_password(hashed_pas,seed) #this is used to encrypt password check
	
	
	key = hashed_key #this is used to encrypt the file data

	password_check = encrypt(np.array([ord(c) for c in hashed_pas],'uint8'),hashed_key) # used to check password when decoding

	########### Generating the cover img ###################
	assert img_ext in ('png', 'tiff', 'bmp')
	img_mode = 'RGB' if img_ext is 'bmp' else 'RGBA'
	pixel_size = len(img_mode)

											# 32 
	required = secret_file.size + 20 + 10+ password_check.size #required bytes
	w = int(math.sqrt( required/pixel_size))+1 # width of the cover img
	shape = (w,w,pixel_size)  # shape of the cover array
	print('shape: ',shape)

	img_size = w**2 *pixel_size # number of bytes available
	added = img_size - required # number of unused bytes

	cover = np.array([],dtype = 'uint8')

	############################################################################

	print('>>> encoding name and unused bytes')
	
	added_bytes = np.array([ord(c) for c in str(added)],dtype = 'uint8')
	added_bytes.resize((10,))
	secret_name = np.array([ord(c) for c in str(secret_file_name)],dtype = 'uint8')
	secret_name.resize((20,))

	
	cover= np.append(cover, added_bytes)

	#password checker /////////////////////////////////
	cover = np.append(cover,password_check)
	#########///////////////////////############

	cover= np.append(cover, encrypt(secret_name,key))
	del secret_name, added_bytes,password_check

	print('>>> encoding file')
	cover = np.append(cover,encrypt(secret_file,key))


	print('>>> saving the encoded img to "%s"'%(output))

	img_from_arr(np.resize(cover,shape)).save(output)
	return np.resize(cover,shape) 


#--------------- Edit this ------------------#
file_name = 'sandbox.zip' # The very secret file xD
password = 'testcode' # The PASSWORD
img_ext = 'tiff' # 'png','tiff', !!! impossible to use jpg !!!
#--------------------------------------------#

start = time.time()
#############
encode(file_name,password,img_ext =img_ext )

#############
end = time.time() - start

print('completed in :',end)



