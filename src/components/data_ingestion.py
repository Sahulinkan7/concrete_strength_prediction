from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from urllib import request
import zipfile
import pandas as pd
from sklearn.model_selection import train_test_split
import os, sys
from src.logger import logging
from src.exception import CustomException


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        os.makedirs(self.data_ingestion_config.root_dir, exist_ok=True)

    def download_dataset(self, download_url):
        try:
            logging.info(f"downloading dataset from url : {download_url}")
            if not os.path.exists(self.data_ingestion_config.downloaded_data_filepath):
                request.urlretrieve(
                    url=download_url,
                    filename=self.data_ingestion_config.downloaded_data_filepath,
                )
            logging.info(
                f"dataset got downloaded and saved into path : {self.data_ingestion_config.downloaded_data_filepath}"
            )
            return self.data_ingestion_config.downloaded_data_filepath
        except Exception as e:
            logging.info(
                f" downloading dataset interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def extract_dataset(self, downloaded_data_path):
        try:
            logging.info(f"extracting downloaded zip file from {downloaded_data_path}")
            unzip_path = self.data_ingestion_config.extracted_data_filepath
            unzip_dir = os.path.dirname(
                self.data_ingestion_config.extracted_data_filepath
            )
            os.makedirs(os.path.dirname(unzip_dir), exist_ok=True)
            with zipfile.ZipFile(downloaded_data_path, "r") as zip_reference:
                zip_reference.extractall(unzip_dir)
                logging.info(f"dataset got extracted to the path : {unzip_path}")
            return unzip_path
        except Exception as e:
            logging.info(
                f" extracting dataset interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def split_extracted_data(self, extracted_data_path):
        try:
            logging.info(
                "spliting extracted dataset into train data and test data set."
            )
            splitted_dataset_dir = self.data_ingestion_config.splitted_dataset_dir
            os.makedirs(splitted_dataset_dir, exist_ok=True)

            logging.info(f"reading dataset from path : {extracted_data_path}")
            dataframe = pd.read_csv(extracted_data_path)
            logging.info(f"dataframe is as \n {dataframe.head(3).to_string()}")

            os.makedirs(
                os.path.dirname(self.data_ingestion_config.train_dataset_filepath),
                exist_ok=True,
            )
            os.makedirs(
                os.path.dirname(self.data_ingestion_config.test_dataset_filepath),
                exist_ok=True,
            )

            train_df, test_df = train_test_split(
                dataframe, test_size=0.2, random_state=33
            )
            logging.info(f"dataframe splitted into train dataframe and test dataframe ")
            logging.info(
                f"train data shape : {train_df.shape} and test data shape : {test_df.shape}"
            )

            train_df.to_csv(self.data_ingestion_config.train_dataset_filepath)
            test_df.to_csv(self.data_ingestion_config.test_dataset_filepath)

            train_filepath = self.data_ingestion_config.train_dataset_filepath
            test_filepath = self.data_ingestion_config.test_dataset_filepath

            logging.info(f"train dataframe saved in file path  : {train_filepath}")
            logging.info(f"test dataframe saved in file path : {test_filepath}")

            return (train_filepath, test_filepath)

        except Exception as e:
            logging.info(
                f" splitting dataset interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            os.makedirs(
                os.path.dirname(self.data_ingestion_config.downloaded_data_filepath),
                exist_ok=True,
            )
            downloaded_path = self.download_dataset(
                self.data_ingestion_config.dataset_download_URL
            )
            extracted_filepath = self.extract_dataset(
                downloaded_data_path=downloaded_path
            )
            train_filepath, test_filepath = self.split_extracted_data(
                extracted_data_path=extracted_filepath
            )

            data_ingestion_artifacts = DataIngestionArtifact(
                raw_data_path=extracted_filepath,
                train_data_path=train_filepath,
                test_data_path=test_filepath,
            )

            return data_ingestion_artifacts

        except Exception as e:
            raise e
