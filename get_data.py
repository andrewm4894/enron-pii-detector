#%%

import os
from dotenv import load_dotenv
load_dotenv()
import kaggle

#%%

kaggle_username = os.getenv("KAGGLE_USERNAME")
kaggle_api_key = os.getenv("KAGGLE_API_KEY")

dataset_name = "wcukierski/enron-email-dataset"
kaggle.datasets.download(dataset_name)

#%%

kaggle.api.authenticate()

#%%

# save into data folder
!kaggle datasets download -d {dataset_name} -p ./data

#%%

# extract into data folder
!unzip ./data/enron-email-dataset.zip -d ./data
