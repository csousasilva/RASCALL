"""

This is the updated version of the "famous" db_management module

This new module include the following highlights
    OOP
    *args and *kwargs for data handeling
    logging



Logging levels

DEBUG
INFO
WARNING
ERROR
CRITICAL



create_db: what to do if REMOVE=False, chose "N"? Return?

The ideology behind modifing the table structure is that you should do one thing at a time. Avoid creating/modifying multiple table, column at once.
You should have free reign when modifying data. 

need SQL injection guard.

"""
VERSION = 0.2
RELEASE = False

import os,sys
import shutil
import numpy as np
import sqlite3
import logging
import datetime

logging.basicConfig(filename='db_interation.log',level=logging.INFO)

class database():
    
    def __init__(self, dir="./database", db_name="test_db_default_name.db", user="self",
                 DEBUG=False, REMOVE=False, BACKUP=False, OVERWRITE=True):
        
        self.db_name = db_name
        self.db_dir = dir
        self.user = user
        
        self.DEBUG = DEBUG
        self.REMOVE = REMOVE
        self.BACKUP = BACKUP
        self.OVERWRITE = OVERWRITE
        
        if RELEASE == True and OVERWRITE == True:
            if self.BACKUP == True:
                print """BACKUP is set to True and OVERWRITE is set to True. \n
                         Beware that BACKUP will overwrite previous BACKUPs. \n
                         Make sure to BACKUP your BACKUP if needed. \n
                         """        
                while True:     
                    next = str(raw_input("Acknowledged! (Y/N)?"))
                    if next.upper() == "Y":
                        break
                    elif next.upper() == "N":
                        return
                                   
            if self.REMOVE == True:
                print """REMOVE is set to True and OVERWRITE is set to True. \n 
                         Be aware as this will automatically overwrite existing database, table and data if they so exists! \n 
                         Please be sure what you are doing and proceed with caution. \n
                         """
                while True:     
                    next = str(raw_input("Are you sure about setting REMOVE to True (Y/N)?"))
                    if next.upper() == "Y":
                        break
                    elif next.upper() == "N":
                        self.REMOVE = False
                        break      
        
        # logging who is accessing the database, for debugging reasons.
        if self.user == "":
            try:
                self.user = os.environ["HOME"].split("/")[-1]
            except:
                self.user = os.getlogin()
            
        if self.db_dir != "":
            self.db_path = os.path.join(dir,db_name)
        else:
            self.db_path = self.db_name
    
    def __repr__(self):
        return self.db_path
    
    def __str__(self):
        return "This is a database named {} located at {}".format(self.db_name, self.db_dir)
    
    def __quit__(self):
        self.c.close()
        self.conn.close()
        
    def check_db_exists(self, path=""):

        if path == "":
            return os.path.exists(self.db_path)
        else: 
            return os.path.exists(path)
    
    def is_db(self):
