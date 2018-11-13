import numpy as np
from PIL import Image
import time 
from cover_funcs import img_to_arr, img_from_arr, hash_text\
					,get_key_from_password, decrypt, text_from_arr


def decode(image_name,password,output = 'decoded_'):
	img_ext = image_name.split('.')[-1]
	assert img_ext in ('png', 'tiff', 'bmp')
	img_mode = 'RGB' if img_ext == 'bmp' else 'RGBA'

	print('>>> loading the image')
	carier = img_to_arr(Image.open(image_name),img_mode).flatten()

	print('>>> decoding name and unused bytes')
	added_bytes = text_from_arr(carier[:10])


	file_size = carier.size - 20 -10 - 32 - int(added_bytes)
	
	print('>>> checking password')
	seed = file_size
	hashed_pas = hash_text(password)
	hashed_key = get_key_from_password(hashed_pas,seed)
	
	key = hashed_key #get_key_from_password(password,seed)

	password_check = text_from_arr( decrypt(carier[10:10+len(hashed_pas)],hashed_key))

	if password_check != hashed_pas:
		raise ValueError('Wrong password !!! ')

	print('>>> Password is valid :)\nStarting ...')
	x = 10+len(hashed_pas)
	name = text_from_arr( decrypt(carier[x:x+20],key))
	print(name)
	output = output+name
	print('>>> Saving the file to "%s"'%(output) )
	x=x+20
	decrypt(carier[x:x+file_size],key).tofile(output)


#--------------- Edit this ------------------#
img_name = 'coded_img.tiff' # the encoded img path
password = 'AmidEast' # the PASSWORD
#--------------------------------------------#


start = time.time()
#############
decode(img_name, password)
#############
end = time.time() - start

print('completed in :',end)
