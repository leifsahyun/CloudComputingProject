#! /usr/bin/env python3

from enum import Enum
import json


BAND_SUPPORTED = False

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
        tp = (Metric.TYPE.BAND if isinstance(t, list) else type_id) #overwrite
        self.set_type(tp)


    # value refoiramtting based on feature support 
    @staticmethod
    def __trshld_band_support(t):
         return (t if (BAND_SUPPORTED or not isinstance(t, list))  else t[0])
    
    @staticmethod
    def __type_band_support(type_id):
         return (Metric.__type_fmt(type_id) if BAND_SUPPORTED else Metric.TYPE.MORE)
    
    # process type selection (enum,int,str)
    @staticmethod
    def __type_fmt(type_id):
        return (Metric.TYPE[type_id.upper()] if isinstance(type_id, str) else Metric.TYPE(type_id))


    @classmethod
    def FromDict(cls,col):#collection
        name=col.get('name')
        if name:
            return Metric(col['name'], cls.__trshld_band_support(col['treshold']), col['type'],col['alpha'])
        else:
            return {Metric(name, cls.__trshld_band_support(vals['treshold']), vals.type, vals.alpha)for name,vals in col}
            

    @classmethod
    def FromList(cls,ls):
        if isinstance(ls, list):
            return list(map(Metric.FromDict,ls))
        else:
            raise ValueError("Invalid metric data")

    @classmethod
    def ExtractJSON(cls,data):
        #data=json.loads(JSONString)
        #for param in metrics #didn't decide if this is for a single obj or container
        #TODO: check if collection, check if has "name"
        par=data.get('metrics')
        if par:
            return Metric.FromList(par)
        else:
            return Metric.FromDict(data)
    
    @classmethod
    def FromJSONString(cls,jstr):
        return Metric.ExtractJSON(json.loads(jstr))
    
    @classmethod
    def FromJSONFile(cls,path):
        return Metric.ExtractJSON(json.load(open(path)))

    #Just a wrapper
    def toDict(self):
        if not BAND_SUPPORTED and self.TYPE == Metric.TYPE.BAND:
                t=t[0]
        return vars(self)

    def exportJSONString(self):
        
        return (json.dumps(self.toDict()))

    # this wrapper takes a Metric.TYPE or int
    # implemented for future work
    def set_type(self,type_id ):
        self._type=self.__type_band_support(type_id)
        
        if self._type == Metric.TYPE.MORE: #TODO: enumerate this
            self.error= lambda v: v-self.treshold
            self.op=lambda v: v>self.treshold

        elif self._type == Metric.TYPE.LESS:
            self.error= lambda v: self.treshold-v
            self.op=lambda v: v<self.treshold

        elif self._type == Metric.TYPE.BAND :
            self.error= lambda v: v-sum(self.treshold)/2
            self.op=lambda v: self.treshold[0]<v<self.treshold[1]

        elif self._type == Metric.TYPE.BOOL:
            self.error= lambda v: int(v == self.treshold)
            self.op= lambda v: int(v == self.treshold)

        else:   
            print("Param type is invalid")
            pass #-1

    def eval(self, val):
        return self.error(val)*self.alpha

    #just a wrapper to have constant access to op
    #TODO: hide op and error from the user
    def eval_bool(self, val):
        return self.op(val)