#! /usr/bin/env python3

# gets all instance types from a driver passed to the function and saves them to files
#sizes contains instance types and sizes
#images contains available operating system images

from ArbitraryDriver import *
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import traceback
import json


def getDriverInstanceLists(cloudDriver):
	print("getting sizes")
	sizes = cloudDriver.list_sizes()
	with open("sizes.txt", "w") as sizeFile:
		for size in sizes:
			sizeFile.write(str(size)+"\n")
	print("sizes written to file")
	print("getting images")
	images = cloudDriver.list_images()
	with open("images.txt", "w") as imageFile:
		for image in images:
			imageFile.write(str(image)+"\n")
	print("images written to file")


# TODO: test case here. (probaly won't need)
# if __name__ == "__main__":
#     # execute only if run as a script
#     main(args)

def main(provider='AWS'):
	keys = None

	try:
		keyFile = open("keys/keys.json")
		stringRep = keyFile.read()
		keys = json.loads(stringRep)
	except:
		print("could not find or could not read keys/keys.json")
		exit()

	IMAGE_ID = 'ami-0fc20dd1da406780b'
	SIZE_ID = 't2.micro'

	print("started script")

	drv_cls = get_driver(Provider.EC2)
	driver = drv_cls(keys["EC2"]["id"], keys["EC2"]["key"], region='us-east-2')

	print("got driver")

	sizes = driver.list_sizes()
	print("got sizes:")

if __name__ == "__main__":
	main()