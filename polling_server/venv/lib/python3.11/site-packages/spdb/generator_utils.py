import hashlib
import base64
import random


def sha256(text: str) -> str:
    m = hashlib.sha256()
    m.update(text.encode())
    return m.hexdigest()


def b32encode(text: str) -> str:
	return base64.b32encode(text.encode()).decode()


def random_text(length: int=None) -> str:
	if length is None:
		length = random.randint(1, 64)

	BASE62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'

	return ''.join(random.SystemRandom().choices(BASE62, k=length)) 


def random_sha256() -> str:
	return sha256(random_text())

def random_b32() -> str:
	return b32encode(random_sha256())