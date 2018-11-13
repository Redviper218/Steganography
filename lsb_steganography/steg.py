import numpy as np
from PIL import Image
import time
from lsb_funcs import img_to_arr, img_from_arr, hash_text\
					,get_key_from_password, encrypt, encode_generator




def encode(img_name, file_name,password,out_ext = 'tiff'):
	""" hide the specified file inside the given image using the lsb method"""

	
	assert out_ext in ('png', 'tiff', 'bmp')
	img_mode = 'RGB' if out_ext == 'bmp' else 'RGBA'

	print('>>> loading the img')
	############ Open the image ############
	carier_img = Image.open(img_name)
	carier = img_to_arr(carier_img,img_mode)
	# flatten the img array for easier processing
	########################################

	#######################################################
	shape = carier.shape  # backup the shape of the img
	carier = carier.flatten()
	#######################################################

	print('>>> loading the file')
	############ Open the file ########################
	secret_arr = np.fromfile(file_name,dtype = 'uint8')
	print('[info]:file size --> ',secret_arr.size)
	###################################################

	############ Calculate if the image can hold the file ############
	print('[info]:carier size --> ',carier.size)

	str_size = str(secret_arr.size)
	ext = file_name.split('.')[-1]
	print(str_size)
	assert len(str_size) < 10 
	assert len(ext) <5
	required = (secret_arr.size + 10+ 10+5)*8 

	print('[info]:required size --> ',required)
	# 5 for storing the file extension
	# and 10 for stoing the file size 
	# 10 for passwordcheck
	if carier.size < required:
		raise ValueError('carier img can\'t hold this file !!')

	print('The image can hold this file\nStarting...')
	
	##################################################################
	arr_size = np.array([ord(c) for c in str_size],'uint8')
	arr_size.resize((10,))
	ext_arr = np.array([ord(c) for c in ext],'uint8')
	ext_arr.resize((5,))

	encoded_data_size = secret_arr.size + ext_arr.size + arr_size.size

	# hashing the password
	seed = secret_arr.size
	hashed_pas = hash_text(password,5)
	hashed_key = get_key_from_password(hashed_pas,seed)
	
	key = get_key_from_password(password,seed)

	print('>>> Encrypting data')
	############ Encrypting the data ############
	hashed_pas = np.array([ord(c) for c in hashed_pas],'uint8')
	password_check = encrypt(hashed_pas,hashed_key) # used to check password when decoding
	
	secret_arr = encrypt(secret_arr,key) # encode the file array 
	ext_arr = encrypt(ext_arr,key)
	#####################################################################
	print('>>> preparing the secret array')
	part1 = np.append(arr_size,password_check)
	secret_arr = np.append(part1,secret_arr)
	secret_arr = np.append(secret_arr,ext_arr)

	############ get the binary represantation  ############
	print('>>> Turning to binary')
	carier_bytes = np.unpackbits(carier).reshape((int(carier.size),8))

	secret_bits = np.unpackbits(secret_arr)
	######################################################################

	


	############ generators to be able to use np.fromiter ############
	carier_bytes_gen = (byte for byte in carier_bytes)
	secret_bits_gen = (bit for bit in secret_bits)
	##################################################################
	print('>>> encoding the secret data to the image')
	
	############ using np.fromiter and the encode_generator ############
	############ to encode the carier bytes  ###########################
	result = np.packbits(np.fromiter(encode_generator(carier_bytes_gen, secret_bits_gen), 'uint8',secret_bits.size*8))

	####################################################################

	

	############ filling the result array with the intaced values of the image ############
	carier = np.append(result,carier[result.size:]).reshape(shape)

	#######################################################################################


	name = img_name.split('.')
	name.pop(-1)
	name = ''.join(name)
	print('>>> Saving the encoded image to "%s"'%('coded_'+name+'.tiff'))
	############ Saving the Encoded image ############
	print(shape)
	carier = carier.reshape(shape)
	carier_img = img_from_arr(carier.reshape(shape))
	carier_img.save(('coded_'+name+'.'+out_ext))
	##################################################


#--------------- Edit this ------------------#
file_name = 'test.exe'  # The secret file
img_name = 'logo.jpg'  # the carier img path 
password = 'test1234'
out_ext = 'tiff'# 'png','tiff', impossible to use 'jpg'
#--------------------------------------------#

start = time.time()
#############
encode(img_name, file_name,password,out_ext = out_ext)
#############
end = time.time() - start

print('completed in :',end)
