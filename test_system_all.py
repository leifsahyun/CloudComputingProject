from ArbitraryDriver import ArbitraryDriver
from recommendAgent.metrics import Metric
from libcloud.compute.types import Provider
from libcloud.compute.types import NodeState
import traceback
import time
# An example of how to use the ArbitraryDriver class
# The provider_to_use variable tells the program which provider to use
print("creating driver")
driver = ArbitraryDriver("keys/keys.json")
driver.load_pem_ssh_key("keys/static_pair.pem")
print("setting up available size list")
google_offering = driver.get_size('n1-standard-1', provider=Provider.GCE)
amazon_offering = driver.get_size('t2.micro', provider=Provider.EC2)
driver.avail_sizes = [google_offering, amazon_offering]
print("will pick from following node sizes:")
for s in driver.avail_sizes:
        print(s.name)
        print("price: "+str(s.price))
print("setting evaluation metric to select cheapest node size")
cheap_metric = Metric("price", 0.02, type_id=Metric.TYPE.LESS)
driver.recommender.metrics = [cheap_metric]
print("creating node")
node = driver.create_managed_node('system-test-node')
print("node created")
# Using try/except/finally ensures the node is destroyed when we are done
try:
        print("waiting for node to be ready")
        node = driver.wait_for_ssh(node)
        print("running sleep job (200 seconds)")
        jobname = "sleep-job"
        job = driver.run_job(node, "sleep 200 && echo complete", name=jobname)
        print("current jobs running on node:")
        print(repr(driver.jobs[node.name]))
        print("setting up periodic migration check")
        driver.check_and_migrate(node)
        print("increasing amazon node price over time starting at "+str(time.time()))
        first = time.time()
        last = first
        now = first
        while now<first+100:
                now = time.time()
                if now>last+1:
                        amazon_offering.price = amazon_offering.price+0.001
                        driver.avail_sizes = [google_offering, amazon_offering]
                        last = now
        print("final prices at "+str(time.time()))
        print("amazon="+str(amazon_offering.price))
        print("google="+str(google_offering.price))
        input("press enter to continue to list running nodes and jobs")
        #driver.recommender.metrics = [Metric("price", 0.02, type_id=Metric.TYPE.MORE)]
        #print("triggering periodic migration check")
        #node = driver.check_and_migrate(node)
        print("running nodes:")
        nodes = driver.list_nodes()
        for n in nodes:
            if n.state == NodeState.RUNNING:
                print(n.name)
        print("current running jobs:")
        print(repr(driver.jobs))
        node_jobs = driver.jobs[node.name]
        input("press enter to end program")
except Exception as e:
        print(traceback.format_exc())
finally:
        print("destroying node")
        for n in nodes:
                driver.destroy_node(n)
        print("node destroyed")
        exit()
