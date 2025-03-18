import os
import sys
import json 

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()

import pandas as pd
import pymongo  
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException    
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.T.to_json()).values()  # Use json.loads instead of json.load)
            return list(records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)   
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]            
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"  
    DATABASE = "network_security"
    Collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(f"Number of records inserted in MongoDB: {no_of_records}")

    # # Read train_data.csv
    # train_data_path = "Artifacts/06_29_2021_12_00_00/data_ingestion/train_data.csv"
    # try:
    #     train_data = pd.read_csv(train_data_path)
    #     print("Train Data:")
    #     print(train_data.head())
    # except FileNotFoundError as e:
    #     print(f"Error reading train_data.csv: {e}")
    #     # Provide the correct path if the file is located elsewhere
    #     correct_train_data_path = "correct/path/to/train_data.csv"
    #     try:
    #         train_data = pd.read_csv(correct_train_data_path)
    #         print("Train Data:")
    #         print(train_data.head())
    #     except Exception as e:
    #         print(f"Error reading train_data.csv from the correct path: {e}")
    # except Exception as e:
    #     print(f"Error reading train_data.csv: {e}")

