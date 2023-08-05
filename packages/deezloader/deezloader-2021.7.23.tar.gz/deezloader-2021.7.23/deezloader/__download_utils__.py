#!/usr/bin/python3

from hashlib import md5 as __md5

from binascii import (
	a2b_hex as __a2b_hex,
	b2a_hex as __b2a_hex
)

from Crypto.Cipher.Blowfish import (
	new as __newBlowfish,
	MODE_CBC as __MODE_CBC
)

from Crypto.Cipher.AES import (
	new as __newAES,
	MODE_ECB as __MODE_ECB
)

__secret_key = "g4el58wc0zvf9na1"
__idk = __a2b_hex("0001020304050607")
__secret_key2 = b"jo6aey6haid2Teih"

def md5hex(data: str):
	hashed = __md5(
		data.encode()
	).hexdigest()

	return hashed

def genurl(md5, quality, ids, media):
	data = b"\xa4".join(
		a.encode()
		for a in [
			md5, quality, ids, media
		]
	)

	data = b"\xa4".join(
		[
			md5hex(data).encode(), data
		]
	) + b"\xa4"

	if len(data) % 16:
		data += b"\x00" * (16 - len(data) % 16)

	c = __newAES(__secret_key2, __MODE_ECB)

	media_url = __b2a_hex(
		c.encrypt(data)
	).decode()

	return media_url

def __calcbfkey(songid):
	h = md5hex(songid)

	bfkey = "".join(
		chr(
			ord(h[i]) ^ ord(h[i + 16]) ^ ord(__secret_key[i])
		)

		for i in range(16)
	)

	return bfkey

def __blowfishDecrypt(data, key):
	c = __newBlowfish(
		key.encode(), __MODE_CBC, __idk	
	)

	return c.decrypt(data)

def decryptfile(content, key, name):
	key = __calcbfkey(key)
	decrypted_audio = open(name, "wb")

	for data in content:
		if len(data) == (2048 * 3):
			data = __blowfishDecrypt(
				data[:2048], key
			) + data[2048:]

		decrypted_audio.write(data)

	decrypted_audio.close()