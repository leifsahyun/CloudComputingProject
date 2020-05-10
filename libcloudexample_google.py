from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import traceback
import json

keys = None

try:
	keyFile = open("keys/keys.json")
	keys = json.load(keyFile)
except:
	print("could not find or could not read keys/keys.json file")
	exit()

#if google
try:
	g_key_file = open('keys/cloudmixer-b3c9c0df4051.json')
	keys['GCE'].update(json.load(g_key_file))
except:
	print("Error raeding the GCE keyfiile")

IMAGE_NAME = 'debian-9-stretch-v20200309'
SIZE_NAME = 'n1-standard-1'

print("started script")
cls = get_driver(Provider.GCE)
#the key and id in the keyfile are for a service account that must be created through the GCE website
#the id is the service account email address, the key is the path to the json keyfile provided by GCE
driver = cls(keys["GCE"]["id"], keys["GCE"]["key"], project=keys['GCE']['project_id'], region='us-east-2')

print("got driver")

sizes = driver.list_sizes()
print("got sizes:")
for sz in sizes:
	print(vars(sz)["extra"])

print(list(vars(sizes[0]).keys()))
images = driver.list_images()
print("got images")


selectedSize = [s for s in sizes if s.name == SIZE_NAME][0]
selectedImage = [i for i in images if i.name == IMAGE_NAME][0]

print("preparing to acquire instance")
node = driver.create_node(name='test-node', image=selectedImage, size=selectedSize, location='us-central1-a')

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
