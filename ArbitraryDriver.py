from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeDriver
from libcloud.compute.base import Node
from libcloud.compute.base import KeyPair
from libcloud.compute.base import NodeAuthPassword
from enum import Enum
from recommendAgent.recommender import Recommender
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

	cloudMixerImageId = 'cloud-mixer-image-2'
	providers = [
		Provider.EC2,
		Provider.GCE
	]
	providerDrivers = {}
	providerKeys = {}
	sshKey = {}
	jobs = {} #this dict will contain job pids for each node name
	avail_sizes = []
	
	# The constructor accepts a keyfile path or a python dictionary of provider keys
	# See the keys/template_keys.json file for the format
	# After construction, the driver will be able to interface with any
	# provider listed in self.providers that it was given keys for
	def __init__(self, keys, provider=None, sizes=None):
		self.recommender = Recommender()
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
		if sizes is None:
			self.avail_sizes = self.list_sizes(provider)
	
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

	def list_nodes(self, provider=None):
		if provider is not None:
			return self.providerDrivers[provider].list_nodes()
		nodes = []
		for driver in self.providerDrivers.values():
			nodes.extend(driver.list_nodes())
		return nodes
		
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
		
	def create_managed_node(self, name, provider=None, size=None, image=None):
		if size is None:
			size_id = self.recommender.recommend(self.avail_sizes)
			for s in self.avail_sizes:
				if s.name == size_id:
					size = s
			if size is None:
				raise RuntimeError("recommended node size not in list of available node sizes")
			sizeDriver = size.driver
			if provider is None:
				for p in self.providerDrivers.keys():
					if self.providerDrivers[p] == sizeDriver:
						provider = p
		if image is None:
			image = self.get_image(self.cloudMixerImageId, provider)
		print("selected size: "+size.name)
		node = self.create_node(name, image, size, provider=provider)
		periodic = threading.Timer(60, self.check_and_migrate, kwargs={node: node})
		return node

	def check_and_migrate(self, node):
		print("checking for better instance")
		provider = None
		size = None
		size_id = self.recommender.recommend(self.avail_sizes)
		if size_id is not None and size_id != node.size.name:
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
		node = None
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
			node = self.providerDrivers[provider].create_node(name=name, image=image, size=size, ex_keyname=ex_keyname, ex_security_groups=ex_security_groups)
		elif provider==Provider.GCE:
			if location is None:
				location='us-central1-a'
			node = self.providerDrivers[provider].create_node(name=name, image=image, size=size, location=location)
		elif provider==Provider.AZURE_ARM:
			node = self.providerDrivers[provider].create_node(name=name, image=image, size=size, auth=NodeAuthPassword('mysecretpassword'), ex_resource_group=self.providerKeys["AZURE_ARM"]["resource_group"], ex_storage_account=self.providerKeys["AZURE_ARM"]["storage_account"], ex_network=keys["AZURE_ARM"]["virtual_network"])
		node.size = size
		return node
	
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
		return nodes_with_ips

	# Waits for an ssh connection to be successfully established, or a timeout to be reached
	# This is especially needed for Google Compute Engine because it requires significant start-up time after successfully returning from driver.wait_until_running before ssh attempts will succeed
	def wait_for_ssh(self, node, user='ubuntu'):
		temp_size = node.size
		node = self.wait_until_running(node)[0][0]
		node.size = temp_size
		print("Establishing ssh connection (will take a minute)")
		start = time.time()
		now = start
		success = False
		key = paramiko.rsakey.RSAKey.from_private_key_file(list(self.sshKey.values())[0])
		attempt = 1
		while now - start < 100 and not success:
			try:
				client = paramiko.client.SSHClient()
				client.set_missing_host_key_policy(paramiko.client.WarningPolicy)
				client.load_system_host_keys()
				client.connect(node.public_ips[0], username=user, pkey=key)
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
	# command: a string bash command
	# user: username and user space to execute the command under
	# callback: function to call on job completion; called with string lists stdout, stderr, and int exit status; each line of output is a string in the lists
	def run_job(self, node, command, user="ubuntu", callback=None, name=None):
		key = paramiko.rsakey.RSAKey.from_private_key_file(list(self.sshKey.values())[0])
		new_job = Job(command, node, key, callback=callback, name=name)
		if node.name in self.jobs:
			self.jobs[node.name].append(new_job)
		else:
			self.jobs[node.name] = [new_job]                
		return new_job.run(user)
			
	def destroy_node(self, node):
		return node.driver.destroy_node(node)

	def migrate_node(self, node, dest_provider, dest_size, name=None):
		if name is None:
			name = node.name+'-copy'
		client = paramiko.client.SSHClient()
		client.set_missing_host_key_policy(paramiko.client.WarningPolicy)
		client.load_system_host_keys()
		key = paramiko.rsakey.RSAKey.from_private_key_file(list(self.sshKey.values())[0])
		client.connect(node.public_ips[0], username='ubuntu', pkey=key)
		suspended_jobs = []
		if node.name in self.jobs:
			suspended_jobs = self.jobs[node.name]
			self.jobs[node.name] = []
		for job in suspended_jobs:
			if job.status == JobStatus.RUNNING:
				job.stop()
				#job.cb_thread.join()
				print(job.status)
				cmdin, cmdout, cmderr = client.exec_command('sudo criu dump --tree '+str(job.pid)+' -D /home/ubuntu/criu-chamber --shell-job')
				exit_code = cmdout.channel.recv_exit_status()
				if exit_code!=0:
					print(cmderr.readlines())
				if job.client:
					job.client.close()
				print("job '"+str(job.name)+"' suspended")
		print("all jobs on node "+str(node.name)+" suspended")
		newNode = self.create_managed_node(name=name, image=self.cloudMixerImageId, size=dest_size, provider=dest_provider)
		print("new node "+str(newNode.name)+" created")
		newNode = self.wait_for_ssh(newNode)
		cmdin, cmdout, cmderr = client.exec_command('rsync -a -e "ssh -i .ssh/static_pair.pem -o StrictHostKeyChecking=no" --super /home/ubuntu ubuntu@'+str(newNode.public_ips[0])+':/home')
		exit_code = cmdout.channel.recv_exit_status()
		if exit_code!=0:
			print(cmderr.readlines())
		print("synced persistent data and process images")
		client.close()
		self.destroy_node(node)
		print("original node destroyed")
		try:
			print("restarting processes")
			clientB = paramiko.client.SSHClient()
			clientB.set_missing_host_key_policy(paramiko.client.WarningPolicy)
			clientB.load_system_host_keys()
			clientB.connect(newNode.public_ips[0], username='ubuntu', pkey=key)
			cmdin, cmdout, cmderr = clientB.exec_command('sudo criu restore -D /home/ubuntu/criu-chamber --shell-job')
			exit_code = cmdout.channel.recv_exit_status()
			if exit_code!=0:
				print(cmderr.readlines())
			for job in suspended_jobs:
				job.node = newNode
				job.sshKey = key
				job.setup_client(user='ubuntu')
				job.stdout = job.client.exec_command('strace -p '+str(job.pid)+' -e write=1')[1]
				job.stderr = job.client.exec_command('strace -p '+str(job.pid)+' -e write=2')[1]
				job.status = JobStatus.RUNNING
				job.stop_event.clear()
				job.cb_thread = threading.Thread(target = job._wait_for_completion)
				if newNode.name in self.jobs:
					self.jobs[newNode.name].append(job)
				else:
					self.jobs[newNode.name] = [job]
				print("restored job "+str(job.name))
			print("processes restored")
		except Exception as e:
			print(traceback.format_exc())
		finally:
			return newNode

