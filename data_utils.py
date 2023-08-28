import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')
    return data