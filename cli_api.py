import sqlite3
from encrypt import Encrypt

 
 
 
class Apikey():
    
    def __init__(self, db, uid):
        self.db = db
        self.uid = uid
        self.schema="""CREATE TABLE apikey (id TEXT PRIMARY KEY,apikey TEXT UNIQUE NOT NULL);"""
        self.make_table()
        
    def api_db_connect(self):
        return sqlite3.connect(self.db)
    
    #make a table to store the api keys
    def make_table(self):
        with self.api_db_connect as db:
            c = db.cursor()
            c.execute(f"CREATE TABLE IF NOT EXISTS apikey{self.schema}")
            db.commit()
            
    #use the uid to generate the new api key using a lot of maths
    
    def generateAndAdd_api_key(self, seed):
        key = Encrypt(self.uid, seed)
        self.key=key
        #add the api key to the database
        
        with self.connect() as db:
            db.execute("INSERT INTO user (id, apikey) "
            "VALUES (?, ?)",
            (self.uid, self.key),)
            db.commit()
        
        return self.key
    
    #write a funtion to retrive the uid using the key from the database
    
    def get_(self):
        pass
    
    #write a funtion to verify if a key already exists in the database
    def exists_(self):
        pass
       