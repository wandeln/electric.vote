import string
import random

def randomString(stringLength = 10):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))

def is_mobile(handler):
	return 'mobile' in handler.request.headers['User-Agent'].lower()
