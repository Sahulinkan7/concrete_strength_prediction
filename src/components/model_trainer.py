import os, sys
from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from src.utils.commonutils import load_numpy_array
from sklearn.linear_model import LinearRegression, ElasticNet, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.utils.commonutils import read_yaml_file, save_object,load_object


class CustomModel:
    def __init__(self, preprocessing_object : object, model_object : object):
        self.preprocessing_object = preprocessing_object
        self.model_object = model_object

    def predict(self, x):
        try:
            transformed_feature = self.preprocessing_object.transform(x)
            return self.model_object.predict(transformed_feature)
        except Exception as e:
            logging.info(f"interrupted due to {CustomException(e,sys)}")
            raise CustomException(e, sys)

    def __str__(self):
        return f"{type(self.model_object).__name__}()"


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def evaluate_model(self, x_train, y_train, x_test, y_test, models) -> dict:
        try:
            logging.info(f"starting model training and evaluation ")
            models_report = {}
            for i in range(len(list(models))):
                model = list(models.values())[i]

                model.fit(x_train, y_train)

                y_train_pred = model.predict(x_train)
                y_test_pred = model.predict(x_test)

                train_score = r2_score(y_train, y_train_pred)
                test_score = r2_score(y_test, y_test_pred)

                models_report[list(models.keys())[i]] = test_score
            logging.info(f"models evaluation scores as \n {models_report}")
            return models_report

        except Exception as e:
            logging.info(
                f"Evaluation of models interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def fine_tune_model(
        self, best_model_object: object, best_model_name, x_train, y_train
    ):
        try:
            model_param_grid = read_yaml_file(
                self.model_trainer_config.model_trainer_config_filepath
            )["model_selection"]["model"][best_model_name]["search_params"]

            grid_search = GridSearchCV(
                best_model_object,
                param_grid=model_param_grid,
                cv=5,
                verbose=3,
                n_jobs=-1,
            )

            grid_search.fit(x_train, y_train)

            best_params = grid_search.best_params_

            finetuned_model = best_model_object.set_params(**best_params)

            return finetuned_model

        except Exception as e:
            logging.info(
                f"finding best tuned model interrupted due to {CustomException(e,sys)}"
            )
            raise CustomException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info(
                f"splitting train array and test array input and target feature "
            )
            train_array = load_numpy_array(
                self.data_transformation_artifact.transformed_train_filepath
            )
            test_array = load_numpy_array(
                self.data_transformation_artifact.transformed_test_filepath
            )

            logging.info(
                f"splitting train and test array to independent and dependent features "
            )
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            preprocessor = load_object(filepath=self.data_transformation_artifact.preprocessor_filepath)

            models = {
                "LinearRegression": LinearRegression(),
                "Ridge": Ridge(),
                "Lasso": Lasso(),
                "ElasticNet": ElasticNet(),
                "DecisionTreeRegressior": DecisionTreeRegressor(),
                "RandomForestRegressor": RandomForestRegressor(),
                "SVR": SVR(),
            }

            model_evaluation_reports: dict = self.evaluate_model(
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test,
                models=models,
            )

            best_model_score = max(sorted(model_evaluation_reports.values()))

            best_model_name = list(model_evaluation_reports.keys())[
                list(model_evaluation_reports.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            fined_tuned_best_model = self.fine_tune_model(
                best_model_object=best_model,
                best_model_name=best_model_name,
                x_train=x_train,
                y_train=y_train,
            )

            fined_tuned_best_model.fit(x_train, y_train)
            y_test_pred = fined_tuned_best_model.predict(x_test)
            accuracy_score = r2_score(y_test, y_test_pred)
            logging.info(f"accuracy of best tuned model is {accuracy_score}")

            if accuracy_score < 0.7:
                model_accepted = False
            else:
                model_accepted = True
                logging.info(f"best model found ")

                os.makedirs(
                    os.path.dirname(self.model_trainer_config.trained_model_filepath),
                    exist_ok=True,
                )
                logging.info(
                    f"saving model in path : {self.model_trainer_config.trained_model_filepath}"
                )

                custom_model = CustomModel(
                    preprocessing_object=preprocessor, model_object=fined_tuned_best_model
                )

                save_object(
                    file_path=self.model_trainer_config.trained_model_filepath,
                    obj=custom_model,
                )

            model_trainer_artifacts = ModelTrainerArtifact(
                trained_model_path=self.model_trainer_config.trained_model_filepath,
                best_model_score=accuracy_score,
                model_accepted= model_accepted
            )

            return model_trainer_artifacts

        except Exception as e:
            logging.info(
                f"Initiating model training interrupted due to {CustomException(e,sys)}"
            )
