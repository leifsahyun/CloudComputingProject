#! /usr/bin/env python3
import threading
import asyncio
import time

from timeloop import Timeloop
from timeloop.job import Job

from datetime import timedelta

WAIT_SECONDS = 1

def foo():
    print(time.ctime())
    threading.Timer(WAIT_SECONDS, foo).start()
    
#foo()
print('hi')



class AsyncAgentPrototype():
    #both: 0
    #main: 1
    #self_check: 2
    def __init__(self,t1=None,t2=None):
        self.__t_main = Timeloop()
        self.__t_selfcheck = Timeloop()

        self._intv_main=t1
        self._intv_check=t2
   
    
    # @self.__t_main.job(interval=timedelta(seconds=_intv_main))
    # def sample_job_every_2s(self):
    #     print("2s job current time : {}".format(time.ctime()))

    # @self.__t_selfcheck.job(interval=timedelta(seconds=5))
    # def run_t(self):
    #         print("5s job current time : {}".format(time.ctime()))
    
    @staticmethod
    def __sec2int(sec):
        return timedelta(seconds=sec)

    def start(self,sel=0):
        if not sel==2: self.__t_main.start()
        if not sel==1: self.__t_selfcheck.start()

    def stop(self,sel=0):
        if not sel==2: self.__t_main.stop()
        if not sel==1: self.__t_selfcheck.stop()



    #assumption these event loops always hold ine job. R: get job id on attach
    def set_interval(self,t,sel=0):
        #TODO: clean this by making parameterizing loop.job
        if (not sel==2) and self.__t_main.jobs: self.__t_main.jobs[0].interval=self.__sec2int(t)
        if (not sel==1) and self.__t_selfcheck.jobs: self.__t_selfcheck.jobs[0].interval=self.__sec2int(t)



class AsyncAgent(Timeloop):
    
    def __init__(self,t1,t2,init_val=None):
        Timeloop.__init__(self)
        self.jobs=[None, None] #Timeloop.jobs is a list
        self.c=0
        self.set_main_job(self.fun1, 2)
        self.set_selfcheck_job(self.fun2, 3, 'werld')
        if init_val:
            #do routine
            self.fun2(init_val)

    # a wrapper to update job.arg before the job.execute is called
    # def update_args(self,job)

    def fun1(self): #use class member in the actual cls
        print("hi, "+ str(self.c))

    def fun2(self, txt):
        self.c+=1
        print("hi, " + txt)
    
    

    @staticmethod
    def __sec2int(sec):
        return timedelta(seconds=sec)
    
    # thse thread control functions uses a selector flag as commented below
    # to access the desried jobs
    #   both: 0
    #   main: 1
    #   self_check: 2
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



agent=AsyncAgent(2,3,'World')
agent.start()

while True:
  try:
    time.sleep(1)
  except KeyboardInterrupt:
    agent.stop()
    break

