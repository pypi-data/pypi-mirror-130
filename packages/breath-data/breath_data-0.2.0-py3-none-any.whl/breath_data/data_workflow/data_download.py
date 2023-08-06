from typing import Dict

from breath_api_interface.service_interface.service import Service
from .workflow import Workflow
import os
import requests

pandas_ids = {
                "test_df":"1fAm2QY4dvucpLF_h9zG-xfOsJUXfVGhU",
                "train_df":"1fISYRVTmO83z1lY1LTzpBUKbeX2oUXNA",
                "val_df":"1esyONsK_FFa9K5nJo3rWNOjaVvaLaL78",
                "ens_train_df":"1f1fxlIEXCy1c_mOHgeWgiPQ_PXmrz2zV",
                "ens_val_df":"1f8FAwZJeQCgXHZ40voZ_2KxMD4JXDzrm"
            }

cvs_ids = {
                "test_df.csv":"1f_rHr_7_aW1YGr340mvrAGPehcXo4-Y_",
                "train_df.csv":"1fh0cMKhyVcoAjhXQyipM5SJJ4S8_q5a0",
                "val_df.csv":"1fJ2aCQCm9dPt0sQOH0KeX3Uh3oKrTX8P",
                "ens_train_df.csv":"1fPtVD8zrTDGpistLMuK095VqEg9zBtAb",
                "ens_val_df.csv":"1fS6C6EqrleJkpvPMMA7Ie39K1lVTILqn"
        }

dataset_dict_ids = {"dataset": "1f-JVuN-RhU8kpiDIehpJLJd9HWAcckMO"}

bd_ids = {"breath.db": "1fJOI8FPe7VjvW8ZHcVW1wFW2f6FiJbQZ"}

model_ids = {"model.h5": "1gAwoNEHGkbrTPE9gPYL_lyrEKrn_h4eI",
            "target_dist.json":"1gKVDHr1tsEwuMRiFLCFQ8I_vJyHMG9hP",
            "train_dist.json":"1gD00hqix88dKzvlzHVKQkNEx9H8inpZM"}

# Download functions from https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

class Downloader(Workflow):
    def __init__(self, workflow_service: Service, workflow_name: str, file_dict:Dict[str, str], directory:str):
        super().__init__(workflow_service, workflow_name)
        self._file_dict = file_dict
        self._directory = directory

    def _workflow_run(self):
        for file_name in self._file_dict:
            print("LOG: Downloading "+file_name)
            file_id = self._file_dict[file_name]

            path = os.path.join(self._directory, file_name)

            download_file_from_google_drive(file_id, path)

        print("LOG: Downloads ended with sucess")

class BDDownloader(Downloader):
    def __init__(self, workflow_service: Service, directory:str=""):
        super().__init__(workflow_service, "BDDownloader", bd_ids, directory)

class ModelDownloader(Downloader):
    def __init__(self, workflow_service: Service, directory: str=""):
        super().__init__(workflow_service, "ModelDownloader", model_ids, directory)