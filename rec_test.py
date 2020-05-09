#! /usr/bin/env python3

from recommendAgent.recommender import Recommender
from recommendAgent.metrics import Metric


dum_instance={
    'latency':70,
    'tail-latency':200,
    'capacity':5,
    'availability':99,
    }

rec = Recommender()

rec.metrics=Metric.FromJSONFile('cfg/def_metrics.json')

print(rec.metrics)

rec.eval(dum_instance)
print(rec.eval(dum_instance))