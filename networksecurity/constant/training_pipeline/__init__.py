import os
import sys
import numpy as np
import pandas as pd

"""
Training Pipeline related constant start with TRAINING_PIPELINE VAR NAME
"""
TARGET_COLUMN ="Result"
PIPELINE_NAME: str = "Network_Security"
ARTIFACTS_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train_data.csv"
TEST_FILE_NAME: str = "test_data.csv"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAMW
"""
    
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "network_security"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store" 
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2
    