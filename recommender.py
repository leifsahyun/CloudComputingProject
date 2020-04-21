#1 /usr/bin/env python3

from enum import Enum
import time, threading




units={}
#decorator for thimer threads
def threaded(fn, interval, unit='sec'):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class Recommender(object):


    # the reccommender has 2 timers one for the regular metrics data update
    # the second, optional one is to check if the current instance is able to satisfy requirements 
    def __init__(self, min_interval):
        self._update_t=None
        #self._update_t=threading.Timer(min_interval*60, hello)
        self._self_t=None
        self.metrics = {}
        self.parms = {}

        if True:  #check if paramters are utd
            self._update_t.start()

    #update timer methods

    def init_self_check(self, sec_interval):
        raise NotImplementedError

    # def start(self):
        # self._update_t(start)

    #def

    #consider making this a startic_method
    def get_candidates():    
    # look up 
        raise NotImplementedError

    def eval_score(self):
        pass




    # Evaluate if given
    def eval_pass(self):
        pass

    def set_reward_func(self,fun):
        #check if len(args) match
        self.eval=fun

    def self_check(self):
        pass

    def recommend(self,instances):
          
        scores = [key:self.eval(instance) for key, instance param in instances]

        best=min(dic, key=dic.get)
        print(" The instance " + instances[best]+" was evaluated as the best candidate")

        return instances[best] 

        #make this more analytic, with non-certain scores and close alternatives


    def eval(self,instance):
        #TODO make this a list comparison
        sum=0
        for key, param in self.metrics:
           sum+=instance[key].eval(stats)
        return sum

    def __del__(self): 
        print("Terminating Recommender...")
        self._update_t.cancel()
        self._self_t.cancel()









#this was going to inherit dict but appearently its
class Metric(object):
#1. Availability: percentage of successful requests
#2. Responsiveness: 99th percentile tail latency
#3. Capacity: # CPU, RAM, Storage (if applicable)
    
    class TYPE(Enum):
        MORE = 1
        LESS = 2
        BAND = 3
        BOOL = 4


    # t should be an array if type_id is BAND (and vice-versa) meaning metric should be between those
    def __init__(self, name, t, type_id=1,alpha=1 ):
        self.name = name
        self.treshold = t
        self.alpha = alpha
        if isinstance(t, list):
            self.set_type(Metric.TYPE.BAND)
        else:
            self.set_type(type_id)

    # this wrapper takes a Metric.TYPE or int
    # implemented for future work
    def set_type(self,type_id ):
        self._type=Metric.TYPE(type_id)
        
        if self._type == "more": #TODO: enumerate this
            self.error= lambda v: v-self.treshold
            self.op=lambda v: v>self.treshold

        elif self._type == "less":
            self.error= lambda v: self.treshold-v
            self.op=lambda v: v<self.treshold

        elif self._type == "band" :
            self.error= lambda v: v-sum(self.treshold)/2
            self.op=lambda v: self.treshold[0]<v<self.treshold[1]

        elif self._type == "bool":
            self.error= lambda v: int(v == self.treshold)
            self.op= lambda v: int(v == self.treshold)

        else:   
            print "Param type is invalid"
            pass #-1

    def eval(self, val):
        return self.error(val)*self.alpha

    #just a wrapper to have constant access to op
    #TODO: hide op and error from the user
    def eval_bool(self, val):
        return self.op(val)
        




# TODO: create instnace set intially, update if none/some 