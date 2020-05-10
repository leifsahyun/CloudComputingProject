#! /usr/bin/env python3

from enum import Enum
import operator
from functools import reduce
import time, threading
import requests, json

from recommendAgent.metrics import Metric

API_Key = "c3d4e51234sa5"

DEF_HOST_NAME = "localhost"
DEF_PORT_NUMBER = 8080

units={}

_sample_sz_name = 'a1.2xlarge'
_sample_candidates = ['a1.4xlarge','a1.large', 'a1.medium']

#decorator for timer threads
def threaded(fn, interval, unit="sec"):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

# class MetricsClient(object):
#     def __init__(self):
#     r = requests.post(url = API_ENDPOINT, data = data) 
     


#class Recommender(MetricsClient):
class Recommender(object):

    # the reccommender has 2 timers one for the regular metrics data update
    # the second, optional one is to check if the current instance is able to satisfy requirements 
    def __init__(self, min_interval=1):
        self._update_t=None
        #self._update_t=threading.Timer(min_interval*60, hello)
        self._self_t=None
        self.metrics = {}
        self.params = {}
        self.candidates=[]

        if True:  #check if paramters are utd
            self.start()

    #update timer methods

    def init_self_check(self, sec_interval):
        raise NotImplementedError

    def start(self):
        if self._update_t: self._update_t.start()

    # POST Request that contains the list of wanted instance types.
    # returns a list of dictionaries in the same order with {} for N/A ones.

    # check stale  before recommend and call this fcn?
    def request_metrics(self):
        
        
        url=DEF_HOST_NAME + ":" + DEF_PORT_NUMBER
        headers={"Accept": "application/json",
                "Content-Type": "application/json"}
        
        #TODO: filter already-up-to-date instances
        predata={"intances":self. candidates}

        r = requests.post(url = url,headers=headers, data = json.dumps(predata)) 
        #TODO: match reveiced instances wit requested?

        resp_hdr=r.headers
        resp_data=json.loads(r.content)

        # case insensitivity for header keys is needed
        if resp_hdr["Content-Type"] == "application/json":
            if self.candidates == resp_data.keys() :

                self.metrics.update(json.loads(r.content))

                
        # check content type. etc.
        # small TODO: purge non-canditadates

        # process request

    #consider making this a staticmethod
    def get_candidates(self):    
    # look up 
        raise NotImplementedError

  
    # need to reformat this: DONE, test
    #  instance[param] is an int/float, and self.metric is a dict of metrics
    def eval(self,instance): #use reward_func
        #TODO make this a list comparison
        #IF dict:
        # for name, metric in self.metrics:
        #    sum+=metric.eval(instance[name])
        #IF list:
        return sum(map(lambda m:m.eval(instance[m.name]),self.metrics))
        #func is a reduce(lambda x,y: ..., list)
        # OR func(list)

    # Evaluate if given
    def eval_bool(self,instance):
        return all(map(lambda m:m.eval_bool(instance[m.name]),self.metrics))


    def set_reward_func(self,fun):
        #check if len(args) match
        self.reward_func=fun

    def self_check(self):
        pass

    def recommend(self,instances):
        
        #dict of instances(dict)
        #scores = {key:self.eval(instance) for key, instance  in instances}
        #lit of instances(dict)
        scores = {instance.name:self.eval(instance) for instance  in instances}

        best=min(scores, key=scores.get)
        #dict of instances(dict)
        # instances[best]
        #list
        print(" The instance " + best+" was evaluated as the best candidate")

        return best

        #make this more analytic, with non-certain scores and close alternatives



    def __del__(self): 
        print("Terminating Recommender...")
        if self._update_t: self._update_t.cancel()
        if self._self_t: self._self_t.cancel()



        

# TODO: create instnace set intially, update if none/some 


#struct User{}

class RecommenderMaster(object):
    users=[]
    def __init__(self):
        raise NotImplementedError
