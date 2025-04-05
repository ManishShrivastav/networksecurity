from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import numpy as np
import os, sys
# import dill
import pickle

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            content = yaml.safe_load(yaml_file)
        return content
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    
def convert_np_types(obj):
    """Recursively convert numpy data types to native Python types."""
    if isinstance(obj, np.generic):  # This handles np.float64, np.int64, etc.
        return obj.item()  # Convert np.float64 to a native Python float
    elif isinstance(obj, dict):  # If the object is a dictionary, recursively convert its values
        return {key: convert_np_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):  # If the object is a list, recursively convert its elements
        return [convert_np_types(item) for item in obj]
    else:
        return obj  # If it's neither a dict nor a list, return it as-is
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Convert numpy types before dumping to YAML
        content = convert_np_types(content)
        
        with open(file_path, 'w') as file:
            yaml.safe_dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def save_numpy_array_data(file_path: str, array: np.ndarray):
    """Save numpy array data to file file_path: str location of file to save array: np.array data to save"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    
def save_object(file_path: str, obj: object) -> None:
    """Save an object to a file using pickle."""
    try:
        logging.info("Entered the save_object method of Main-Utils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
        logging.info("Exited the save_object method of Main-Utils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists.")
        with open(file_path, 'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load 
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # model.fit(X_train, y_train) # train model

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        
        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys)




