"""by Hubertus Mitschke created on 05/29/22"""
import pandas as pd

def save_data_dict_to_csv(data_dict, save_file_path) -> bool:
    df = pd.DataFrame(data_dict).transpose()
    df.to_csv(save_file_path)
    return True


def open_data_dict_from_csv(url_save_name) -> {str: {str: str}}:
    df = pd.read_csv(url_save_name, index_col=0)
    return df.transpose().to_dict()

