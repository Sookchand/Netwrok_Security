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


class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
            ) # Output: Artifacts/06_29_2021_12_00_00/data_validation
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir, 
            training_pipeline.DATA_VALIDATION_VALID_DIR 
            ) # Output: Artifacts/06_29_2021_12_00_00/data_validation/validated
        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir, 
            training_pipeline.DATA_VALIDATION_INVALID_DIR
            ) # Output: Artifacts/06_29_2021_12_00_00/data_validation/invalid  
        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir, 
            training_pipeline.TRAIN_FILE_NAME
            ) # Output: Artifacts/06_29_2021_12_00_00/data_validation/validated/train_data.csv
        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir, 
            training_pipeline.TEST_FILE_NAME
            ) # Output: Artifacts/06_29_2021_12_00_00/data_validation/validated/test_data.csv 
        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir, 
            training_pipeline.TRAIN_FILE_NAME
            ) # Output: Artifacts/06_29_2021_12_00_00/data_validation/invalid/train_data.csv
        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir, 
            training_pipeline.TEST_FILE_NAME
            ) # Output: Artifacts/06_29_2021_12_00_00/data_validation/invalid/test_data.csv    
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        ) # Output: Artifacts/06_29_2021_12_00_00/data_validation/drift_report/report.yml   
        
class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMTION_DIR_NAME
            ) # Output: Artifacts/06_29_202
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy")
            ) # Output: Artifacts/06_29_2021_12_00_00/data_transformation/transformed_data/train_data.npy
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy")
            ) # Output: Artifacts/06_29_2021_12_00_00/data_transformation/transformed_data/test_data.npy    
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,
            ) # Output: Artifacts/06_29_2021_12_00_00/data_transformation/transformed_object/preprocessing_object.pkl