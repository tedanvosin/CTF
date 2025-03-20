#!/usr/bin/env python
import RPi.GPIO as GPIO
import requests
import MFRC522
import signal
import time 
import json 

next_in_seq = 0 

def bytes(num):
	return [int(num >> 16), int((num >> 8) & 0xFF), int(num & 0xFF)]

def random_key_gen():
	global next_in_seq
	next_in_seq = (next_in_seq * 0x52c6425d + 0xcc52c) % 2**32
	return next_in_seq % 0xffffff;

def end_read(signal,frame):
	exit()


signal.signal(signal.SIGINT, end_read)

MIFAREReader = MFRC522.MFRC522()

def read_mifare_classic_card(passcode, api):
	global next_in_seq
	next_in_seq = passcode
	url = api
	continue_reading = True

	sectors = [8,22,34]

	while continue_reading:
		
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

		(status,uid) = MIFAREReader.MFRC522_Anticoll()
	 
		if status == MIFAREReader.MI_OK:

			uid_hex = "".join(hex(x)[2:] for x in uid)
			#print "UID:", uid_hex
		 
			MIFAREReader.MFRC522_SelectTag(uid)
			card_information = []

			for i in range(0,3):
				sector = sectors[i]
				key_gen = []
				
				for k in range(0,2):
					key_gen += bytes(random_key_gen())

				status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, sector, key_gen, uid)
				if status == MIFAREReader.MI_OK:
				
					data_read =  MIFAREReader.MFRC522_Read(sector)
					card_information.append(data_read)
				else:
					return "Authentication error"
			
			MIFAREReader.MFRC522_StopCrypto1()

			try:
				name, auth_code, access_level = card_information

				name = "".join(hex(x)[2:] for x in name).strip("00")	

				auth_code =  "".join("{:02x}".format(x) for x in auth_code)
				access_level = "".join("{:02x}".format(x) for x in access_level)               
			except:
				continue_reading = False
				return "Malformed data"

			auth_code = auth_code + "".join("{:02x}".format(x) for x in key_gen)
			
			creds = {'uid': uid_hex[:8],
					 'username': name,
					 'authorization_code': auth_code,
					 'access_level': access_level}


			response = requests.post(url, data = creds)
			response = json.loads(response.text)


			continue_reading = False 
			time.sleep(1)
			GPIO.cleanup()
			return response["door_status"]