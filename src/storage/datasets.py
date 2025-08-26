import os
import pandas as pd
from pathlib import Path

# Paths
ABSOLUTE_PATH = Path(__file__).resolve().parent.parent.parent
datasets_path = os.path.join(ABSOLUTE_PATH, "data", "datasets")

# Files
file_profile = os.path.join(datasets_path, "profile_butik.txt")
file_catalog = os.path.join(datasets_path, "katalog_butik.xlsx")
file_faq = os.path.join(datasets_path, "faq_butik.xlsx")

class Datasets:
    """Provides documents to create the vector store"""
    @staticmethod
    def get_profile() -> str:
        with open(file_profile) as f:
            profile = f.read()
        return profile

    @staticmethod
    def get_catalog() -> pd.DataFrame:
        return pd.read_excel(file_catalog, index_col=None)

    @staticmethod
    def get_faq() -> pd.DataFrame:
        return pd.read_excel(file_faq, index_col=None)