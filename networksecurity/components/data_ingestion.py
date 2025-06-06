from networksecurity.Exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 

# Configuration of the data ingestion config 
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact # output of data ingestion
import os 
import sys 
import numpy as np 
import pandas as pd 
import  pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try: 
            self.data_ingestion_config=data_ingestion_config 
        except Exception as e : 
            raise NetworkSecurityException(e,sys)
    def export_collection_as_data_frame(self):
        """
        Reading data from mongo db 
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name] # reading the data from mongodb 
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            return df 
        except Exception as e: 
            raise NetworkSecurityException
    
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder 
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e : 
            raise NetworkSecurityException(e,sys)
    
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on dataframe")
            logging.info("Exited split_data_as_dataframe of Data_Ingestion class")
            
            dir_path= os.path.dirname(self.data_ingestion_config.training_file_path) #saving the files in the directory
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info("Exporting the train and test file path ")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,index=True, header=True
            )
            logging.info("Exported train and test file path ")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
    
    def initiate_data_ingestion(self):
        try: 
            dataframe=self.export_collection_as_data_frame()  #read from mongodb 
            dataframe=self.export_data_into_feature_store(dataframe) #save it 
            self.split_data_as_train_test(dataframe) # do the train test split and save it 
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact   # output of the data ingestion 
        except Exception as e : 
            raise NetworkSecurityException(e,sys)
        
# Here in data  ingestion the final goal is to take the final dataset and do the train test split of the dataset
# Now we'll towards the data ingestion artifacts 
# data ingestion artifact is the output of data ingestion 