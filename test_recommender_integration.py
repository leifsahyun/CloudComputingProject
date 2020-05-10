from ArbitraryDriver import ArbitraryDriver
from recommendAgent.metrics import Metric
from libcloud.compute.types import Provider
import traceback
# An example of how to use the ArbitraryDriver class
# The provider_to_use variable tells the program which provider to use
print("creating driver")
driver = ArbitraryDriver("keys/keys.json")
driver.load_pem_ssh_key("keys/static_pair.pem")
print("setting up available size list")
avail_sizes = []
avail_sizes.append(driver.get_size('t2.micro', provider=Provider.EC2))
avail_sizes.append(driver.get_size('n1-standard-1', provider=Provider.GCE))
driver.avail_sizes = avail_sizes
print("will pick from following node sizes:")
for s in avail_sizes:
    print(s.name)
print("setting evaluation metric to select cheapest node size")
driver.recommender.metrics = [Metric("price", 0, type_id=Metric.TYPE.LESS)]
print("creating node")
node = driver.create_managed_node('integration-test-node')
print("node created")
# Using try/except/finally ensures the node is destroyed when we are done
try:
	print("waiting for node to be ready")
	node = driver.wait_for_ssh(node)
	print("running sleep job")
	job = driver.run_job(node, "sleep 10 && echo complete")
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
