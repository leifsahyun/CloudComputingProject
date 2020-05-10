from ArbitraryDriver import ArbitraryDriver
from libcloud.compute.types import Provider
import traceback
# An example of how to use the ArbitraryDriver class
# The provider_to_use variable tells the program which provider to use
provider_to_use = Provider.GCE
print("creating driver")
driver = ArbitraryDriver("keys/keys.json")
driver.load_pem_ssh_key("keys/static_pair.pem")
print("creating node")
# When using the ArbitraryDriver, the create_node function is the only
# function called differently between providers
if provider_to_use==Provider.EC2:
	node = driver.create_node(name='test-node1', image=driver.get_image('cloud-mixer-image-2', provider=Provider.EC2), size=driver.get_size('t2.micro', provider=Provider.EC2), provider=Provider.EC2)
elif provider_to_use==Provider.GCE:
	node = driver.create_node(name='test-node1', image=driver.get_image('cloud-mixer-image-2', provider=Provider.GCE), size=driver.get_size('n1-standard-1', provider=Provider.GCE), provider=Provider.GCE)
# Using try/except/finally ensures the node is destroyed when we are done
try:
	print("waiting for node to be ready")
	node = driver.wait_for_ssh(node)
	print("running sleep job")
	job = driver.run_job(node, "sleep 100 && echo complete")
	print("current jobs running on node:")
	print(repr(driver.jobs[node.name]))
	job.join()
	print("current jobs running on node:")
	print(repr(driver.jobs[node.name]))
except Exception as e:
	print(traceback.format_exc())
finally:
	print("destroying node")
	driver.destroy_node(node)
	print("node destroyed")
