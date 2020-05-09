#! /usr/bin/env python3

# gets instance sizes 

# Since we will run this one or two times, the proccess is not parameterized or wrapped into methods

from ArbitraryDriver import *
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import traceback
import json, csv

keys = {}


#def set_keys():

try:
	keyFile = open("keys/keys.json")
	stringRep = keyFile.read()
	keys = json.loads(stringRep)
except:
	print("could not find or could not read keys/keys.json")
	exit()
#if google
try:
	g_key_file = open('keys/cloudmixer-b3c9c0df4051.json')
	keys['GCE'].update(json.load(g_key_file))
except:
	print("Error raeding the GCE keyfiile")


print("Acquiring instance information")
g_cls = get_driver(Provider.GCE)
g_driver = g_cls(keys["GCE"]["id"], keys["GCE"]["key"], project=keys['GCE']['project_id'])
g_sizes = g_driver.list_sizes()

# print("GCE  instance fields:")
# print(list(vars(g_sizes[0]).keys()))
# print(vars(g_sizes[0]))

aws_cls = get_driver(Provider.EC2)
aws_driver = aws_cls(keys["EC2"]["id"], keys["EC2"]["key"], region='us-east-2')
aws_sizes = aws_driver.list_sizes()

# print("AWS instance fields:")

# print(list(vars(aws_sizes[0]).keys()))
# print(vars(aws_sizes[0]))

#size_hdrs=list(vars(aws_sizes[0]).keys())
size_hdrs=['id','name','type','size', 'ram', 'cpu','disk','gpu', 'bandwidth', 'price']

print('writing files')


## Google Cloud Engine ##

csv_file = "gce_instances.csv"
try:
	with open(csv_file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=size_hdrs, extrasaction='ignore')
		writer.writeheader()
		for sz in g_sizes:	
			size_row=vars(sz)
			#print(size_row)
			ids=size_row['name'].split('-')
			size_row['type'] = ids[0]
			size_row['size'] = "-".join(ids[1:])
			
			size_row['gpu']=size_row['extra'].get('gpu',0)
			size_row['cpu']=size_row['extra'].get('guestCpus',0) #We ignore cpu type for now, this is why benchmarking is neccesary.

			size_row['provider'] = 'GCE'

		#GCE instances have attachable CPUS. LibCloud is note supporting these yet
		#It's filed name is probably 'accelerator'

		# compute:
		# * nvidia-tesla-t4
		# * nvidia-tesla-v100
		# * nvidia-tesla-p100
		# * nvidia-tesla-p4
		# * nvidia-tesla-k80
		# graphical:
		# * nvidia-tesla-t4-vws
		# * nvidia-tesla-p100-vws
		# * nvidia-tesla-p4-vws:
			
			
			writer.writerow(size_row)
except IOError:
    print("I/O error")

## Amazon Web Services

csv_file = "aws_instances.csv"
try:
	with open(csv_file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=size_hdrs, extrasaction='ignore')
		writer.writeheader()
		for sz in aws_sizes:
			size_row=vars(sz)
			
			ids = size_row['name'].split('.')
			size_row['type'] = ids[0]
			size_row['size'] = ids[1] 

			size_row['gpu'] = size_row['extra'].get('gpu',0)
			size_row['cpu'] = size_row['extra'].get('vcpu',0)

			size_row['provider'] = 'AWS'
			#print(size_row)
			writer.writerow(size_row)

except IOError:
    print("I/O error")