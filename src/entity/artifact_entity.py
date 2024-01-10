from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    raw_data_path : str
    train_data_path: str
    test_data_path: str
    
@dataclass
class DataValidationArtifact:
    data_validation_status : bool
    data_validation_report_filepath : str
    validated_dataset_filepath : str
    validated_train_filepath : str
    validated_test_filepath : str
    
@dataclass
class DataTransformationArtifact:
    preprocessor_filepath : str
    transformed_train_filepath : str
    transformed_test_filepath : str
    
    
    