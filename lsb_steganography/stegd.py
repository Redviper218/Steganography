import numpy as np
from PIL import Image
import time
from lsb_funcs import img_to_arr, img_from_arr, hash_text\
					,get_key_from_password, decrypt, decode_generator,text_from_arr

def decode(img_name,password,outpath = 'decoded_'):
	
	img_ext = img_name.split('.')[-1]
	assert img_ext in ('png', 'tiff', 'bmp')
	img_mode = 'RGB' if img_ext == 'bmp' else 'RGBA'

	print('>>> loading the image ')
	########### Open the image ###########
	carier_img = Image.open(img_name)
	carier = img_to_arr(carier_img,img_mode)
	######################################
	
	carier = carier.flatten() # flatten for easier processing

	print('>>> Turning to binary')
	carier_bytes = np.unpackbits(carier).reshape((int(carier.size),8))

	carier_bytes_gen = (byte for byte in carier_bytes)


	#get the file size
	file_size = np.packbits(np.fromiter(decode_generator(carier_bytes_gen), 'uint8',10*8))
	file_size = int(text_from_arr(file_size))

	print('>>> checking password')
	# hashing the password
	seed = file_size
	hashed_pas = hash_text(password,5)
	hashed_key = get_key_from_password(hashed_pas,seed)#7dd1c460de
	
	key = get_key_from_password(password,seed)

	password_check =  np.packbits(np.fromiter(decode_generator(carier_bytes_gen), 'uint8',10*8))
	password_check = text_from_arr(decrypt(password_check,hashed_key))

	
	if password_check != hashed_pas:
		raise ValueError('Wrong password !!! ')

	print('>>> Password is valid :)\nStarting ...')
	############ decode the secret data  ###########################
	print('>>> Decoding secret file data')
	secret_data = np.packbits(np.fromiter(decode_generator(carier_bytes_gen), 'uint8',file_size*8))
	print('>>> Decrypting secret file data')
	secret_data = decrypt(secret_data,key)

	print('>>> Decoding secret file extension')
	secret_ext = np.packbits(np.fromiter(decode_generator(carier_bytes_gen),'uint8',5*8))
	print('>>> Decrypting secret file extension')
	secret_ext = decrypt(secret_ext,key)
	secret_ext = text_from_arr(secret_ext)


	name = 'stegd_decode.%s'%(secret_ext)
	print('>>> Saving the file to "%s"'%(name) )
	secret_data.tofile('%s'%(name))
	####################################################################
	
	
	
#--------------- Edit this ------------------#
img_name = 'coded_logo.tiff' # the encoded img path
password = 'test1234' # enter password here 
#--------------------------------------------#

start = time.time()
#############
decode(img_name,password)
#############
end = time.time() - start

print('completed in :',end)
