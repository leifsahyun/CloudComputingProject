#! /usr/bin/env python3

from recommendAgent.recommender import Recommender
from recommendAgent.metrics import Metric


inst_a1={
    'instance_id':'a1.large',
    'latency':70,
    'tail-latency':200,
    'capacity':5,
    'availability':99,
    }


inst_e2={
    'instance_id':'e2-highcpu',
    'latency':90,
    'tail-latency':200,
    'capacity':5,
    'availability':99,
    }


inst_m1={
    'instance_id':'m1.large',
    'latency':70,
    'tail-latency':200,
    'capacity':5,
    'availability':99,
    }

instances = [inst_a1,inst_e2,inst_m1]

rec = Recommender()

rec.metrics=Metric.FromJSONFile('cfg/def_metrics.json')

print(rec.metrics)

print(rec.eval(inst_m1))
print(rec.eval_bool(inst_m1))

print(rec.recommend(instances))