import hashlib

def HashValue(args):
	hash = hashlib.sha1()
	hash.update(args.encode('utf-8'))
	return hash.hexdigest()
