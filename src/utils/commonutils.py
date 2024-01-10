import yaml

import os,sys
from src.exception import CustomException
from src.logger import logging

def read_yaml_file(file_path):
    try:
        with open(file_path,'r') as file:
            content=yaml.safe_load(file)
            return content 
    except Exception as e:
        logging.info(f"reading yaml file interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)