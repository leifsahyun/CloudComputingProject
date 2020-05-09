from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeDriver
from libcloud.compute.base import Node
from libcloud.compute.base import KeyPair
from libcloud.compute.base import NodeAuthPassword
#from recommender import Recommender
import subprocess
import traceback
import json
import time
import threading
import paramiko

# This class allows the user to acquire and use instances from
# arbitrary providers without worrying about the provider-specific
# functions and data
class ArbitraryDriver(NodeDriver):
	
	providers = [
		Provider.EC2,
		Provider.GCE
	]
	providerDrivers = {}
	providerKeys = {}
	sshKey = {}
	jobs = {} #this dict will contain job pids for each node name
	
	# The constructor accepts a keyfile path or a python dictionary of provider keys
	# See the keys/template_keys.json file for the format
	# After construction, the driver will be able to interface with any
	# provider listed in self.providers that it was given keys for
	def __init__(self, keys, provider=None):
		#self.recommender = Recommender(10)
		if provider is not None:
			print("Warning: setting up an ArbitraryDriver for a specific provider will make it unable to use other providers")
		if type(keys) is str:
			# Open the keyfile and retrieve provider keys
			try:
				keyFile = open(keys)
				stringRep = keyFile.read()
				self.providerKeys = json.loads(stringRep)
				keyFile.close()
			except Exception as e:
				raise type(e)("Failed to load json keyfile %s: %s" % (keys, str(e))) from e
		elif type(keys) is dict:
			# Load the dict of provider keys
			self.providerKeys = keys
		else:
			raise TypeError("keys parameter in ArbitraryDriver constructor must be a string file path or a dict")		
		# Setup the individual provider drivers
		if provider is not None:
			self.providerDrivers[provider] = self.setup_driver(provider)
		else:
			for p in self.providers:
				if p.name in self.providerKeys:
					self.providerDrivers[p] = self.setup_driver(p)
	
	def setup_driver(self, provider):
		cls = get_driver(provider)
		if provider == Provider.EC2:
			return cls(self.providerKeys["EC2"]["id"], self.providerKeys["EC2"]["key"], region='us-east-2')
		elif provider == Provider.GCE:
			#open the google keyfile to get the project id
			if not "project_id" in self.providerKeys["GCE"]:
				try:
					keyFile = open(self.providerKeys["GCE"]["key"])
					stringRep = keyFile.read()
					tempLoaded = json.loads(stringRep)
					self.providerKeys["GCE"]["project_id"] = tempLoaded["project_id"]
					keyFile.close()
				except Exception as e:
					raise type(e)("Failed to load Google keyfile %s: %s" % (self.providerKeys["GCE"]["key"], str(e))) from e
			return cls(self.providerKeys["GCE"]["id"], self.providerKeys["GCE"]["key"], project=self.providerKeys["GCE"]["project_id"])
		elif provider == Provider.AZURE_ARM:
			return cls(tenant_id=self.providerKeys["AZURE_ARM"]["tenant_id"], subscription_id=self.providerKeys["AZURE_ARM"]["subscription_id"], key=self.providerKeys["AZURE_ARM"]["key"], secret=self.providerKeys["AZURE_ARM"]["secret"], region="East US")
		else:
			raise RuntimeError("No defined implementation for the provider specified")
	
	def list_sizes(self, provider=None):
		if provider is not None:
			return self.providerDrivers[provider].list_sizes()
		print("Warning: without a driver parameter, the list_sizes function lists all available sizes across all providers. This takes some time and will generate a very large list.")
		sizes = []
		for driver in self.providerDrivers.values():
			sizes.extend(driver.list_sizes())
		return sizes
	
	def list_images(self, provider=None):
		if provider is not None:
			return self.providerDrivers[provider].list_images()
		print("Warning: without a driver parameter, the list_images function lists all available images across all providers. This takes some time and will generate a very large list.")
		images = []
		for driver in self.providerDrivers.values():
			images.extend(driver.list_images())
		return images
		
	def get_image(self, image_id, provider=None):
		# Some providers have implemented a quick get_image function,
		# try to get that first then do the naive approach like with get_size
		if provider is not None:
			try:
				return self.providerDrivers[provider].get_image(image_id)
			except:
				pass
		image = [i for i in self.list_images(provider) if i.name == image_id][0]
		if image is None:
			raise RuntimeError("Could not find image_id in provider(s)")
		else:
			return image
			
	def get_size(self, size_id, provider=None):
		size = [s for s in self.list_sizes(provider) if s.name == size_id][0]
		if size is None:
			raise RuntimeError("Could not find size_id in provider(s)")
		else:
			return size
	
	# Loads a *.pem ssh key file that will be used to access nodes
	# generated by this driver.
	def load_pem_ssh_key(self, filePath, name=None):
		# check that the file is accessible
		f = open(filePath)
		f.close()
		# check that the file is *.pem
		if not filePath.endswith(".pem"):
			raise ValueError("File must be *.pem")
		if name is None:
			name = filePath[filePath.rfind("/")+1:-4]
		self.sshKey[name] = filePath
		
	def create_managed_node(self, name, provider=None, slos={}):
		if provider is None:
			size = None
			#size = self.recommender.recommend(self.list_sizes())
			sizeDriver = size.driver
			for p in self.providerDrivers.keys():
				if self.providerDrivers[p] == sizeDriver:
					provider = p
		node = self.create_node(name, cloudMixerImage, size, provider=provider)
		periodic = threading.Timer(60, self.check_and_migrate, kwargs={node: node, slos: slos})
		return node

	def check_and_migrate(self, node, slos):
		provider = None
		size = None
		#size = self.recommender.recommend(self.list_sizes())
		if size is not None and size.name != node.size.name:
			sizeDriver = size.driver
			for p in self.providerDrivers.keys():
				if self.providerDrivers[p] == sizeDriver:
					provider = p
			return self.migrate_node(node, provider, size)
		else:
			return node
		
	
	def create_node(self, name, image, size, provider=None, location=None, ex_keyname=None, ex_security_groups=None):
		if provider is None:
			raise RuntimeError("Node must be created with a specified provider using this function; use create_managed_node to create a node using SLOs")
			return None
		if not provider in self.providerDrivers.keys():
			raise RuntimeError("No defined implementation for the provider specified")
		if provider==Provider.EC2:
			if ex_keyname is None:
				keypairs = self.providerDrivers[Provider.EC2].list_key_pairs()
				for k in keypairs:
					if k.name in self.sshKey:
						ex_keyname = k.name
						break
				if ex_keyname is None:
					raise RuntimeError("Could not find a ssh keypair that is both loaded in this driver and registered with Amazon")
			if ex_security_groups is None:
				ex_security_groups=["default"]
			return self.providerDrivers[provider].create_node(name=name, image=image, size=size, ex_keyname=ex_keyname, ex_security_groups=ex_security_groups)
		elif provider==Provider.GCE:
			if location is None:
				location='us-central1-a'
			return self.providerDrivers[provider].create_node(name=name, image=image, size=size, location=location)
		elif provider==Provider.AZURE_ARM:
			return self.providerDrivers[provider].create_node(name=name, image=image, size=size, auth=NodeAuthPassword('mysecretpassword'), ex_resource_group=self.providerKeys["AZURE_ARM"]["resource_group"], ex_storage_account=self.providerKeys["AZURE_ARM"]["storage_account"], ex_network=keys["AZURE_ARM"]["virtual_network"])
	
	def wait_until_running(self, nodes):
		driver_node_associations = {}
		nodes_with_ips = []
		if type(nodes) is Node:
			nodes = [nodes]
		for n in nodes:
			if n.driver in driver_node_associations:
				driver_node_associations[n.driver].append(n)
			else:
				driver_node_associations[n.driver] = [n]
		for driver in driver_node_associations:
			nodes_with_ips.extend(driver.wait_until_running(driver_node_associations[driver]))
			if type(driver) == get_driver(Provider.GCE):
				for n in driver_node_associations[driver]:
					self.wait_for_GCE_node(n)
		return nodes_with_ips

	### ! Google Compute Engine requires significant start-up time after successfully returning from driver.wait_until_running before ssh attempts will succeed. This method waits for that to happen.
	def wait_for_GCE_node(self, node):
		print("Establishing ssh connection (will take a minute)")
		start = time.time()
		now = start
		success = False
		googleSshKey = list(self.sshKey.keys())[0]
		key = paramiko.rsakey.RSAKey.from_private_key_file(list(self.sshKey.values())[0])
		attempt = 1
		while now - start < 100 and not success:
			try:
				client = paramiko.client.SSHClient()
				client.set_missing_host_key_policy(paramiko.client.WarningPolicy)
				client.load_system_host_keys()
				client.connect(node.public_ips[0], username='static_pair', pkey=key)
				client.close()
				success = True
			except Exception as e:
				print("attempt "+str(attempt)+" failed to connect")
			now = time.time()
			attempt = attempt+1
		if success:
			print("ssh connection established")
			return node
		else:
			raise IOError("timeout establishing ssh connection")
	
	# Runs an arbitrary job (a bash command) on an arbitrary node
	# node: a LibCloud Compute Node
	# job: a string bash command
	# silent: whether to print info about the job
	# user: username and user space to execute the command under
	# callback: function to call on job completion; called with string lists stdout, stderr, and int exit status; each line of output is a string in the lists
	def run_job(self, node, job, silent=False, user=None, callback=None):
		if not silent:
			print("Running job '%s'" % job)
		if callback is None and not silent:
			callback = self.default_job_completion
		elif callback is None and silent:
			callback = lambda arg1, arg2: True
		if user is None:
			if type(node.driver) == get_driver(Provider.GCE):
				user = list(self.sshKey.keys())[0]
			elif type(node.driver) == get_driver(Provider.EC2):
				user = "ubuntu"
		if user is None:
			raise RuntimeError("Must define user parameter if not not running on a GCE or EC2 node")
		client = paramiko.client.SSHClient()
		client.set_missing_host_key_policy(paramiko.client.WarningPolicy)
		client.load_system_host_keys()
		key = paramiko.rsakey.RSAKey.from_private_key_file(list(self.sshKey.values())[0])
		client.connect(node.public_ips[0], username='static_pair', pkey=key)
		def wait_for_completion():
			exit_status = stdout.channel.recv_exit_status()
			result = stdout.readlines()
			result_err = stdout.readlines()
			callback(result, result_err, exit_status)
			client.close()
		# Run the job
		print("job start "+str(time.time()))
		stdin, stdout, stderr = client.exec_command(job)
		cb_thread = threading.Thread(target = wait_for_completion)
		cb_thread.start()
		return cb_thread
		
	def default_job_completion(self, stdout, stderr, exit_status):
		print("job returned "+str(time.time()))
		if exit_status == 0:
			for line in stdout:
				print(line)
			if stderr != []:
				print("WARNINGS: %s" % str(stderr))
		else:
			raise RuntimeError("ERRORS: %s" % str(stderr))
                
			
	def destroy_node(self, node):
		return node.driver.destroy_node(node)

	def migrate_node(self, node, dest_provider, dest_size, name=None):
		if name is None:
			name = node.name+'-copy'
		client = paramiko.client.SSHClient()
		client.load_system_host_keys()
		client.connect(node.public_ips[0], username='ubuntu', key_filename=list(self.sshKey.values())[0])
		if node.name in self.jobs:
			for job in self.jobs[node.name]:
				cmdin, cmdout, cmderr = client.exec_command('sudo criu dump --tree '+job+' -D /home/ubuntu/criu-chamber')
		print("jobs on node "+node.name+" suspended")
		newNode = self.create_node(name=name, image='cloud-mixer-image-2', size=dest_size, provider=dest_provider)
		print("new node "+name+" created")
		newNode = self.wait_until_running([newNode])[0][0]
		cmdin, cmdout, cmderr = client.exec_command('rsync -a -e "ssh -i .ssh/static_pair.pem" --super /home/ubuntu ubuntu@'+newNode.public_ips[0]+':/home')
		print("synced persistent data and process images")
		client.close()
		self.destroy_node(node)
		print("original node destroyed")
		try:
			print("restarting processes")
			clientB = paramiko.client.SSHClient()
			clientB.load_system_host_keys()
			clientB.connect(newNode.public_ips[0], username='ubuntu', key_filename=list(self.sshKey.values())[0])
			clientB.exec_command('sudo criu restore -d -D /home/ubuntu/criu-chamber')
		except Exception as e:
			print(traceback.format_exc())
		finally:
			return newNode

