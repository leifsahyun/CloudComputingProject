#! /usr/bin/env python3


from metricServer.DBClient import DBClient
from run_perfkit_and_parse_output import run_benchmarks

example_entry = {'inst_id': 1, 'resp': 92, 'latency': 100, 'tail_lat': 145}
example_instance = {'provider': 'AWS', 'type': 's1', 'tier': 'micro',
                    'cpu': 4, 'gpu': 1, 'memory': 16}

print("MySQL client Test")  # use logging.DEBUG
cli = DBClient()

cli.help()
cli.add_instance_type(example_instance)
cli.add_entry(example_entry)

cli.show_instances()

print("")
print("Test get id from tag:")
print(cli.get_inst_id("AWSc48xlge"))

print("Test select last:")
print(cli.pull_last("AWSc48xlge"))
print(cli.pull_last(1))

print(cli.get_alternatives('c4.8xlarge'))

print(cli.get_candidates({'ram':16000,'cpu':8}))

print("Connection established")

exit()
tests = [("GCP", "f1-micro"), ("AWS", "t2.micro")]

i = 6  # will use for ids
for provider, machine_type in tests:
    benchmarks = ["ping"]

    # run benchmark
    parsed_dict = run_benchmarks(provider, benchmarks, machine_type)
    if parsed_dict is None:
        print("Benchmarks failed.")
        continue

    # coremark cpu score. Will not use for now.
    # if "coremark" in benchmarks:
    #     coremark_scores = parsed_dict["coremark"]["Coremark Score"]
    #     avg_score = sum(coremark_scores) / len(coremark_scores)
    #     print("Average coremark: {}".format(avg_score))

    if "ping" in benchmarks:
        # get ping results average
        ping_scores = parsed_dict["ping"]["Average Latency"]
        avg_lat = sum(ping_scores) / len(ping_scores)
        ping_scores = parsed_dict["ping"]["Max Latency"]
        max_lat = sum(ping_scores) / len(ping_scores)

        # add entry
        entry = {'inst_id': i, 'resp': 100, 'latency': avg_lat, 'tail_lat': max_lat}
        cli.add_entry(entry)
    i += 1

cli.disconnect()
