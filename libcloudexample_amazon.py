from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import traceback
import json

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
#print(sizes)
print(list(vars(sizes[0]).keys()))
print(vars(sizes[0]))

images = driver.list_images()
selectedSize = [s for s in sizes if s.id == SIZE_ID][0]
selectedImage = [i for i in images if i.id == IMAGE_ID][0]

print("preparing to acquire instance")
node = driver.create_node(name='test-node', image=selectedImage, size=selectedSize)

try:
	print("waiting for node to be ready")
	print(node)
	driver.wait_until_running([node])
	print(node)

except Exception as e:
	print(traceback.format_exc())
finally:
	print("destroying node")
	driver.destroy_node(node)

###
#size = [s for s in sizes if s.id == 'performance1-1'][0]
#image = [i for i in images if 'Ubuntu 18.04' in i.name][0]

#node = driver.create_node(name='libcloud', size=size, image=image)
#print(node)
###
