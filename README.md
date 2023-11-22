# enron-pii-detector

Project to extract PII in Enron emails dataset taken from [Kaggle](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset)

## Project Structure

- [`/data`](./data/): Contains the dataset. Only smaller subset of the dataset is uploaded to Github. The full dataset can be downloaded as per instructions in [`00_get_data.ipynb`](./00_get_data.ipynb)
- [`/data/labels/`](./data/labels/): Folder containing human generated labels considered the ground truth for this project.
- [`/data/labels_llm/`](./data/labels_llm/): Folder containing subfolders (basically a subfolder for each different approach or experiment) of LLM generated labels for evaluation.
- [`/src/`](./src/): Folder containing some helper functions and utility functions used in different places in this project.
- [`labeling_app.py`](./labeling_app.py): A little labeling app built with Streamlit to label the dataset. It is this app that generates the ground truth labels in [`/data/labels/`](./data/labels/).
- [`00_get_data.ipynb`](./00_get_data.ipynb): A notebook to download the dataset from Kaggle, extract it, shuffle it, and do some random splits.
- [`01_openai_prompt_engineering.ipynb`](./01_openai_prompt_engineering.ipynb): A notebook to generate labels for the `/data/labels_llm/` folder using OpenAI's API and minimal prompt engineering. This is to serve as a baseline for the LLM approach(s).
- [`02_openai_prompt_engineering_evaluation.ipynb`](./02_openai_prompt_engineering_evaluation.ipynb): A notebook to evaluate the labels generated in [`01_openai_prompt_engineering.ipynb`](./01_openai_prompt_engineering.ipynb) using the ground truth labels in [`/data/labels/`](./data/labels/).
