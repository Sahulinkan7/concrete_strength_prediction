from src.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
import os,sys 
from src.logger import logging

class Trainpipeline:
    is_running_pipeline = False
    def __init__(self) :
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        
    def start_data_ingestion(self,data_ingestion_config : DataIngestionConfig) -> DataIngestionArtifact:
        try:
            logging.info(f"{'<<'*30} Data Ingestion component started {'>>'*30}")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion artifacts \n {data_ingestion_artifacts}")
            logging.info(f"{'<<'*30} Data Ingestion component completed {'>>'*30}")
            return data_ingestion_artifacts
        except Exception as e:
            logging.info(f"Training pipeline start data ingestion method interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    def start_data_validation(self,data_validation_config : DataValidationConfig,
                              data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info(f"{'<<'*30} Data validation component started {'>>'*30}")
            data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info(f"data validation artifacts \n {data_validation_artifact}")
            logging.info(f"{'<<'*30} Data validation component completed {'>>'*30}")
            return data_validation_artifact
        except Exception as e:
            logging.info(f"Training pipeline start data validation interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
        
    def start_data_transformation(self,data_transformation_config : DataTransformationConfig,
                                  data_validation_artifact : DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info(f"{'<<'*30} Data Transformation component started {'>>'*30}")
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifacts=data_transformation.initiate_data_transformation()
            
            logging.info(f"data transformation artifacts : {data_transformation_artifacts}")
            logging.info(f"{'<<'*30} Data Transformation component completed {'>>'*30}")
            return data_transformation_artifacts
        except Exception as e:
            logging.info(f"Training pipeline start data transformation interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    def start_model_training(self,model_trainer_config : ModelTrainerConfig,
                             data_transformation_artifact : DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logging.info(f"{'<<'*30} Model Training component started {'>>'*30}")
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info(f"{'<<'*30} Model Training component completed {'>>'*30}")
            return model_trainer_artifacts
        except Exception as e:
            logging.info(f"Training pipeline start model training interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            Trainpipeline.is_running_pipeline = True
            logging.info(f"{'=='*30} Training pipeline started {'=='*30}")
            data_ingestion_artifacts=self.start_data_ingestion(data_ingestion_config=self.data_ingestion_config)
            data_validation_artifact=self.start_data_validation(data_validation_config=self.data_validation_config,data_ingestion_artifact=data_ingestion_artifacts)
            data_transformation_artifact = self.start_data_transformation(data_transformation_config=self.data_transformation_config,data_validation_artifact=data_validation_artifact)
            best_model_score=self.start_model_training(model_trainer_config=self.model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            print(best_model_score)
            Trainpipeline.is_running_pipeline = False
            logging.info(f"{'=='*30} Training pipeline completed {'=='*30}")
        except Exception as e:
            logging.info(f"Training pipeline interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    
    