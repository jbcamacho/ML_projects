import os
import json
from typing import Tuple, Optional

def load_kaggle_api_auth(file_path: str = '') -> bool:
    if not file_path:
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'kaggle.json')
    with open(file_path, 'r') as f:
        auth_data = json.load(f)
    try:
        os.environ['KAGGLE_USERNAME'] = auth_data['username']
        os.environ['KAGGLE_KEY'] = auth_data['key']
    except Exception as e:
        raise Exception("An error ocurred while loading the authentication.  \n Error: {e}")
    return 1

       
def kaggle_authenticate():
    from kaggle.api.kaggle_api_extended import KaggleApi
    try:
        api = KaggleApi()
        api.authenticate()
    except Exception as e:
        raise Exception(f"An error ocurred during the authentication. \n Error: {e}")
    return api

def download_dataset(kaggle_api, dataset_name: str) -> bool:
    try:
        kaggle_api.dataset_download_files(dataset=dataset_name, path='.', unzip=True)
    except Exception as e:
        raise Exception(f"An error ocurred while downloading the dataset {dataset_name}. \n Error: {e}")
    return 1
    


if __name__ == "__main__":
    load_kaggle_api_auth()
    api = kaggle_authenticate()
    download_dataset(api, "vikrishnan/boston-house-prices")