class JobStatus(Enum):
	NOT_RUNNING = 1
	RUNNING = 2
	FINISHED = 3

class Job:
	# Job constructor
	# command: bash command to run
	# node: a LibCloud Compute Node
	# sshKey: paramiko key to connect to node
	# name: name for this job (optional)
	# callback: function to run on job completion (defaults to printing job's stdout to local stdout)
	#       callback is called with string lists stdout, stderr, and int exit status; each line of output is a string in the lists
	def __init__(self, command, node, sshKey, name=None, callback=None):
		self.command = command
		self.node = node
		self.sshKey = sshKey
		self.status = JobStatus.NOT_RUNNING
		self.name = name
		self.callback = callback
		if self.name is None:
			self.name = command
		if self.callback is None:
			self.callback = self._default_job_completion
		self.cb_thread = None
		self.pid = None
		self.stdout = None
		self.stderr = None
		self.stop_event = threading.Event()

	def setup_client(self, user="ubuntu"):
		self.client = paramiko.client.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.client.WarningPolicy)
		self.client.load_system_host_keys()
		self.client.connect(self.node.public_ips[0], username=user, pkey=self.sshKey)

	# Runs this job on an arbitrary node
	# user: username and user space to execute the command under
	def run(self, user="ubuntu"):
		self.setup_client(user)
		print("Running job '%s'" % self.name)
		# Run the job
		print(self.name+" start time: "+str(time.time()))
		stdin, self.stdout, self.stderr = self.client.exec_command('echo $$ && exec '+self.command)
		self.pid = int(self.stdout.readline())
		self.cb_thread = threading.Thread(target = self._wait_for_completion)
		self.cb_thread.start()
		self.status = JobStatus.RUNNING
		return self.cb_thread

	def stop(self):
		if self.status != JobStatus.RUNNING:
			print("job '"+self.name+"' is not running")
			return
		self.status = JobStatus.FINISHED
		self.stop_event.set()
			

	def wait_for_completion(self):
		while self.status==JobStatus.RUNNING:
			pass
	
	def _wait_for_completion(self):
		while not self.stdout.channel.exit_status_ready() and self.status==JobStatus.RUNNING and not self.stop_event.is_set():
			pass
		if not self.stop_event.is_set():
			exit_status = self.stdout.channel.recv_exit_status()
			self.callback(self.stdout.readlines(), self.stderr.readlines(), exit_status)
		self.status = JobStatus.FINISHED
		self.client.close()

	def _default_job_completion(self, stdout, stderr, exit_status):
		print(self.name+" stop time: "+str(time.time()))
		if exit_status == 0:
			for line in stdout:
				print(line)
			if stderr != []:
				print("WARNINGS: %s" % str(stderr))
		else:
			raise RuntimeError("ERRORS: %s" % str(stderr))

	def __str__(self):
		return self.name+": command = "+self.command

	def __repr__(self):
		return str(self)
