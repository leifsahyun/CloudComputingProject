
#gets all instance types from a driver passed to the function and saves them to files
#sizes contains instance types and sizes
#images contains available operating system images
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
