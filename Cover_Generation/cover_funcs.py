import numpy as np
from PIL import Image
import hashlib
from itertools import cycle
import random

#these are the function while both encoding or decoding
#i puted them in a seperate file only to avoid writing them in both files

def img_to_arr(img,mode = 'RGBA'):
	return np.array(img.convert(mode))
def img_from_arr(arr):
	return Image.fromarray(arr)

def hash_text(text):

	########## hashing password ############
	myhash = hashlib.md5()
	myhash.update(text.encode('utf-8'))
	return myhash.hexdigest()
	########################################

def get_key_from_password(password,seed = None):
	# edit this function to encrypt the password
	if seed:random.seed(seed)
	key = np.array([(ord(c) + int(random.random()*10) ) for c in password] ,dtype ='uint16')
	return key

def encrypt(arr,password_arr):
	return np.bitwise_xor(arr,np.fromiter(cycle(password_arr), arr.dtype,arr.size))
	
def decrypt(encrypted,key):
	return np.bitwise_xor(encrypted,np.fromiter(cycle(key), encrypted.dtype,encrypted.size))#just for saving time

def text_from_arr(arr):
	def check(val):
		if val != 0: return chr(val)
		else: return ''

	return ''.join(map(check,arr))	
