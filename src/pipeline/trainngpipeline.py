from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.components.data_ingestion import DataIngestion
from src.exception import CustomException
import os,sys 
from src.logger import logging

class Trainpipeline:
    def __init__(self) :
        self.data_ingestion_config = DataIngestionConfig()
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f"{'<<'*30} Data Ingestion component started {'>>'*30}")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion artifacts \n {data_ingestion_artifacts}")
            logging.info(f"{'<<'*30} Data Ingestion component completed {'>>'*30}")
            return data_ingestion_artifacts
        except Exception as e:
            logging.info(f"Training pipeline start data ingestion method interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            logging.info(f"{'=='*30} Training pipeline started {'=='*30}")
            self.start_data_ingestion()
            logging.info(f"{'=='*30} Training pipeline completed {'=='*30}")
        except Exception as e:
            logging.info(f"Training pipeline interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    
    