from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeAuthPassword
import traceback
import json

keys = None

try:
	keyFile = open("keys.json")
	stringRep = keyFile.read()
	keys = json.loads(stringRep)
except:
	print("failed to read key file")
	exit()

IMAGE_ID = 'Debian:debian-10-daily:10:0.20200321.207'
SIZE_ID = 'Basic_A0'
AUTH = NodeAuthPassword('mysecretpassword')

print("started script")

cls = get_driver(Provider.AZURE_ARM)
#azure requires more keys than the other cloud providers, first set up an app in azure and a client secret for it
#the tenant_id can be found by searching it in azure, as can the subscription_id, the key is the application_id you get when creating the application, the secret is the client secret you create
driver = cls(tenant_id=keys["AZURE_ARM"]["tenant_id"], subscription_id=keys["AZURE_ARM"]["subscription_id"], key=keys["AZURE_ARM"]["key"], secret=keys["AZURE_ARM"]["secret"], region="East US")

print("got driver")

sizes = driver.list_sizes()
selectedSize = [s for s in sizes if s.id == SIZE_ID][0]
selectedImage = driver.get_image(IMAGE_ID)

print("preparing to acquire instance")
#additional authentication required for creating a node: auth is a password defined per node that you will need to access node later
#resource_group is the name of a resource_group created through azure's interface, storage_account is the name of a storage account created through azure's interface, network is the name of a virtual network created through azure's interface
node = driver.create_node(name='test-node', image=selectedImage, size=selectedSize, auth=AUTH, ex_resource_group=keys["AZURE_ARM"]["resource_group"], ex_storage_account=keys["AZURE_ARM"]["storage_account"], ex_network=keys["AZURE_ARM"]["virtual_network"])

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
