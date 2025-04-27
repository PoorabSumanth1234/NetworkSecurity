import os 
import sys 
import json
import certifi

from dotenv import load_dotenv
load_dotenv()

mongo_db_url=os.getenv('MONGO_DB_URL')
print(mongo_db_url)
ca=certifi.where()   #this line retrieves the part to the bundle of CA certificates provided by certify and store it in th variable ca 
#ca is cerficate autorities (i.e the trusted certificate authorities) , this is done to ensure that the server we are connecting has a trusted certificate ensured. 
# certifi provides a set of root certificates 
# It is commonly used by python libraries that needs to make a secure http connection 

import pandas as pd 
import numpy as np 
import pymongo 
from networksecurity.logging.logger import logging
from networksecurity.Exception.exception import NetworkSecurityException

class NetworkDataExtract():  #this is my etl pipeline 
    def __init__(self):
        try:
            pass 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converted(self,file_path):
        try:
            data=pd.read_csv(file_path) 
            data.reset_index(drop=True,inplace=True) #this is used for removing or dropping the index numbers from the dataset 
            # How to insert our data in form of json in mongodb ---> we convert every record in the form of list of json [{A:1,B:2}] like in the form of key value pairs i.e list of dicionaries
            records=list(json.loads(data.T.to_json()).values())   #csv to json conversion
            return records 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def insert_data_to_mongo_db(self,records,database,collection): #collection is like a table just like that in sql 
        try:
            self.database=database
            self.collection=collection
            self.records=records 
            self.mongo_client=pymongo.MongoClient(mongo_db_url)
            self.database=self.mongo_client[self.database]  #What database we are using will assigned in this mongo client 
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
            #we need to create a client so that we can connect to our mongodb 
            #pymongo is used to connect with mongodb 
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__=='__main__':
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="Poorab"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_converted(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_to_mongo_db(records,DATABASE,Collection)
    print(no_of_records)

 