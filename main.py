from networksecurity.components.data_ingestion import DataIngestion  # Output: DataIngestion
from networksecurity.components.data_validation import DataValidation  # Output: DataValidation
from networksecurity.components.data_transformation import DataTransformation    
from networksecurity.exception.exception import NetworkSecurityException  # Output: NetworkSecurityException
from networksecurity.logging.logger import logging  # Output: logging 
from networksecurity.entity.config_entity import DataIngestionConfig  # Output: DataIngestionConfig
from networksecurity.entity.config_entity import DataValidationConfig  # Output: DataValidationConfig  
from networksecurity.entity.config_entity import DataTransformationConfig   
from networksecurity.entity.config_entity import TrainingPipelineConfig # Output: TrainingPipelineConfig




if __name__=="__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()  # Output: TrainingPipelineConfig object
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)  # Output: DataIngestionConfig object
        data_ingestion = DataIngestion(dataingestionconfig)  # Output: DataIngestion object
        logging.info("Initiate the data ingestion")  # Output: Log the message
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data initiation completed")  # Output: Log the message
        print(dataingestionartifact)
        data_validation_config = DataValidationConfig(trainingpipelineconfig)  # Output: DataValidationConfig object
        data_validation=DataValidation(dataingestionartifact, data_validation_config)  # Output: DataValidation object
        logging.info("Initiate the data validation")  # Output: Log the message
        data_validation_artifact=data_validation.initiate_data_validation()  # Output: Data validation initiated
        logging.info("Data validation completed")  # Output: Log the message
        print(data_validation_artifact)
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info("Data transformation started")
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data transformation completed")
    except NetworkSecurityException as e:
        logging.error(e)  # Output: Log the error message
   