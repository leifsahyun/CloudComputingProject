# code to copy over json file:
# scp -i test_25apr.pem ubuntu@ec2-54-91-148-57.compute-1.amazonaws.com:/tmp/perfkitbenchmarker/runs/b6d5c331/perfkitbenchmarker_results.json $HOME/

import json
import os
from os.path import expanduser, join, abspath

home = expanduser("~")

benchmarks = ["ping"]

# config file variables
pem_key_path = "$HOME/Downloads/test_25apr.pem"
dest_path = home
perfkit_res_file = "/tmp/perfkitbenchmarker/runs/f06e3be0/perfkitbenchmarker_results.json"
instance_url = "ubuntu@ec2-54-91-148-57.compute-1.amazonaws.com"

# create the copy command
command = "scp -i {} {}:{} {}".format(pem_key_path, instance_url, perfkit_res_file, dest_path)

print("Obraining results from remote server...")
stream = os.popen(command)
output = stream.read()

# JSON file
json_filepath = abspath(join(dest_path, 'perfkitbenchmarker_results.json'))
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
