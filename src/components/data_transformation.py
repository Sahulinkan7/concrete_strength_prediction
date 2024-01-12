from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
import os, sys
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import pandas as pd
from src.utils.commonutils import read_yaml_file, save_object, save_numpy_array
from src.constants import SCHEMA_FILE_PATH
import numpy as np


class DataTransformation:
    def __init__(
        self,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact,
    ):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact

            os.makedirs(self.data_transformation_config.root_dir, exist_ok=True)

        except Exception as e:
            raise CustomException(e, sys)

    def get_data_transformation_object(self) -> object:
        try:
            logging.info(f"creating data transformation object")
            logging.info(f"creating pipeline for data transformer object")

            preprocessor = Pipeline(
                steps=[
                    ("imputer", SimpleImputer()),
                    ("scaler", StandardScaler()),
                ]
            )

            logging.info(f"pipeline for data transformer created")
            logging.info(f"data transformer object created")

            return preprocessor

        except Exception as e:
            logging.info(
                f"Data transformation object creation interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f" reading dataframe ")
            train_dataframe = pd.read_csv(
                self.data_validation_artifact.validated_train_filepath
            )
            test_dataframe = pd.read_csv(
                self.data_validation_artifact.validated_test_filepath
            )

            preprocessor = self.get_data_transformation_object()
            target_column = list(
                read_yaml_file(SCHEMA_FILE_PATH)["TARGET_COLUMN"].keys()
            )[0]

            # splitting training dataframe
            logging.info(f"droping target columns from training dataframe ")
            input_feature_train_df = train_dataframe.drop(columns=target_column, axis=1)
            target_feature_train_df = train_dataframe[target_column]
            logging.info(f"columns for model training are \n {input_feature_train_df.columns}")
            logging.info(f"target feature {target_column} dropped from train dataframe")
            logging.info(
                f"input feature train dataframe and target feature dataframe created successfully"
            )

            # splitting test dataframe
            input_feature_test_df = test_dataframe.drop(columns=target_column, axis=1)
            target_feature_test_df = test_dataframe[target_column]
            logging.info(f"target feature dropped from test dataframe")
            logging.info(
                f"input feature test dataframe and target feature dataframe created successfully"
            )

            logging.info(f"before transforming train input features {input_feature_train_df.head(2).to_string()}")
            logging.info(
                f"fitting preprocessor object with input train feature dataframe to create tranformer object"
            )
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(
                input_feature_train_df
            )
            transformed_input_test_feature = preprocessor_object.transform(
                input_feature_test_df
            )

            logging.info("input features of train and test dataframe got transformed")

            train_arr = np.c_[
                transformed_input_train_feature, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                transformed_input_test_feature, np.array(target_feature_test_df)
            ]

            save_object(
                file_path=self.data_transformation_config.tranformation_object_filepath,
                obj=preprocessor_object,
            )
            logging.info(f"preprocessor object got saved successfully .")

            save_numpy_array(
                file_path=self.data_transformation_config.transformed_train_filepath,
                array=train_arr,
            )
            save_numpy_array(
                file_path=self.data_transformation_config.transformed_test_filepath,
                array=test_arr,
            )

            logging.info(
                f"Transformed train array and test array got saved successfully"
            )

            data_transformation_artifact = DataTransformationArtifact(
                preprocessor_filepath=self.data_transformation_config.tranformation_object_filepath,
                transformed_train_filepath=self.data_transformation_config.transformed_train_filepath,
                transformed_test_filepath=self.data_transformation_config.transformed_test_filepath,
            )

            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)
