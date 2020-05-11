#! /usr/bin/env python3

from recommendAgent.recommender import Recommender
from recommendAgent.metrics import Metric


inst_a1={
    'name':'a1.large',
    'latency':70,
    'tail-latency':200,
    'cpu_perf':5,
    'availability':99,
    }


inst_e2={
    'name':'e2-highcpu',
    'latency':90,
    'tail-latency':200,
    'cpu_perf':5,
    'availability':99,
    }


inst_m1={
    'name':'m1.large',
    'latency':70,
    'tail-latency':200,
    'cpu_perf':5,
    'availability':99,
    }

print("Recommender")
print("Offline Example")

instances = {'a1.large':inst_a1,'e2-highcpu':inst_e2,'m1.large':inst_m1}

rec = Recommender()

rec.metrics=Metric.FromJSONFile('cfg/def_metrics.json')

print(rec.metrics)

print(rec.eval(inst_m1))
print(rec.eval_bool(inst_m1))
rec.candidates=instances.keys()
rec.instance_data=instances
print(rec.recommend())

print("Live Test")
print("metricServer must be running")
print("")
print("------------")
print("")

rec = Recommender(20,1,'c5.9xlarge')
rec.metrics=Metric.FromJSONFile('cfg/def_metrics.json')
print("current: "+ rec.current )
print("Initial candidates:",rec.candidates)

rec.request_alternatives(rec.current)
print("Inst data:" ,rec.instance_data)
rec.request_metrics()
print(rec.recommend())


#cand
