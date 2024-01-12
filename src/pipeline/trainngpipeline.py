from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from concrete_app.models import Modeltraining
from datetime import datetime
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
import os, sys
from src.logger import logging
from threading import Thread
from dataclasses import dataclass,asdict
from uuid import uuid4
import pandas as pd

@dataclass
class Experiments:
    experiment_id : int
    running_status : str
    start_time : str
    stop_time : str 
    execution_time : str
    message : str
    accuracy : str
    is_model_accepted: bool 
    
class Trainpipeline(Thread):
    experiment : Experiments = Experiments(*([None]*8))
    is_running_pipeline = False
    experiment_file_path = None
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        Trainpipeline.experiment_file_path = os.path.join("artifacts","experiments","experiments.csv")
        super().__init__(daemon=False,name="TrainingPipeline")

    def start_data_ingestion(self, data_ingestion_config: DataIngestionConfig) -> DataIngestionArtifact:
        try:
            logging.info(f"{'<<'*30} Data Ingestion component started {'>>'*30}")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion artifacts \n {data_ingestion_artifacts}")
            logging.info(f"{'<<'*30} Data Ingestion component completed {'>>'*30}")
            return data_ingestion_artifacts
        except Exception as e:
            logging.info(
                f"Training pipeline start data ingestion method interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def start_data_validation(
        self,
        data_validation_config: DataValidationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
    ) -> DataValidationArtifact:
        try:
            logging.info(f"{'<<'*30} Data validation component started {'>>'*30}")
            data_validation = DataValidation(
                data_validation_config=data_validation_config,
                data_ingestion_artifact=data_ingestion_artifact,
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"data validation artifacts \n {data_validation_artifact}")
            logging.info(f"{'<<'*30} Data validation component completed {'>>'*30}")
            return data_validation_artifact
        except Exception as e:
            logging.info(
                f"Training pipeline start data validation interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def start_data_transformation(
        self,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact,
    ) -> DataTransformationArtifact:
        try:
            logging.info(f"{'<<'*30} Data Transformation component started {'>>'*30}")
            data_transformation = DataTransformation(
                data_transformation_config=data_transformation_config,
                data_validation_artifact=data_validation_artifact,
            )
            data_transformation_artifacts = (
                data_transformation.initiate_data_transformation()
            )

            logging.info(
                f"data transformation artifacts : {data_transformation_artifacts}"
            )
            logging.info(f"{'<<'*30} Data Transformation component completed {'>>'*30}")
            return data_transformation_artifacts
        except Exception as e:
            logging.info(
                f"Training pipeline start data transformation interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def start_model_training(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ) -> ModelTrainerArtifact:
        try:
            logging.info(f"{'<<'*30} Model Training component started {'>>'*30}")
            model_trainer = ModelTrainer(
                model_trainer_config=model_trainer_config,
                data_transformation_artifact=data_transformation_artifact,
            )
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info(f"{'<<'*30} Model Training component completed {'>>'*30}")
            return model_trainer_artifacts
        except Exception as e:
            logging.info(
                f"Training pipeline start model training interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def run_pipeline(self):
        try:
            if Trainpipeline.experiment.running_status:
                logging.info(f"pipeline is already running ")
                return Trainpipeline.experiment
            
            logging.info(f"{'=='*30} Training pipeline started {'=='*30}")
            
            experiment_id = str(uuid4())
            
            Trainpipeline.experiment=Experiments(experiment_id=experiment_id,
                                                 running_status=True,
                                                 start_time=datetime.now(),
                                                 stop_time=None,
                                                 execution_time=None,
                                                 is_model_accepted=None,
                                                 message="Pipeline has been started",
                                                 accuracy=None)

            logging.info(f"Pipeline experiments : {Trainpipeline.experiment}")
            
            # self.save_experiment()
            self.save_experiment_in_db()
            
            data_ingestion_artifacts = self.start_data_ingestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_validation_artifact = self.start_data_validation(
                data_validation_config=self.data_validation_config,
                data_ingestion_artifact=data_ingestion_artifacts,
            )
            data_transformation_artifact = self.start_data_transformation(
                data_transformation_config=self.data_transformation_config,
                data_validation_artifact=data_validation_artifact,
            )
            model_training_artifact = self.start_model_training(
                model_trainer_config=self.model_trainer_config,
                data_transformation_artifact=data_transformation_artifact,
            )
            
            stop_time=datetime.now()
            Trainpipeline.experiment = Experiments(experiment_id=Trainpipeline.experiment.experiment_id,
                                                   running_status=False,
                                                   start_time=Trainpipeline.experiment.start_time,
                                                   stop_time=stop_time,
                                                   execution_time=stop_time-Trainpipeline.experiment.start_time,
                                                   message="Pipeline completed",
                                                   is_model_accepted=model_training_artifact.model_accepted,
                                                   accuracy=model_training_artifact.best_model_score)
            # self.save_experiment()
            self.update_experiment_in_db()
            logging.info(f"{'=='*30} Training pipeline completed {'=='*30}")
            return model_training_artifact
        except Exception as e:
            logging.info(
                f"Training pipeline interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)
        
    def run(self)-> ModelTrainerArtifact:
        try:
            training_artifacts = self.run_pipeline()
            return training_artifacts
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def save_experiment_in_db(self):
        try:
            logging.info(f"saving experiment data in database")
            mydict = asdict(Trainpipeline.experiment)
            print(mydict)
            md=Modeltraining(**mydict)
            md.save()
            logging.info(f"experiment data got saved into database")
        except Exception as e:
            raise CustomException(e,sys) 
        
    def update_experiment_in_db(self):
        try:
            logging.info(f"updating experiment data in database")
            mydict=asdict(Trainpipeline.experiment)
            logging.info(f"{mydict}")
            exp_obj = Modeltraining.objects.get(experiment_id=Trainpipeline.experiment.experiment_id)
            exp_obj.execution_time = Trainpipeline.experiment.execution_time
            exp_obj.running_status = Trainpipeline.experiment.running_status
            exp_obj.start_time = Trainpipeline.experiment.start_time
            exp_obj.stop_time = Trainpipeline.experiment.stop_time
            exp_obj.message = Trainpipeline.experiment.message
            exp_obj.accuracy = Trainpipeline.experiment.accuracy
            exp_obj.is_model_accepted = Trainpipeline.experiment.is_model_accepted
            exp_obj.save()
            logging.info(f"experiment data got updated in db")
        except Exception as e:
            raise CustomException(e,sys)

    def save_experiment(Self):
        try:
            logging.info(f"saving experiments into filepath {Trainpipeline.experiment_file_path}")
            if Trainpipeline.experiment.experiment_id is not None:
                experiment = Trainpipeline.experiment
                logging.info(f"{experiment}")
                experiment_dict = asdict(experiment)
                
                experiment_dict : dict = {key : [val] for key,val in experiment_dict.items()}
                
                experiment_report = pd.DataFrame(experiment_dict)
                
                os.makedirs(os.path.dirname(Trainpipeline.experiment_file_path),exist_ok=True)
                if os.path.exists(Trainpipeline.experiment_file_path):
                    experiment_report.to_csv(Trainpipeline.experiment_file_path,index=False,header=False,mode="a")
                else:
                    experiment_report.to_csv(Trainpipeline.experiment_file_path,index=False,header=True,mode="w")
            else:
                logging.info(f"experiment not yet started ")
        except Exception as e:
            logging.info(f"saving experiment interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
