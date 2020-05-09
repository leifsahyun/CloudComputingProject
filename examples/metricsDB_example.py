#! /usr/bin/env python3
from metricServer.DBClient import DBClient

example_entry = {'inst_id': 1, 'resp': 92, 'latency': 100, 'tail_lat': 145}
example_instance = {'provider': 'AWS', 'type': 's1', 'tier': 'micro',
        'cpu': 4, 'gpu': 1, 'memory': 16}


print("MySQL client Test") #use logging.DEBUG
cli=DBClient()

cli.help()
cli.add_instance_type(example_instance)
cli.add_entry(example_entry)

cli.show_instances()


print("")
print("Test get id from tag:")    
print(cli.get_inst_id("awss1micr"))

print("Test select last:")    
print(cli.pull_last("awst1micr"))
print(cli.pull_last(1))

print("Connection established")


cli.disconnect()

