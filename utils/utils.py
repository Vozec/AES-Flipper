#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _authors_: Vozec
# _date_ : 27/10/2022


import argparse
from binascii import unhexlify,hexlify
from base64   import b64decode

from utils.logger import logger

def parse_args():
	parser = argparse.ArgumentParser(add_help=True, description='This tool automates a AES CBC BitFlip attack')
	parser.add_argument("-p","--plaintext",dest="plaintext",type=str,required=True, help="Know Plaintext")
	parser.add_argument("-f","--flipped",dest="flipped",type=str,required=True, help="Flipped Plaintext")
	parser.add_argument("-c","--ciphertext",dest="cipher",type=str,required=True, help="CipherText")
	parser.add_argument("-e","--encoding",dest="encoding",type=str,choices=['base64', 'hex','base64&hex','hex&base64'],required=True,default='base64', help="CipherText Encoding")
	parser.add_argument("-i","--iv",dest="iv",action='store_true',default=False, help="Firsts Bytes are iv")
	return parser.parse_args()

def header():
	logger(r"""
    ___                _________                      
   /   | ___  _____   / ____/ (_)___  ____  ___  _____
  / /| |/ _ \/ ___/  / /_  / / / __ \/ __ \/ _ \/ ___/
 / ___ /  __(__  )  / __/ / / / /_/ / /_/ /  __/ /    
/_/  |_\___/____/  /_/   /_/_/ .___/ .___/\___/_/     
                            /_/   /_/                 
""",'log',0,0)

def complete(plaintext,args):
	if args.iv:
		return pad('%s%s'%('_IV_'*4,plaintext))
	return pad(plaintext)

def pad(cnt,blocksize=16):
	return cnt+''.join(['.' for _ in range(16-len(cnt)%blocksize)])

def split_Block(plain,ciphered,blocksize=16):
	clearBlock,cipherBlock = [],[]
	for i in range((len(plain)//blocksize)+1):
		clearBlock.append(plain[i*blocksize:blocksize*(i+1)])
		cipherBlock.append(ciphered[(i*blocksize)*2:(blocksize*(i+1))*2])
	return list(filter(None,clearBlock)),list(filter(None,cipherBlock))

def decode_Cipher(args):
	ciphertext = ''
	if(args.encoding == 'hex'):
		return unhexlify(bytes(args.cipher,'utf-8'))
	elif(args.encoding == 'base64'):
		return b64decode(bytes(args.cipher,'utf-8'))
	elif(args.encoding == 'base64&hex'):
		return unhexlify(b64decode(bytes(args.cipher,'utf-8')))
	elif(args.encoding == 'hex&base64'):
		return b64decode(unhexlify(bytes(args.cipher,'utf-8')))
	return None

def encode_Cipher(ciphertext):
	return hexlify(ciphertext).decode()

def get_diff_coord(plain,spotted,blocksize=16):
	to_flip = []
	for i in range(min(len(plain),len(spotted))):
		if plain[i] != spotted[i]:
			to_flip.append((i//blocksize,i%blocksize,spotted[i]))
	return to_flip

def print_blocs(blocks,edited,pad=32):
	print(' | ' + ' | '.join([
			b + ''.join([' ' for _ in range(pad-len(b)//10)])
			for b in [''.join(
				['\033[9%sm%s\033[0m'%(
					'2' if (i,j) in [(x,y) for x,y,z in edited] else '0',
					blocks[i][j]
				) 
				for j in range(len(blocks[i]))])
			for i in range(len(blocks))
		]
	]) + ' |')

def print_refs(Ci):
	final = '| ' + ' | '.join([
		' '*13+'Bloc %s'%str(i)+' '*13
	for i in range(len(Ci)) ]) + ' | '
	logger(final,'progress',0,0,True)

def print_detroyed(to_edit,Ci):
	final = '  ' + '   '.join([
		'%s%s%s'%(
			' '*11,'(Detroyed)' if i+1 in [_[0] for _ in to_edit] else ' '*10,' '*11
		)
	for i in range(len(Ci)) ])
	logger(final,'error',0,0,True)

def print_final(Ci,args):
	final = unhexlify(bytes(''.join(Ci),'utf-8'))
	if(args.encoding == 'hex'):
		final = ''.join(Ci)
	elif(args.encoding == 'base64'):
		final = b64encode(final).decode()
	elif(args.encoding == 'base64&hex'):
		final = hexlify(b64encode(final)).decode()
	elif(args.encoding == 'hex&base64'):
		final = b64encode(bytes(''.join(Ci),'utf-8')).decode()
	logger('| %s |\n'%final,'flag',0,0,True)


def hex_block(plain_coord):
	return  [(x,2*y,z) for x,y,z in plain_coord] + \
	 [(x,2*y+1,z) for x,y,z in plain_coord] + \
	 [(x-1,2*y,z) for x,y,z in plain_coord] + \
	 [(x-1,2*y+1,z) for x,y,z in plain_coord]

def get_bitflip(currentBit , Letter_Spotted , Letter_edited):
	result = int(currentBit,16) ^ ord(Letter_Spotted) ^ ord(Letter_edited)
	return chr(result).encode('latin1').hex()

def flipBlock(indexBlock,indexLetter,newletter,Ci,Cl,blocksize=16):
	indexChar 		= indexLetter%blocksize
	hex_spotted 	= Ci[indexBlock-1][indexChar*2:(indexChar*2)+2]
	letter_spotted  = Cl[indexBlock][indexChar:indexChar+1]
	flipped 		= get_bitflip(hex_spotted ,letter_spotted, newletter)
	Ci[indexBlock-1] = Ci[indexBlock-1][:indexChar*2] + flipped   + Ci[indexBlock-1][(indexChar*2)+2:]
	Cl[indexBlock]  =  Cl[indexBlock][:indexChar]  	  + newletter + Cl[indexBlock][(indexChar)+1:]
	return Cl,Ci

def check_validity(to_flip):
	l = list(dict.fromkeys([_[0] for _ in to_flip]))
	if (len(l) != 1):
		if sorted(l) == list(range(min(l), max(l)+1)):
			logger('\nWarning : 2 Consecutives blocs are flipped , The forged ciphertext is invalid !\n','error',0,0,True)
			return False
	return True
