# code to copy over json file:
# scp -i test_25apr.pem ubuntu@ec2-54-91-148-57.compute-1.amazonaws.com:/tmp/perfkitbenchmarker/runs/b6d5c331/perfkitbenchmarker_results.json $HOME/

import json
import os
import sys
from os.path import expanduser, join, abspath
import re
import subprocess

home = expanduser("~")

# config perfkit variables
provider = "GCP"
benchmarks = ["coremark"]  # also coremark
machine_type = "f1-micro"

perfkit_command = "./pkb.py --cloud={} --benchmarks={} --machine_type={}".format(provider, ",".join(benchmarks), machine_type)

print("Running benchmarks: {}  on provider: {}  with machine type {}...".format(", ".join(benchmarks), provider, machine_type))
process = subprocess.Popen(perfkit_command.split(sep=" "),
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
output = stdout.decode('utf-8')

# parse perfkit output
matchObj = re.match(r'((.|\n)*)Publishing (\d+) samples to (.+)(.*?)', output, re.M|re.I)

perfkit_res_file = None
if matchObj:
    perfkit_res_file = matchObj.group(4).strip()
    print("Perfkit file found at: {}".format(perfkit_res_file))
else:
   print("Failed to parse perfkit output!!")
   print("Dump:")
   print(output)
   print("Stderr:")
   print(stderr)
   sys.exit()


# JSON file
json_filepath = abspath(perfkit_res_file)
f = open(json_filepath, "r")

# Reading from file
lines = f.readlines()
f.close()

parsed_dict = {}

# Iterating through the json
# list
for line in lines:
    res = json.loads(line)
    top_level_key = res["test"]
    metric = res["metric"]

    # every benchmark will have a dict entry with every metric as a list
    # example: parsed_dict["coremark"]["Coremark Score"]  returns a list
    if top_level_key in parsed_dict:
        if metric in parsed_dict[top_level_key]:
            parsed_dict[top_level_key][metric].append(res["value"])
        else:
            parsed_dict[top_level_key][metric] = [res["value"]]
    else:
        parsed_dict[top_level_key] = {metric: [res["value"]]}

if "coremark" in benchmarks:
    coremark_scores = parsed_dict["coremark"]["Coremark Score"]
    avg_score = sum(coremark_scores) / len(coremark_scores)
    print("Average coremark: {}".format(avg_score))

if "ping" in benchmarks:
    coremark_scores = parsed_dict["ping"]["Average Latency"]
    avg_score = sum(coremark_scores) / len(coremark_scores)
    print("Average Latency of Ping: {} ms".format(avg_score))

    coremark_scores = parsed_dict["ping"]["Max Latency"]
    avg_score = sum(coremark_scores) / len(coremark_scores)
    print("Average Max Latency of Ping: {} ms".format(avg_score))


# os.remove(json_filepath)
