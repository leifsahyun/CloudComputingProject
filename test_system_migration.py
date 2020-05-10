from ArbitraryDriver import ArbitraryDriver
from recommendAgent.metrics import Metric
from libcloud.compute.types import Provider
from libcloud.compute.types import NodeState
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
driver.recommender.metrics = [Metric("price", 0.02, type_id=Metric.TYPE.LESS)]
print("creating node")
node = driver.create_managed_node('integration-test-node')
if node.size is None:
	print("node size is None")
	raise RuntimeException()
print("node created")
# Using try/except/finally ensures the node is destroyed when we are done
try:
	print("waiting for node to be ready")
	node = driver.wait_for_ssh(node)
	if node.size is None:
		print("node size is None")
		raise RuntimeException()
	print("running sleep job (2 minutes)")
	jobname = "sleep-job"
	job = driver.run_job(node, "sleep 120 && echo complete", name=jobname)
	print("current jobs running on node:")
	print(repr(driver.jobs[node.name]))
	print("changing evaluation metric to select most expensive node size")
	driver.recommender.metrics = [Metric("price", 0.02, type_id=Metric.TYPE.MORE)]
	print("triggering periodic migration check")
	node = driver.check_and_migrate(node)
	if node.size is None:
		print("node size is None")
		raise RuntimeException()
	print("running nodes:")
	nodes = driver.list_nodes()
	for n in nodes:
            if n.state == NodeState.RUNNING:
                print(n.name)
	print("current running jobs:")
	print(repr(driver.jobs))
	node_jobs = driver.jobs[node.name]
	for j in node_jobs:
            if j.name == jobname:
                j.wait_for_completion()
                break
except Exception as e:
	print(traceback.format_exc())
finally:
	print("destroying node")
	driver.destroy_node(node)
	print("node destroyed")
