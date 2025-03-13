from datetime import datetime
import os
from networksecurity.constant import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACTS_DIR)
# Output: Network_Security
# Output: Artifacts     

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACTS_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.model_dir=os.path.join("final_model")
        self.timestamp: str=timestamp
        

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifact_dir, 
            training_pipeline.DATA_INGESTION_DIR_NAME
            ) # Output: Artifacts/06_29_2021_12_00_00/data_ingestion
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, 
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, 
            training_pipeline.FILE_NAME
            ) # Output: Artifacts/06_29_2021_12_00_00/data_ingestion/feature_store    
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, 
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
            ) # Output: Artifacts/06_29_2021_12_00_00/data_ingestion/train_data.csv
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, 
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
            ) # Output: Artifacts/06_29_2021_12_00_00/data_ingestion/test_data.csv
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION # Output: 0.2    
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME # Output: NetworkData  
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME # Output: network_security

