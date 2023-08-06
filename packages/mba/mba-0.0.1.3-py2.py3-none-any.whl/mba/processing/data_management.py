import joblib
import pandas as pd
from pathlib import Path

# from mba import __version__ as _version
from mba.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config



def read_data_csv(file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    return dataframe