#        print os.path.join(self.db_dir, self.db_name)
        return os.path.isfile(os.path.join(self.db_dir, self.db_name))
        
         
    def access_db(self):
        
        print self.db_path
    
        self.conn = sqlite3.connect(self.db_path)
        self.conn.text_factory = str  #retrieve DB strings in UTF-8 format? is this useful?
        self.c = self.conn.cursor()
   
        if self.DEBUG:
            if not RELEASE:
                self.c.execute("SELECT * FROM DEBUG where value=0")
                print self.c.fetchall()
            
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.c.execute("INSERT INTO DEBUG VALUES(?, ?, ?, ?)", 
                           (self.user,"DEBUG",date,1))
            self.conn.commit()
            
        logging.info("Accessing DB: {}".format(self.db_name))
    
    def create_db(self):
        """ the old database is not removed by default"""

        if self.check_db_exists():
            if self.OVERWRITE:
                if self.REMOVE:
                        self.delete_db() if os.path.exists(self.db_path) else None
                else:    
                    while True:
                        next = str(raw_input("Are you sure about removing database: {} (Y/N)?".format(self.db_path)))
                        if next.upper() == "Y":
                            self.delete_db() if os.path.exists(self.db_path) else None
                            break
                        elif next.upper() == "N":
                            logging.info("Old database not removed. No new database created, DB creation process terminated")
                            return #?
            else:
                logging.info("Old database not removed due to no overwrite permission.")
                raise Exception("Database with name {} already exist. No overwrite permission. New Database not created")
                return
        else:
            # if file dir already exist, don't need to recreate
            os.makedirs(self.db_dir) if not os.path.exists(self.db_dir) else None 
            
        self.conn = sqlite3.connect(self.db_path)
        self.conn.text_factory = str  #retrieve DB strings in UTF-8 format? is this useful?
        self.c = self.conn.cursor()
        
        #creating a dummy table for debugging purposes
        # 0 for create, 1 for access, 2 for insert, 3 for select, 4 for alter, 5 for delete?
        # 
        if self.DEBUG:
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.c.execute("CREATE TABLE IF NOT EXISTS DEBUG(user TEXT, table_name TEXT, date TEXT, value REAL)")
            self.c.execute("INSERT INTO DEBUG VALUES(?, ?, ?, ?)", 
                           (self.user,"DEBUG",date,0))
        
        self.conn.commit()        
        logging.info("DB: {} created".format(self.db_name))       
        
        
    def delete_db(self):
        
        # to delete an sqlite database, simply remove the file.
        
        if self.BACKUP:
            
            backup_dir = "".join([self.db_dir,"/backup/"])
            backup_path = "".join([self.db_dir,"/backup/",self.db_name])
            os.makedirs(backup_dir) if not os.path.exists(backup_dir) else None # make dir if dir not exist
            
            try:
                if self.OVERWRITE:
                    shutil.copyfile(self.db_path, backup_path)
                    os.remove(self.db_path)
                else:
                    logging.info("Backup database not removed due to no overwrite permission.")
                    raise Exception("Backup Database with name {} already exist. No overwrite permission. New Database not created")
                    return      
                              
            except IOError as e:
                print e
            
            logging.info("DB: {} backed up".format(self.db_name))
            
        else:
            os.remove(self.db_path)
            logging.info("DB: {} deleted".format(self.db_name))
    
    def update_db_name(self,new_db_name):
        
        os.chdir(self.db_dir)
        temp = self.db_name
        
        self.db_name = new_db_name
        os.rename(temp,new_db_name)
        
        logging.info("DB name updated from {} to {}".format(temp, new_db_name))
        return new_db_name
    
    def check_table_exist(self, table_name):
        
        self.c.execute("SELECT name FROM sqlite_master WHERE name='{}'".format(table_name))
        result = self.c.fetchone()
        if result == None or result[0] != table_name:
            return False
        return True
        
    def access_table(self, table_name):
        """ the use of this is kinda questionable, sort of a pseudo __init__? maybe for debugging reasons?"""
        self.table_name = table_name
        
    def create_table(self, table_name, *columns, **primary):
        """
        example usage:
            column = [("column A","text"),("column B","text"),("column C","text"),("column D","text"),("column E","text")]
            primary= {"primary":"column A"}
            create_table(table_name, *columns, **primary)
        """
        # check if table exist

        if self.check_table_exist(table_name):
            if self.OVERWRITE:
                if self.REMOVE:
                    self.delete_table(table_name)
                else:    
                    while True:
                        next = str(raw_input("Are you sure about removing table: {} (Y/N)?".format(table_name)))
                        if next.upper() == "Y":
                            self.delete_table(table_name) if os.path.exists(self.db_path) else None
                            break
                        elif next.upper() == "N":
                            logging.info("Old table not removed. No new table created, table creation process terminated")
                            return #?        
            else:
                logging.info("Old table not removed due to no overwrite permission.")
                raise Exception("Table with name {} already exist. No overwrite permission. New table not created")
                return
                    
        # check if column number is correct
        if len(columns) == 0:
            raise Exception("Your table column is empty, no table is created")
            return
        
        # generating table creation query
        for i, [column, type] in enumerate(columns):
            _ = "{} {}".format(column, type) if i==0 else "{}, {} {}".format(_, column, type)
            if primary != {} and column == primary.items()[0][1]:
                _ = "{} PRIMARY KEY".format(_)   
        command = "CREATE TABLE {} ({})".format(table_name, _)  
        
        if primary != {} and "PRIMARY" not in command:
            raise Exception("No matching primary key, table not created")
            return
        
        self.c.execute(command)
        self.conn.commit()    
        
        logging.info("Table: {} created for DB: {}".format(table_name, self.db_name))
    
    def update_table_name(self, table_name, new_table_name):
        
        if not self.check_table_exist(table_name):
            raise Exception("Can't alter a Ghost table. Please Check if your table exists")
            return   
                    
        command = "ALTER TABLE {} RENAME TO {}".format(table_name,new_table_name)
        
        try:
            self.c.execute(command)
        except sqlite3.OperationalError:
            if self.OVERWRITE:
                self.BACKUP = False
                self.delete_table(new_table_name)
                self.c.execute(command)
                logging.info("Old backup table removed and new table backed up.")
            else:
                logging.info("No overwrite permission, new table not backed up.")
  
        self.conn.commit()
        
        logging.info("Table: {} from DB: {} renamed to {} ".format(table_name, self.db_name, new_table_name))

    def delete_table(self,table_name):
        """
        Delete the table by default. If BACKUP is True, update the table_name to table_name_backup
        """
        
        if not self.check_table_exist(table_name):
            raise Exception("Can't remove a Ghost table. Please Check if your table exists")
            return           
        
        if self.BACKUP:
            self.update_table_name(table_name, table_name+"_backup")
            return
        else:                   
            command = "DROP TABLE {}".format(table_name)
        
        self.c.execute(command)
        self.conn.commit()
        
        logging.info("Table: {} from DB: {} Deleted".format(table_name, self.db_name))


    def join_table(self, *table, **parameters):
        pass

    def describe_table(self,table_name):
        
        self.c.execute("PRAGMA table_info({})".format(table_name))
        col_num = len(self.c.fetchall())
        
        self.c.execute("SELECT Count() FROM {}".format(table_name))
        row_num = self.c.fetchone()[0]
        
        cel_num = col_num*row_num
        
        print " Table: {} \n Column: {} \n Row: {} \n Cell: {} \n".format(table_name, col_num, row_num, cel_num)

    def get_table_row_count(self, table_name):
        
        self.c.execute("SELECT Count() FROM {}".format(table_name))
        return self.c.fetchone()[0]
    
    def get_table_column_count(self, table_name):
        
        self.c.execute("PRAGMA table_info({})".format(table_name))
        return len(self.c.fetchall())  

    def get_table_primary_column(self, table_name):
        
        self.c.execute("PRAGMA table_info({})".format(table_name))
        result = self.c.fetchall()
        for i,key in enumerate([x[5] for x in result]):
            if key == 1:
                return result[i][1],i
            else:
                print "Table does not have a primary key"
                return "",-1
            
        #return len(self.c.fetchall())  


    def get_column_name(self,table_name, conn, c):
        self.c.execute("PRAGMA table_info({})".format(table_name))
        return [x[1] for x in self.c.fetchall()]
    
    def check_column_exist(self, table_name, column_name):
        """
        need to test if fetchall can be compared using "in"
        fetchall for pragma gives something like [(0, 'user', 'TEXT', 0, None, 0), etc]
        need to grab the second element from each tuple and form another list.
        """
        self.c.execute("PRAGMA table_info({})".format(table_name))
        if column_name in [x[1] for x in self.c.fetchall()]:
            return True
        else:
            return False
    
    def add_column(self):
        pass
    
    def update_column_name(self):
        pass

    def delete_column(self):
        pass



    def insert_data_single(self, table_name, data, commit=True, guard=True):
        """
        Insert a single line of data into the table
        If ignore is True, will pass if data sequence already exist in primed table
        """
        
        if guard:
            if len(data) != self.get_table_column_count(table_name):
                logging.debug("Data length does not match table column count, process terminated")
                raise Exception("Data length does not match table column count, please check input data")
                return
        
        for i in range(len(data)):
            _ = "{}".format("?") if i==0 else "{},{}".format(_,"?")
        command = "INSERT INTO {} VALUES ({})".format(table_name, _)
        
        try:
            self.c.execute(command, data)
            if commit:
                self.conn.commit()
                logging.debug("Data injected into database")
            else:
                logging.debug("Data not injected into database")            
            
        except sqlite3.IntegrityError as s:
            # insert failed here because the table has primary key and you're inserting duplicates
            
            
            if self.OVERWRITE:
                self.update_data(data)
                logging.debug("Existing Data replaced with new injection")
            else:
                logging.debug("Data injection error: {}".format(s))
                raise Exception("Duplicate Data")
            return

    def _insert_data_single_dev(self, table_name, data):
        """
        This version of the insert is for bulk insertion without all the safety measures
        Not commited or logged by default to save time.
        Only use this if you're sure what you're doing and the code tested
        """
        for i in range(len(data)):
            _ = "{}".format("?") if i==0 else "{},{}".format(_,"?")
        command = "INSERT INTO {} VALUES ({})".format(table_name, _)  
        self.c.execute(command, data)
        
        
        

    def update_data(self,data):
        """
        update the data in an element
        """
        column,pos = test_db.get_table_primary_column(table_name)
        
        
        for i in range(len(data)):
            _ = "{}".format("?") if i==0 else "{},{}".format(_,"?")
        command = "UPDATE {} VALUES ({})".format(table_name, _)
        
        print command        
        
        
        #c.execute('UPDATE %s SET %s="%s" WHERE %s="%s"'%(table_name,data[0],data[1],conditions[0],conditions[1]))
        
        
    
    def delete_data(self):
        pass
    
    
    
    
    def select(self, table_name, columns="*", limit=-1, order="", asc=True,**kwargs):
        """
        The robust select query constructor
        
        The only required parameter is table_name
        By default if no additional parameters are provided, will execute the following query:
            SELECT * FROM table_name LIMIT 50
        
        If RELEASE is set to False (i.e, in dev mode), then will execute
            SELECT * FROM table_name
            
        This is the simplest select query, which can be dangerous when your table is very large. 
        table_name can be either a string or a list if you want to select data from multiple tables.
        When comparing between columns in table, always use "table_x.column_a=":"table_y.column_b"
        
        Optional parameters include:
            columns: which column in the table you're interested in to return
            limit: how many rows you want to return
            order: order by 
            asc: ascending is true. if false then descending
            remaining **kwargs will yield all the conditons for the WHERE clause.    
            
        """
        
        table_name = ",".join(table_name) if type(table_name) == list else table_name
        
        
        # This is so complex yet... somehow pythonic. It's basically a bunch of if else statements and for loops joined into 1 liners
        target = ", ".join(i for i in columns) if columns != "*" else "*"
        condition = "".join(["WHERE ", (" AND ".join( "".join([item,'"',key,'"']) if (type(key) == str and "." not in key) else "".join([item,str(key)]) for item, key in kwargs.items()))]) if kwargs!={} else ""
        orderby = ("ORDER BY {}".format(order) if asc else "ORDER BY {} DESC".format(order)) if order != "" else ""
        limitation = "LIMIT {}".format(limit) if limit != -1 else ("LIMIT 50" if RELEASE else "")

        cmd = "SELECT %s FROM %s %s %s %s"%(target, table_name, condition, orderby, limitation)
        
        if self.DEBUG:
            print "Executing Query... \n{}".format(cmd)
        try:
            self.c.execute(cmd)  
            logging.debug("Selecting from database with {}".format(cmd))
            return self.c.fetchall()
        except Exception as e:
            print e
            raise Exception("""Select Failed, maybe something is wrong with the query? \n
                            Try describe_table(table_name) to see if column names are correct""")
            return []
    


