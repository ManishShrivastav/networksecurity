import sys, os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import (TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import (DataValidationArtifact, DataTransformationArtifact)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import (save_numpy_array_data, save_object)

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(cls) -> Pipeline:
        """
        It initializes the KNNImputer object with the parameters specified in the training_pipeline.py
        file and returns a Pipeline object with the KNNImputer object as the first step.
        
        Args:
            cls: DataTransformation
            
        Returns:
            Pipeline: A pipeline object with KNNImputer
        """
        logging.info("Entered the get_data_transformer_object method of DataTransformation class")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialized KNNImputer with parameters: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor: Pipeline = Pipeline(steps=[("Imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered the initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Started the data transformation process")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # training dataframe
            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            # testing dataframe
            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            # imputer object
            preprocessor = self.get_data_transformer_object()

            # fit_transform the training data nad test data
            preprocessor_object = preprocessor.fit(input_features_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_features_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_features_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # save the transformed data to the specified file paths
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            # Preparing artifacts
            data_transformation_artifact = DataTransformationArtifact(transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                                                                      transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                                                                      transformed_test_file_path=self.data_transformation_config.transformed_test_file_path)
            
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)