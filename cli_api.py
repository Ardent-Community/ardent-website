import sqlite3
from encrypt import Encrypt

 
 
 
class Apikey():
    
    def __init__(self, db):
        self.db = db
        self.schema="""CREATE TABLE apikey (id TEXT PRIMARY KEY,key TEXT UNIQUE NOT NULL);"""
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
    
    def generateAndAdd_api_key(self, seed, uid):
        key = Encrypt(uid, seed)
        #add the api key to the database
        
        with self.api_db_connect as db:
            c= db.cursor()
            c.execute("INSERT INTO apikey (id, key) "
            "VALUES (?, ?)",
            (uid, key),)
            db.commit()
        
        return key
    
    #write a funtion to retrive the uid using the key from the database
    
    def get_(self, key):
        with self.api_db_connect() as db:
            c=db.cursor()
            userkey = c.execute(f"SELECT * FROM apikey WHERE  key = {key}").fetchnone()
            if not userkey:
                return None
            
            uid_ = userkey[0]
            return uid_
            
            
    
    #write a funtion to verify if a key already exists in the database
    def exists_(self, uid):
        with self.api_db_connect() as db:
            c=db.cursor()
            userid = c.execute(f"SELECT * FROM apikey WHERE  id = {uid}").fetchnone()
            if not userid: return False
            else: return True
            
       