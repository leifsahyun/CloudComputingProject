#This script allocates an ubuntu t2 micro instance on Amazon EC2 and
#runs a job [JOB] on it defined as a shell command, currently set to
#the date command. Make sure to create a keys.json file before running.
#Also make sure to create a keypair pem file and register the keypair
#with AWS. If the keypair you use is not called 'static_pair', add it
#to the sshKeys list.
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import traceback
import json
import subprocess

providerKeys = None
sshKeys = {
"static_pair": "static_pair.pem"
}

try:
	keyFile = open("keys.json")
	stringRep = keyFile.read()
	providerKeys = json.loads(stringRep)
except:
	print("failed to read key file")
	exit()

IMAGE_ID = 'ami-0fc20dd1da406780b'
SIZE_ID = 't2.micro'
#this is the job to run on the remote server as a shell command
JOB = "date"

print("started script")

cls = get_driver(Provider.EC2)
driver = cls(providerKeys["EC2"]["id"], providerKeys["EC2"]["key"], region='us-east-2')

print("got driver")

sizes = driver.list_sizes()
print("got sizes")
images = driver.list_images()
print("got images")

selectedSize = [s for s in sizes if s.id == SIZE_ID][0]
selectedImage = [i for i in images if i.id == IMAGE_ID][0]

print("loading key pair for ssh")
keypairs = driver.list_key_pairs()
pair = None
pemFile = None
for k in keypairs:
	if k.name in sshKeys:
		pair = k
		pemFile = sshKeys[k.name]
if pair is not None:
	print(pair)
	print(pemFile)
else:
	print("ERROR: Could not find ssh key")
	exit()

print("preparing to acquire instance")
node = driver.create_node(name='test-node', image=selectedImage, size=selectedSize, ex_keyname=pair.name, ex_security_groups=["launch-wizard-1"])

try:
	print(node)
	print("waiting for node to be ready")
	node_with_ip = driver.wait_until_running([node])
	node = node_with_ip[0][0]
	node_ip = node_with_ip[0][1][0]
	print(node)
	print(node_ip)
	print("Making call to cloud server to retrieve date")
	
	#from https://gist.github.com/bortzmeyer/1284249
	#the only simple way to do ssh in Python
	ssh = subprocess.Popen(["ssh", "-i", pemFile, "-o", "StrictHostKeyChecking=no", "ubuntu@%s" % node_ip, JOB],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
	#There is a known issue with using Popen.wait when stdout is specified in the
	#Popen constructor, see https://docs.python.org/2/library/subprocess.html
	#however, without this call, stdout.readlines() blocks because the pipe
	#remains open. At some point in the future, we will want to find a different
	#way to do this.
	ssh.wait()
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


