import pandas as pd


def load_data(file_path):
    data = pd.read_csv(file_path, delimiter=";", encoding="ISO-8859-1")
    data = data.drop(
        [
            "titre",
            "description",
            "archive",
            "typeform",
            "catform",
            "deflang",
            "username",
            "datecreat",
            "datedeb",
            "datefin",
            "raisonsociale",
            "cliadr",
            "cliville",
        ],
        axis=1,
    )

    return data
