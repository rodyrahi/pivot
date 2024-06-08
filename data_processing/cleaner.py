import pandas as pd

class DataCleaner:
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    @staticmethod
    def clean_data(data: pd.DataFrame) -> pd.DataFrame:
        cleaned_data = data.dropna()
        return cleaned_data

    @staticmethod
    def fill_na(data: pd.DataFrame, value) -> pd.DataFrame:
        return data.fillna(value)

    @staticmethod
    def drop_na(data: pd.DataFrame, subset=None) -> pd.DataFrame:
        return data.dropna(subset=subset)
