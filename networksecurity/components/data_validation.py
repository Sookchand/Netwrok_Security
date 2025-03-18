from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging  
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
import pandas as pd 
import os,sys

import pandas as pd
import os
import sys
from scipy.stats import ks_2samp
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

def extract_schema_columns(schema):
    try:
        # Flatten the list of dictionaries into a single dictionary
        return {list(column.keys())[0]: list(column.values())[0] for column in schema["columns"]}
    except Exception as e:
        raise NetworkSecurityException(f"Invalid schema format: {e}", sys)


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self._schema_columns = extract_schema_columns(self._schema_config)  # Extract schema columns
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Validates if the DataFrame has the correct number of columns and logs any extra or missing columns.
        """
        try:
            required_columns = set(self._schema_columns.keys())
            actual_columns = set(dataframe.columns)

            logging.info(f"Required columns: {required_columns}")
            logging.info(f"Actual columns: {actual_columns}")

            # Identify extra columns
            extra_columns = actual_columns - required_columns
            if extra_columns:
                logging.warning(f"Extra columns found in the dataframe: {extra_columns}")
                dataframe.drop(columns=list(extra_columns), inplace=True)

            # Identify missing columns
            missing_columns = required_columns - actual_columns
            if missing_columns:
                logging.error(f"Missing columns in the dataframe: {missing_columns}")
                return False

            return len(dataframe.columns) == len(required_columns)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_column_data_types(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and correct column data types based on the extracted schema configuration.
        """
        try:
            for column, expected_dtype in self._schema_columns.items():
                if column in dataframe.columns:
                    try:
                        logging.info(f"Validating column: {column}")
                        dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce')  # Convert to numeric if needed
                        dataframe[column] = dataframe[column].astype(expected_dtype)  # Enforce data type
                        logging.info(f"Column {column} converted to {expected_dtype}")
                    except Exception as e:
                        raise NetworkSecurityException(
                            f"Failed to convert column {column} to {expected_dtype}. Error: {e}", sys
                        )
                else:
                    logging.error(f"Column {column} is missing in the DataFrame")
                    raise NetworkSecurityException(
                        f"Column {column} is not present in the DataFrame as expected by the schema.", sys
                    )
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        """
        Detects dataset drift by comparing the distributions of columns in base and current DataFrames.
        """
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                is_found = is_same_dist.pvalue < threshold
                if is_found:
                    status = False
                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            # Log drift detection status
            logging.info(f"Drift detection status: {status}")
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Initiates the data validation process, including column validation, data type validation, and drift detection.
        """
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # Read the data from train and test files
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            # Validate number of columns
            if not self.validate_number_of_columns(train_dataframe):
                raise NetworkSecurityException("Train data has incorrect number of columns.", sys)
            if not self.validate_number_of_columns(test_dataframe):
                raise NetworkSecurityException("Test data has incorrect number of columns.", sys)
            
            # Validate and correct data types
            train_dataframe = self.validate_column_data_types(train_dataframe)
            test_dataframe = self.validate_column_data_types(test_dataframe)
            
            # Check for data drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            
            # Save validated files
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            
            # Create and return DataValidationArtifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            logging.info("Data validation completed successfully.")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
