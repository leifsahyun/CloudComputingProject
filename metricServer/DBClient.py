#! /usr/bin/env python
#TODO: later, narrow down 
import mysql.connector as connector
import getpass
from tabulate import tabulate


#move this, MEH
dbx = None
curs = None 
#TODO:  list of default adresses to fall back to


BYTE_FACTOR = 1024
#yep a MACRO DICT
FACTOR={'cpu':1,'ram':1024,'disk':100}
#for value test
MAX=str(1.15)
MIN=str(0.86)

DEF_USR = 'perfkit'
DEF_HOST = '127.0.0.1'
DEF_DB = 'metricsDB'

BENCH_TABLE="benchmark"
INST_TABLE="sizes_lite"
class DBClient(object):

    inst_headers=['id' , 'tag', 'provider', 'type', 'tier', 'cpu', 'gpu', 'memory']
    bench_headers=['id', 'inst_id', 't_entry', 'resp', 'latency', 'tail_lat']
    descriptors=['Field', 'Type', 'Null', 'Key', 'Default','Extra']

    def __init__(self, *args):
        if args == (): args = DEF_USR
        self.curs = None
        self.dbx=self.connect_db(args) #or *args?
        

    ### Access
    def connect_db(self, usr=DEF_USR, h=DEF_HOST, db=DEF_DB ):
        
        #passport prompt could be tied to an arg, and fired if only one isn't passed
     

        '''
        # ALTERNATIVE #
        config = {
            'user': 'usr',
            'password': 'password',
            'host': '127.0.0.1',
            'database': 'employees',
            'raise_on_warnings': True
        }

        dbx = connector.connect(**config)
        ''' 
        
        #Try connection with the provided values
        while not self.curs:
            
            if __name__ == "__main__": #not intended for production, delete
                p='0202duolc'
            else:
                try:
                    p = getpass.getpass() #backwards pass thru 
                    # 0202doulc
                except KeyboardInterrupt:
                    exit()
                else:
                    pass
            try:
                p='0202duolc'
                dbx = connector.connect(user=usr, password=p,
                                host=h,database=db,
                                auth_plugin='mysql_native_password')
                #cursor.execute("SELECT * FORM employees")   # Syntax error in query
            
            except connector.Error as err:
                if err.errno == connector.errorcode.CR_UNKNOWN_HOST:
                    print("Unknown host")
                elif err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Wrong credentials")
                elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
            else:
                self.curs = dbx.cursor(buffered=True)
                self.dict_curs = dbx.cursor(dictionary=True)

                return dbx


    #### DATABASE OPS

    # receive an entry, validate and insert
    # entry should have 

    # example: aDBCleint.add_entry(Perfkit.do_bench_stuff())
    
        
        #CONSIDER: having tables for each instance type
        #entry_data = {}
    def add_entry(self, entry):
        
        add_cmd = ("INSERT INTO " + BENCH_TABLE +
               "(inst_id, resp, latency, tail_lat) " #do +[field for field in <names_list>] + ?
               "VALUES (    %(inst_id)s, %(resp)s, %(latency)s, %(tail_lat)s)")

        # encapsulate this
        try:
            self.curs.execute(add_cmd, entry)
       
        except connector.Error as err:
            if err.errno == (connector.errorcode. ER_NO_REFERENCED_ROW_2 or connector.errorcode. ER_ROW_IS_REFERENCED_2):
                print("Unknown instance identifier!")
            else:
                print("Something else went wrong whiel adding the entry!")
                return        
        self.dbx.commit()
    
    def add_instance_type(self, instance):
        
        #CONSIDER: having tables for each instance type
       
        add_inst_cmd = ("INSERT INTO " + INST_TABLE +
               "(provider, type, tier, cpu, gpu, memory) "
               "VALUES (    %(provider)s, %(type)s, %(tier)s, %(cpu)s, %(gpu)s, %(memory)s)")
        #autogenerate id, or have DB assign it and print

        # Insert new employee
        try:
            self.curs.execute(add_inst_cmd, instance)
       
        except connector.Error as err:
            if err.errno == (connector.errorcode.ER_DUP_ENTRY or connector.errorcode.ER_DUP_KEYNAME):
                print("Duplicate instance entry!")
            else:
                print("Something else went wrong!")
                return
        #probably keep a table of last entries?
        #... = cursor.lastrowid        
        self.dbx.commit()

    #select and return the last metric data (for each? for an instant if exist? discuss)
    def pull_last(self, identifier,n=1):
        #accept both id or str
        #OBSOLOTE
        # if isinstance(identifier, int): 
        #     id_cat='id'
        identifier=self.__identifier(identifier)
        sel_cmd = ("SELECT * FROM " + BENCH_TABLE + " WHERE t_entry=(SELECT MAX(t_entry) FROM "+ BENCH_TABLE + ") AND inst_id=%s;"  )
        price_cmd = ("SELECT `price` FROM " + INST_TABLE + "  WHERE id=%s;"  )

        #dict_curs
        self.dict_curs.execute(sel_cmd,(identifier,))
        res=self.dict_curs.fetchall()
        
        if not res:
            print("No entry for the requested instance")
            return

        #this is easier but we can also get prices once when we ask for candadtes
        #seperately get price

        self.dict_curs.execute(price_cmd,(identifier,))
        full_res=list(map(dict.update,zip(res,self.dict_curs.fetchall())))

        return full_res[:n] #n is a place holder for now and must be kept as 1. fetchall returns a list of dict entries, enabling us to collect data for running awg

    def get_alternatives(self,instance,stats=['cpu','ram']): #stats option provides the "get instances withx,y matching 'instance'" ability
        return self.get_candidates(self.get_inst_stats(self.__identifier(instance),stats))

    def get_candidates(self,stat_dict):
        
        #'WHERE a DIV 2 BETWEEN 10 AND 11' AND 'b DIV 4 BETWEEN 10 AND 11' ...]
        candidate_cmd=("SELECT `name` from " + INST_TABLE + 
        " WHERE " + " AND ".join([ k + " DIV " + str(stat_dict[k]) + " BETWEEN " + MIN + " AND " + MAX for k in stat_dict.keys()])+";")
        #unfortuntely python doesn't have list generation from ditc comprehension
        #print(candidate_cmd)
        self.curs.execute(candidate_cmd)
        res=self.curs.fetchall()
        return list(map(lambda x: x[0], res))

        #EXTRA:
        #if empty
        #    self.get_candidates({'ram':stat_dict['ram']})


    #### UTILITY

    def help(self):
        #execute
        self.curs.execute("describe " + INST_TABLE + ";")
        #fetch
        insts=self.curs.fetchall()
        #tabulate
        print(tabulate(insts, headers=DBClient.descriptors, tablefmt='psql'))


        self.curs.execute("describe " + BENCH_TABLE + ";")
        benchs=self.curs.fetchall()
        print(tabulate(benchs, headers=DBClient.descriptors, tablefmt='psql'))

    # Internally we always use the instance id in the database. This method will deal with name, tag or id
    def __identifier(self,idf):
        if isinstance(idf, str):
            return self.get_inst_id(idf)
        elif isinstance(idf, int):
            return idf
        else:
            print("Identifier not recognized")
            return
        
    # get the requested stats for a given instance id
    def get_inst_stats(self,id,stats=['cpu','ram','disk']):
        
        get_stats_cmd=("SELECT {} FROM ".format(",".join(stats)) + INST_TABLE +";")
        self.dict_curs.execute(get_stats_cmd)
        return self.dict_curs.fetchall()[0]
         

    def get_inst_id(self, lbl):# select the correct id for tag
        
        id_cmd=("SELECT `id` FROM `" + INST_TABLE  + "` WHERE (`tag` = %s OR `name` = %s)")
        self.dict_curs.execute(id_cmd, (lbl,lbl))
        res=self.dict_curs.fetchall()
        return (res[0]['id'] if res else "invalid instance" )


    def show_instances(self, full=False):
        #TODO: limit to last N entries if showing benchmarks

        #show all columns if only requested
        if full:
            hdr_list = DBClient.inst_headers
            hdr_str = "*"

        else:
            hdr_list = DBClient.inst_headers[:2] #tip: [:None] returns the full list
            hdr_str = ",".join(hdr_list)

        self.curs.execute("select %s from "%hdr_str + INST_TABLE  + ";")
        cols_info=self.curs.fetchall()
        print(tabulate(cols_info, headers=hdr_list, tablefmt='psql'))


    #manually execute a command. #DANGERZONE, well, user access in DB is limited. so, not really
    def man_exec(self, *args):
        if args == ( () or "" ): 
            print("Command can't be empty")
            return

        self.curs.execute(args)
        self.basic_print()


    def basic_print(self, dic=0):
        if dic:
            res=self.dict_curs.fetchall()
        else:
            res=self.curs.fetchall()

        print(res)

    # sample case for python garbage-collection practices
    def disconnect(self):
        print("Closing DB conection")
        self.curs.close()
        self.dict_curs.close()
        self.dbx.close()
        
        

def main():
    print("DBClient submodule")
  

if __name__ == "__main__":
    
    main() 