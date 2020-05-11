#! /usr/bin/env python3

from enum import Enum
import operator
from functools import reduce
import time
import requests, json

from timeloop import Timeloop
from timeloop.job import Job
#timeloop does exactly that and more
#decorator for timer threads
# def threaded(fn, interval, unit="sec"):
#     def wrapper(*args, **kwargs):
#         thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
#         thread.start()
#         return thread
#     return wrapper

from datetime import timedelta


from recommendAgent.metrics import Metric

API_Key = "c3d4e51234sa5"

CHANGE_COST = 0 
CEIL_SCORE = 1000000

DEF_HOST_NAME = "localhost"
DEF_PORT_NUMBER = 8080

units={}


# class MetricsClient(object):
#     def __init__(self):
#     r = requests.post(url = API_ENDPOINT, data = data) 
     

# In multi-user case, a recommender resides in the server/cloud 
# and keeps track of
#           clients(jobs,current_instance(s),set(candidates),metrics)
# regularly requests the benchmark data for the set of candidates across all users.
# regularly checks the cur isnt for each job on the desired interval
# calculates reward for each job's instance & candidates on request
# A user usually has multiple Jobs; a Job has a Client (or User) and a Metrics

#class Recommender(MetricsClient): #MetricsClient takes over HTTP attributes
class Recommender(Timeloop):

    # the Recommender has 2 timers one for the regular metrics data update
    # the second, optional one is to check if the current instance is able to satisfy requirements 
    
    def __init__(self,t_update=20,t_self=0,init_val=None):
        Timeloop.__init__(self)
        self.jobs=[None, None] #Timeloop.jobs is a list
        self.need_eval=False

        # t_* values are in minutes
        self.set_main_job(self.request_metrics, t_update*60)
        self.set_selfcheck_job(self.self_check, t_self*60)
        
        self.init_metrics_client()
        #self.clients
        #self.jobs has a current instance, candidates, metrics and a clientowner
        self.candidates=[]
        self.metrics={} #have avarning for empty metrics
        self.instance_data={} #overall collection of instances


        if isinstance(init_val, str):
            self.set_current(init_val)
            #self.request_alternatives(init_val)
        elif isinstance(init_val, dict):
            self.request_candidates(init_val)


    ### HTTP Client ###
    def init_metrics_client(self):
        self.url='http://' + DEF_HOST_NAME + ":" + str(DEF_PORT_NUMBER)
        self.headers={"Accept": "application/json",
                "Content-Type": "application/json"}

    # send a POST request to the metricsServer with given payload
    #   return the response headers and content 
    def request(self, op, data_dict):
        # We would use routes to append self.url and process requests based on route instead of 
        # within POST data
        data_dict['request']=op
        r = requests.post(url = self.url,
            headers=self.headers, data = json.dumps(data_dict)) 
        data=(json.loads(r.content) if r.content else {})
        return r.headers, data

    # POST Request that contains the list of wanted instance types.
    # returns a list of dictionaries in the same order with {} for N/A ones.

    # check stale  before recommend and call this fcn?
    def request_metrics(self):
        
        #TODO: filter already-up-to-date instances
        resp_hdr,resp_data=self.request("metrics",{"instances":self.candidates})

        # case insensitivity for header keys is needed
        if resp_hdr["Content-Type"] == "application/json":
            if self.candidates == resp_data.keys():
               [self.instance_data.update(resp_data or {})]

    def request_alternatives(self, inst_size):  
        resp_hdr,resp_data=self.request("alternatives",{"instance":inst_size})
        if resp_hdr["Content-Type"] == "application/json":
            self.set_candidates(resp_data.get('instance_names'))

    #find matching instances from specs
    def request_candidates(self,dict_params):    
        resp_hdr,resp_data=self.request("candidates",{"params":dict_params})
        if resp_hdr["Content-Type"] == "application/json":
            self.set_candidates(resp_data.get('instance_names'))

      
    @staticmethod
    def __sec2int(sec):
        return timedelta(seconds=sec)


    ### Threading ###
    def start(self,sel=0):
        if not sel==2: self.jobs[0].start()
        if not sel==1: self.jobs[1].start()

    def stop(self,sel=0):
        if not sel==2: self.jobs[0].stop()
        if not sel==1: self.jobs[1].stop()

    def set_interval(self,t,sel=0):
        #TODO: clean this by making parameterizing loop.job
        if (not sel==2) and self.jobs[0].jobs: self.jobs[0].interval=self.__sec2int(t)
        if (not sel==1) and self.jobs[1].jobs: self.jobs[1].interval=self.__sec2int(t)
 
    #these could just be "in line"
    def set_main_job(self, func, t, *args, **kwargs):
        self.jobs[0] = Job(self.__sec2int(t), func, *args, **kwargs)

    def set_selfcheck_job(self, func, t, *args, **kwargs):
        self.jobs[1] = Job(self.__sec2int(t), func, *args, **kwargs)
    ### ###### ###

    # make sure teh candidates iterable has unqiue values and incldues the curretn instance
    def set_candidates(self,ls):
        
        self.candidates=list(set((ls if ls else [])+[self.current]))

    # need to reformat this: DONE, test
    #  instance[param] is an int/float, and self.metric is a dict of metrics
    def eval(self,instance): #use reward_func
        #TODO make this a list comparison
        #IF dict:
        # for name, metric in self.metrics:
        #    sum+=metric.eval(instance[name])
        #IF list:
        return sum(map(lambda m: (m.eval(instance.get(m.name)) if instance else CEIL_SCORE),self.metrics))
        #func is a reduce(lambda x,y: ..., list)
        # OR func(list)

    # Evaluate if given
    def eval_bool(self,instance):
        return all(map(lambda m:(m.eval_bool(instance.get(m.name)) if instance else False),self.metrics))


    def set_reward_func(self,fun):
        #check if len(args) match
        self.reward_func=fun

    def recommend(self):
    #   return self.recommend_from(self.instance_data)

    #def recommend_from(self,instances):
        #print(self.instance_data)
        #dict of instances(dict)
        scores = {key:self.eval(self.instance_data.get(key)) for key  in self.candidates}
        #list of instances(dict)
        #scores = {instance['name']:self.eval(instance) for instance  in instances}

        best=min(scores, key=scores.get)
        #dict of instances(dict)
        # instances[best]
        #list
        print(" The instance " + best +" was evaluated as the best candidate")

        return best
        #optional: save scores, store best in self.recommendation

        #make this more analytic, with non-certain scores and close alternatives
    
    def set_current(self,inst):
        self.current=inst
        self.request_alternatives(self.current)

    def self_check(self):
        self.need_eval=self.eval_bool(self.current)
        return self.need_eval

    def close(self): 
        print("Terminating Recommender...")
        self.stop()

    

#struct User{}

class RecommenderMaster(object):
    users=[]
    def __init__(self):
        raise NotImplementedError
