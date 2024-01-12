from src.logger import logging
from src.exception import CustomException
import os,sys 
import pandas as pd 
from src.entity.config_entity import ModelTrainerConfig
from src.utils.commonutils import load_object

def get_data_frame(data_dict:dict):
    try:
        logging.info(f"creating new dataframe ")
        newdict = {}
        for k,v in data_dict.items():
            newdict[k]=[v]
        dataframe = pd.DataFrame(newdict)
        logging.info(dataframe.columns)
        logging.info(f"\n{dataframe.head(1).to_string()}")
        return dataframe
    except Exception as e:
        logging.info(f"Data frmecreation interrupted due to {CustomException(e,sys)}")
        raise CustomException(e,sys)
    

class Prediction:
    def __init__(self):
        pass
    
    def single_output_predict(self,dataframe : pd.DataFrame):
        try:
            logging.info(f"doing single data predition ")
            object_path = ModelTrainerConfig.trained_model_filepath
            if not os.path.exists(object_path):
                return None
            modelobj=load_object(object_path)
            predictedoutput=modelobj.predict(dataframe)
            logging.info(f"predicted output is {predictedoutput}")
            return predictedoutput
        except Exception as e:
            logging.info(f"single data prediction interrupted due to {CustomException(e,sys)}")
            raise CustomException(e,sys)
        
    
    