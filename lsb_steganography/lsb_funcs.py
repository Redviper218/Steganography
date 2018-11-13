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

def hash_text(text,lenght = 5):

	########## hashing password ############
	myhash = hashlib.shake_128()
	myhash.update(text.encode('utf-8'))
	return myhash.hexdigest(lenght)
	########################################

def get_key_from_password(password,seed = None):
	# edit this function to encrypt the password
	if seed:random.seed(seed)
	key = np.array([(ord(c) + int(random.random()*10) ) for c in password] ,dtype ='uint16')
	return key

def encrypt(arr,password_arr):

	return np.bitwise_xor(arr,np.fromiter(cycle(password_arr), arr.dtype,arr.size))

def encode_generator(carier_bytes_gen,secret_bits_gen):
	while True:#i < secret_bits.size:
		byte = next(carier_bytes_gen)
		byte[-1] = next(secret_bits_gen)
		for b in byte: yield b
		#yield np.packbits(byte)[0]  # this much slower
			
	



def text_from_arr(arr):
	def check(val):
		if val != 0: return chr(val)
		else: return ''

	return ''.join(map(check,arr))	

def decrypt(encrypted,key):
	return np.bitwise_xor(encrypted,np.fromiter(cycle(key), encrypted.dtype,encrypted.size))#just for saving time

def decode_generator(carier_bytes_gen):
	i=0
	while True:#i < secret_bits.size:	
		yield next(carier_bytes_gen)[-1]
