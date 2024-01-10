from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from src.constants import SCHEMA_FILE_PATH
from src.utils.commonutils import read_yaml_file
import os,sys 
import pandas as pd
import yaml

class DataValidation:
    def __init__(self,data_validation_config : DataValidationConfig,
                 data_ingestion_artifact : DataIngestionArtifact):
        
        logging.info(f"Data Validation object created")
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        
        os.makedirs(data_validation_config.root_dir,exist_ok=True)
        logging.info(f"Data validation artifact directory created ")
    
    def validate_columns(self,data_filepath) -> bool:
        try:
            logging.info(f"validating all columns inside dataframe")
            validation_status = None
            dataframe = pd.read_csv(data_filepath)
            
            all_columns = list(dataframe.columns)
            schema_columns = read_yaml_file(SCHEMA_FILE_PATH)['COLUMNS'].keys()
            logging.info(f"columns from schema file : {schema_columns}")
            logging.info(f"columns from dataframe : {all_columns}")
            
            for col in all_columns:
                if col not in schema_columns:
                    validation_status = False
                    with open(self.data_validation_config.data_validation_status_filepath,'w') as file:
                        yaml.dump({'validation_status':validation_status},file)
                else:
                    validation_status = True
                    with open(self.data_validation_config.data_validation_status_filepath,'w') as file:
                        yaml.dump({'validation_status':validation_status},file)
                        
            logging.info(f"validation status is {validation_status}")
            
            return validation_status                    
                
        except Exception as e:
            logging.info(f"validate columns method interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            validation_status = self.validate_columns(data_filepath=self.data_ingestion_artifact.raw_data_path)
            
            validation_artifact = DataValidationArtifact(
                data_validation_status=validation_status,
                data_validation_report_filepath=self.data_validation_config.data_validation_status_filepath,
                validated_dataset_filepath= self.data_ingestion_artifact.raw_data_path,
                validated_train_filepath= self.data_ingestion_artifact.train_data_path,
                validated_test_filepath=self.data_ingestion_artifact.test_data_path
            )
            
            return validation_artifact
        except Exception as e:
            logging.info(f"Data validation inititation interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)