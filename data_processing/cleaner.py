import pandas as pd
from codegenration.code_genration import CodeGeneration


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
    def drop_na(data: pd.DataFrame, subset=None , dataframe_frame=None) -> pd.DataFrame:
        df = data.dropna(subset=subset)
        dataframe_frame.display_data(df.head(10))
        code = f"df = data.dropna(subset={subset})\n"
        CodeGeneration.generate_code(code)


        

        
