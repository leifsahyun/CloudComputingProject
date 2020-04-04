from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import subprocess
import traceback
import json
import time

providerKeys = None
sshKeys = {
"static_pair": "keys/static_pair.pem"
}
sshUsername = None

try:
	keyFile = open("keys/keys.json")
	stringRep = keyFile.read()
	providerKeys = json.loads(stringRep)
except:
	print("failed to read key file")
	exit()

IMAGE_NAME = 'debian-9-stretch-v20200309'
SIZE_NAME = 'n1-standard-1'
#this is the job to run on the remote server as a shell command
JOB = "date"

print("started script")

cls = get_driver(Provider.GCE)
#the key and id in the keyfile are for a service account that must be created through the GCE website
#the id is the service account email address, the key is the path to the json keyfile provided by GCE
driver = cls(providerKeys["GCE"]["id"], providerKeys["GCE"]["key"], project='airy-strength-272318')

print("got driver")

sizes = driver.list_sizes()
print("got sizes")
images = driver.list_images()
print("got images")

selectedSize = [s for s in sizes if s.name == SIZE_NAME][0]
selectedImage = [i for i in images if i.name == IMAGE_NAME][0]

print("loading key pair for ssh")
#Getting a list of key pairs is not implemented for Google Compute Engine in Libcloud, so it is necessary to specify a single keypair
pairName = list(sshKeys.keys())[0]
pemFile = sshKeys[pairName]
sshUsername = pairName

print("preparing to acquire instance")
node = driver.create_node(name='test-node', image=selectedImage, size=selectedSize, location='us-central1-a')



try:
	print("waiting for node to be ready")
	print(node)
	node_with_ip = driver.wait_until_running([node])
	node = node_with_ip[0][0]
	node_ip = node.public_ips[0]
	print(node)
	print(node_ip)
	
	### ! Google Compute Engine requires significant start-up time after successfully returning from driver.wait_until_running before ssh attempts will succeed
	print("Establishing ssh connection (will take a minute)")
	start = time.time()
	now = start
	success = False
	while now - start < 100 and not success:
		ssh = subprocess.Popen(["ssh", "-i", pemFile, "-o", "StrictHostKeyChecking=no", "%s@%s" % (sshUsername, node_ip), "true;"],
					shell=False,
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE)
		while ssh.poll() is None:
			now = time.time()
			if now-start>100:
				raise IOError("timeout establishing ssh connection")
		if ssh.poll() == 0:
			success = True
			break
		now = time.time()
	if success:
		print("ssh connection established")
	else:
		raise IOError("timeout establishing ssh connection")
		
		
		
	### From this point on, code is identical to running_jobs_amazon.py
	print("Making call to cloud server to retrieve date")
	ssh = subprocess.Popen(["ssh", "-i", pemFile, "-o", "StrictHostKeyChecking=no", "%s@%s" % (sshUsername, node_ip), JOB],
					shell=False,
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE)
	# Run the job until it completes or a 100 second timeout
	start = time.time()
	now = start
	last = now
	while ssh.poll() is None and now-start<100:
		now = time.time()
		#periodic printing to show the script is alive
		if now-last > 5:
			print("waiting for job to complete")
			last = now
	if ssh.poll() is None:
		print("job timed out")
		ssh.kill()
	else:
		print("job finished")
	result = ssh.stdout.readlines()
	if result == []:
		error = ssh.stderr.readlines()
		print("ERROR: %s" % error)
	else:
		print("result:")
		print(result)

except Exception as e:
	print(traceback.format_exc())
finally:
	print("destroying node")
	driver.destroy_node(node)
