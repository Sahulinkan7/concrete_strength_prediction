from dataclasses import dataclass
import os

@dataclass
class DataIngestionConfig:
    root_dir: str = os.path.join("artifacts","data_ingestion")
    dataset_download_URL : str = f"https://github.com/Sahulinkan7/dataset_repo/raw/main/concrete_data.zip"
    downloaded_data_filepath: str = os.path.join(root_dir,"downloaded_data","concrete.zip")
    extracted_data_filepath: str = os.path.join(root_dir,"extracted_data","concrete_data.csv")
    splitted_dataset_dir : str = os.path.join(root_dir,"splitted_dataset")
    train_dataset_filepath : str = os.path.join(splitted_dataset_dir,"train_dataset","train.csv")
    test_dataset_filepath : str = os.path.join(splitted_dataset_dir,"test_dataset","test.csv")