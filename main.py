from networksecurity.components.data_ingestion import DataIngestion  # Output: DataIngestion
from networksecurity.exception.exception import NetworkSecurityException  # Output: NetworkSecurityException
from networksecurity.logging.logger import logging  # Output: logging   
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig  # Output: DataIngestionConfig, TrainingPipelineConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig


if __name__=="__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()  # Output: TrainingPipelineConfig object
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)  # Output: DataIngestionConfig object
        data_ingestion = DataIngestion(dataingestionconfig)  # Output: DataIngestion object
        logging.info("Initiate the data ingestion")  # Output: Log the message
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
    except NetworkSecurityException as e:
        logging.error(e)  # Output: Log the error message
   