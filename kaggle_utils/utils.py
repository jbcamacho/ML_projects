import os
import json
from typing import Any, Dict, Optional
import subprocess
import logging

class KaggleUtils():

    __auth_file_path: str
    __auth_data: Optional[Dict]
    __api: Optional[Any]
    __logger: Optional[logging.Logger]
    def __init__(self, auth_file_path: str = '') -> None:
        self.__auth_file_path = ''
        self.__auth_data = None
        self.__api = None
        self.__logger = None

    def __enter__(self):
        self.__install_kaggle()
        self.__load_kaggle_api_auth()
        self.__kaggle_authenticate()
        self.__init_logger()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print("\nExecution type:", exc_type)
            print("\nExecution value:", exc_value)
            print("\nTraceback:", traceback)

    def __install_kaggle(self):
        pip_list = subprocess.Popen(["python3", "-m", "pip", "list"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # print(pip_list.stdout.read())
        if not 'kaggle' in pip_list.stdout.read():
            subprocess.Popen(["python3", "-m", "pip", "install", "--upgrade", "kaggle", "--quiet"])
        return 1

    def __load_kaggle_api_auth(self) -> bool:
        if not self.__auth_file_path:
            current_dir = os.path.dirname(__file__)
            self.__auth_file_path = os.path.join(current_dir, 'kaggle.json')

        with open(self.__auth_file_path, 'r') as f:
            self.__auth_data = json.load(f)
        try:
            os.environ['KAGGLE_USERNAME'] = self.__auth_data['username']
            os.environ['KAGGLE_KEY'] = self.__auth_data['key']
        except Exception as e:
            raise Exception("An error ocurred while loading the authentication.  \n Error: {e}")
        return 1
        
    def __kaggle_authenticate(self) -> bool:
        from kaggle.api.kaggle_api_extended import KaggleApi
        try:
            api = KaggleApi()
            api.authenticate()
        except Exception as e:
            raise Exception(f"An error ocurred during the authentication. \n Error: {e}")
        self.__api = api
        return 1

    def __init_logger(self):
        from sys import stdout
        self.__logger = logging.getLogger("KaggleUtils")
        self.__logger.addHandler(logging.StreamHandler(stream=stdout))
        self.__logger.setLevel(logging.INFO)

    def kaggle_download_dataset(self, dataset_name: str) -> bool:
        try:
            self.__api.dataset_download_files(dataset=dataset_name, path='.', unzip=True)
        except Exception as e:
            raise Exception(f"An error ocurred while downloading the dataset {dataset_name}. \n Error: {e}")
        else:
            self.__logger.info(f"The dataset '{dataset_name}' was sucessfully downloaded.")
        return 1
    


if __name__ == "__main__":
    load_kaggle_api_auth()
    api = kaggle_authenticate()
    download_dataset(api, "vikrishnan/boston-house-prices")

