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
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

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

    # Configuration for Data Ingestion
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config)
    data_ingestion_artifact = DataIngestionArtifact(
        trained_file_path=data_ingestion_config.training_file_path,
        test_file_path=data_ingestion_config.testing_file_path
    )

    # Data Transformation
    data_transformation_config = DataTransformationConfig(training_pipeline_config)
    data_transformation = DataTransformation(data_ingestion_artifact, data_transformation_config)
    data_transformation_artifact = data_transformation.initiate_data_transformation()

    # Model Training
    model_trainer_config = ModelTrainerConfig(training_pipeline_config)
    model_trainer = ModelTrainer(model_trainer_config)
    model_trainer_artifact = model_trainer.train_model(
        train_arr=np.load(data_transformation_config.transformed_train_file_path),
        test_arr=np.load(data_transformation_config.transformed_test_file_path)
    )
    print(f"Model Trainer Artifact: {model_trainer_artifact}")

