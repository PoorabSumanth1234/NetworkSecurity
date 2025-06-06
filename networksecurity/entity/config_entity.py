from datetime import datetime 
import os 
from networksecurity.constant import Training_Pipeline 
print(Training_Pipeline.ARTIFACT_DIR)
print(Training_Pipeline.PIPEINE_NAME)


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_name=Training_Pipeline.PIPEINE_NAME
        self.artifact_name=Training_Pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.timestamp: str=timestamp
    
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir: str=os.path.join(
            training_pipeline_config.artifact_dir,Training_Pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str= os.path.join(
            self.data_ingestion_dir,Training_Pipeline.DATA_INGESTION_FEATURE_STORE_DIR,Training_Pipeline.FILE_NAME
        )
        self.training_file_path: str=os.path.join(
            self.data_ingestion_dir, Training_Pipeline.DATA_INGESTION_INGESTED_DIR,Training_Pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path: str= os.path.join(
            self.data_ingestion_dir, Training_Pipeline.DATA_INGESTION_INGESTED_DIR,Training_Pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio=Training_Pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name=Training_Pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name=Training_Pipeline.DATA_INGESTION_DATABASE_NAME
# We are initialising this data_ingestion directory the data_ingestion_dir_name value and the values are cominng from the training pipeline config 
        