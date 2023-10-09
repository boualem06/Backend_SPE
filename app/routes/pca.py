from flask import Flask, jsonify
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
from flask_cors import CORS

from flask import Blueprint, request
from data_utils import load_data


pca_bp = Blueprint("pca", __name__)


@pca_bp.route("/PCA", methods=["POST"])
def PcaImplementation():
    file_path = request.json["original_filename"]
    # data = pd.read_csv("./files/" + file_path, delimiter=";", encoding="ISO-8859-1")

    request_data = request.get_json()

    # Check if the 'columns_for_pca' key is present in the JSON data
    if "columns_for_pca" not in request_data:
        return jsonify({"error": "Columns for PCA not provided"}), 400

    columns_for_pca = request_data["columns_for_pca"]

    # file_path = "./output.csv"
    data = load_data(file_path)

    # Select the specified columns and drop any non-numeric columns
    numeric_data = data[columns_for_pca].select_dtypes(include=[np.number])

    # # Handle missing values

    numeric_data.fillna(0, inplace=True)

    # Performing PCA
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data)
    pca = PCA()
    pca_result = pca.fit_transform(scaled_data)
    results_dics = []
    for index, item in enumerate(pca_result):
        results_dics.append({})
        results_dics[index]["val1"] = item[0]
        results_dics[index]["val2"] = item[1]

    explained_variance_ratio = pca.explained_variance_ratio_
    results_dics_var = []
    for index, item in enumerate(explained_variance_ratio):
        results_dics_var.append({})
        results_dics_var[index]["comp"] = "comp" + str(index)
        results_dics_var[index]["var"] = item

    loadings = pca.components_.T * np.sqrt(
        pca.explained_variance_
    )  # this will be used for the loading plot

    result = {
        "pca_result": results_dics,
        "explained_variance_ratio": results_dics_var,
        "loadings": loadings.tolist(),
    }

    return jsonify(result)
