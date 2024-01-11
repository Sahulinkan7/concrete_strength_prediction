from dataclasses import dataclass
import os
from src.constants import MODEL_TRAINER_CONFIG_FILE_PATH
@dataclass
class DataIngestionConfig:
    root_dir: str = os.path.join("artifacts","data_ingestion")
    dataset_download_URL : str = f"https://github.com/Sahulinkan7/dataset_repo/raw/main/concrete_data.zip"
    downloaded_data_filepath: str = os.path.join(root_dir,"downloaded_data","concrete.zip")
    extracted_data_filepath: str = os.path.join(root_dir,"extracted_data","concrete_data.csv")
    splitted_dataset_dir : str = os.path.join(root_dir,"splitted_dataset")
    train_dataset_filepath : str = os.path.join(splitted_dataset_dir,"train_dataset","train.csv")
    test_dataset_filepath : str = os.path.join(splitted_dataset_dir,"test_dataset","test.csv")
    
@dataclass
class DataValidationConfig:
    root_dir : str = os.path.join("artifacts","data_validation")
    data_validation_dir : str = os.path.join(root_dir,"data_validation")
    data_validation_status_filepath : str = os.path.join(root_dir,"report.yaml")
    

@dataclass
class DataTransformationConfig:
    root_dir : str = os.path.join("artifacts","data_transformation")
    transformed_train_filepath: str = os.path.join(root_dir,"transformed_data","train.npy")
    transformed_test_filepath: str = os.path.join(root_dir,"transformed_data","test.npy")
    tranformation_object_filepath : str = os.path.join(root_dir,"transformed_object","preprocessor.pkl")
    

@dataclass
class ModelTrainerConfig:
    root_dir : str = os.path.join("artifacts","model_trainer")
    model_trainer_config_filepath = MODEL_TRAINER_CONFIG_FILE_PATH
    trained_model_filepath : str = os.path.join(root_dir,"trained_model","model.pkl")