if __name__ == "__main__":
    
    kwargs = {"db_name":"testdb.db",
              "user":"",
              "DEBUG":True,
              "REMOVE":True,
              "BACKUP":True,
              "OVERWRITE":True}
    
    
    test_db = database(**kwargs)
    
    #test_db.create_db()
    test_db.access_db()
    #test_db.check_table_exist("DEBUG")
    #test_db.update_db_name("noob.db")
    """

    table_name = "TESTING"
    columns = [("column_A","text"),("column_B","text"),("column_C","text"),("column_D","text"),("column_E","text")]
    primary= {"primary":"column_A"}
    
    test_db.create_table(table_name, *columns, **primary)

    test_db.describe_table(table_name)
    
    
    data = ["a","b","c","d","e"]
    
    test_db._insert_data_single_dev(table_name, data)
    test_db.insert_data_single(table_name, data)
    
    
    
    test_db.select(table_name)
    
    column,pos = test_db.get_table_primary_column(table_name)
    print column, pos
    
    #test_db.check_column_exist(table_name, "user")
    
    logging.info("Code Executed \n\n")

    """
    table_name = ["TESTING"]
    
    
    columns = ["column_D",
               "column_E"
               ]
    
    kwargs = {
              "limit": 50,
              "order":"column_A",
              "columns":columns,
              "asc":False
              }
            
    
    result = test_db.select(table_name, **kwargs)
    result = test_db.select(table_name)    
    print result
    
    
    
    
    
    
    