from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging  # Output: Logger object


## Configuration of the Ingestion Config
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig  # Output: DataIngestionConfig, TrainingPipelineConfig   
from networksecurity.entity.artifact_entity import DataIngestionArtifact  # Output: DataIngestionArtifact   
import os   # Output: OS module
import sys  # Output: SYS module
import pymongo  # Output: pymongo 
from typing import List, Dict  # Output: List, Dict
from sklearn.model_selection import train_test_split  # Output: train_test_split
import pandas as pd  # Output: pandas as pd
import numpy as np  # Output: numpy as np
from dotenv import load_dotenv  # Output: load_dotenv

load_dotenv()  # Output: Load the environment variables 

MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # Output: Get the MongoDB URL from the environment variables

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config  # Output: DataIngestionConfig object 
        except Exception as e:
            raise NetworkSecurityException(e, sys)  # Output: Raise an exception

    def export_collection_as_dataframe(self):
        """
        Read the data from the MongoDB collection and export it as a DataFrame

        Raises:
            NetworkSecurityException: An error occurred while exporting the collection as a DataFrame
        """

        try:
            database_name = self.data_ingestion_config.database_name  # Output: network_security
            collection_name = self.data_ingestion_config.collection_name  # Output: NetworkData
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)  # Output: MongoDB client
            collection = self.mongo_client[database_name][collection_name] # Output: MongoDB database
        
            df = pd.DataFrame(list(collection.find()))  # Output: Get the data from the MongoDB collection
            if "_id" in df.columns:
                df.drop(columns=["_id"], axis=1)  # Output: Drop the '_id' column)
            
            df.replace({"na":np.nan}, inplace=True)  # Output: Replace 'na' with NaN
            return df  # Output: Return the DataFrame
                
        except Exception as e:
            raise NetworkSecurityException(e, sys)  # Output: Raise an exception

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feauture_store_path = self.data_ingestion_config.feature_store_file_path  # Output: Artifacts/06_29_2021_12_00_00/feature_store  
            # Creating folder for feature store
            dir_path = os.path.dirname(feauture_store_path)  # Output: Get the directory path   
            os.makedirs(dir_path, exist_ok=True)  # Output: Create the directory path
            dataframe.to_csv(feauture_store_path, index=False)  # Output: Save the data to the feature store path
            logging.info(f"Data saved to feature store at {feauture_store_path}")  # Output: Log the message
            return dataframe  # Output: Return the DataFrame
        except Exception as e:
            raise NetworkSecurityException(e, sys)  # Output: Raise an exception

    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
                )  # Output: Split the data into train and test sets
                
            logging.info(
                "Performed train test split on the dataframe"
                )  # Output: Log the message

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
                )  # Output: Log the message
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)  # Output: Get the directory path
            os.makedirs(dir_path, exist_ok=True)  # Output: Create the directory path
            logging.info(f"Exporting train and test file path.")  # Output: Log the message
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
                )  # Output: Save the training data to the training file path
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
                )  # Output: Save the testing data to the testing file path
            logging.info("Data split into train and test sets. Export train and test file path")  # Output: Log the message
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)  # Output: Raise an exception


    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()  # Output: Get the data from the MongoDB collection
            dataframe = self.export_data_into_feature_store(dataframe)  # Output: Save the data to the feature store
            self.split_data_as_train_test(dataframe)  # Output: Split the data into train and test sets
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)  # Output: Raise an exception
    
    

    

    # def save_data(self, data: pd.DataFrame, file_path: str) -> None:
    #     try:
    #         data.to_csv(file_path, index=False)  # Output: Save the data to the file path
    #     except Exception as e:
    #         raise NetworkSecurityException(e, sys)  # Output: Raise an exception

    # def ingest_data(self)
    