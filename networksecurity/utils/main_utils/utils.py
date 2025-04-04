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