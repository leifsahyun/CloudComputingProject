#! /usr/bin/env python
#TODO: later, narrow down 
from mysql import connector

#move this, MEH
dbx = None
curs = None 
#TODO:  list of default adresses to fall back to


#Coudln't refrain from wrapping it in a class

class DBClient(object):
    DEF_USR = 'perfkit'
    DEF_HOST = '127.0.0.1'
    DEF_DB = 'metricsDB'


    def __init__(self, *args):
        self.dbx=connect_db(args)
        self.curs=self.dbx.cursor


    def connect_db(self, usr=DEF_USR, h=DEF_HOST, db=DEF_DB ):
        
        #passport prompt could be tied to an arg, and fired if only one isn't passed
        p = getpass.getpass() #backwards pass thru 
        # 0202doulc

        '''
        # ALTERNATIVE #
        config = {
            'user': 'scott',
            'password': 'password',
            'host': '127.0.0.1',
            'database': 'employees',
            'raise_on_warnings': True
        }

        dbx = connector.connect(**config)
        ''' 
        
        #Try connection with the provided values
        try:
            dbx = connector.MySQLConnection(user=usr, password=p,
                            host=h,database=db,
                            auth_plugin='mysql_native_password')
            #self.cursor = self.dbx.cursor()
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
                exit()
        else:
            
            return dbx
    # expect mysql.connector.errors.InterfaceError
    # mysql.connector.errors.DatabaseError: 2003 (HY000): Can't connect to MySQL server on '127.0.0.2' (111)

    # receive an entry, validate and insert
    # entry should have 

    # example: aDBCleint.add_entry(Perfkit.do_bench_stuff())
    def add_entry(self, entry):
        
        #CONSIDER: having tables for each instance type
        entry_data = {}
        
        add_employee = ("INSERT INTO benchmark "
               "(first_name, last_name, cpu, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")


        # Insert new employee
        self.curs.execute(add_employee, entry)
       
        #probably keep a table of last entries?
        #... = cursor.lastrowid        
        self.dbx.commit()
    
    def add_instance_type(self, instance):
        
        #CONSIDER: having tables for each instance type
       
        add_cmd = ("INSERT INTO instances"
               "(first_name, last_name, cpu, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")


        # Insert new employee
        self.curs.execute(add_cmd, instance)
       
        #probably keep a table of last entries?
        #... = cursor.lastrowid        
        self.dbx.commit()


    #select and return the last metric data (for each? for an instant if exist? discuss)
    def pull_last(self):
        pass

    # sample case for python garbage-collection practices
    def disconnect(self):
        self.curs.close()
        self.dbx.close()
        
    def __del__(self):
        print("Closing DB conection")
        self.disconnect()



if __name__ == "__main__":
    #main()
    pass