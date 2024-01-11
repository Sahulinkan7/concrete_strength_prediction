import yaml
import numpy as np
import os,sys
from src.exception import CustomException
from src.logger import logging
import pickle

def read_yaml_file(file_path):
    try:
        with open(file_path,'r') as file:
            content=yaml.safe_load(file)
            return content 
    except Exception as e:
        logging.info(f"reading yaml file interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)
    
def save_object(file_path,obj):
    try:
        logging.info(f"saving object in file path : {file_path}")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file:
            pickle.dump(obj=obj,file=file)
    except Exception as e:
        logging.info(f"saving object interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)

def save_numpy_array(file_path,array):
    try:
        logging.info(f"saving numpy array in path : {file_path}")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file:
            np.save(file=file,arr=array)
    except Exception as e:
        logging.info(f"saving numpy array interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)
    
    
def load_numpy_array(file_path)->np.array:
    try:
        logging.info(f"loading numpy array data from {file_path}")
        with open(file_path,'rb') as file:
            return np.load(file=file)
    except Exception as e:
        logging.info(f"loading numpy array data got interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)