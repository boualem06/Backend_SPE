from flask import Flask,jsonify
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np 
from flask_cors import CORS

from flask import Blueprint
from data_utils import load_data


pca_bp = Blueprint('pca', __name__)


@pca_bp.route('/PCA')
def PcaImplementation():
    file_path = './data2.csv'
    data = load_data(file_path)
    data.drop(data.columns[40], axis=1, inplace=True)
# Remove non-numeric columns like 'titre', 'description', etc.
    numeric_data = data.drop(['titre', 'description', 'archive', 'typeform', 'catform', 'deflang', 'username', 'datecreat', 'datedeb', 'datefin',
                          'raisonsociale', 'cliadr', 'cliville', 'enqueteur', 'daterepon', 'uidrpnd', 'adresse', 'annï¿½ï¿½', 'wilaya', 'sexe',
                          'sitfam', 'sitprof', 'nivetude', 'profession', 'isparrain', 'isanonyme', 'emploie', 'csp', 'gpslatrepon', 'gpslonrepon',
                          'Present sur RS', 'RS utilise', 'Raisons Utilisation RS', 'Suivre Les Marques', 'Marque Doit etre sur RS',
                          'Top Of Mind Marque', 'Top Of Mind Marque DZ', 'Connaissance Marque Condor',
                          'Origirne de Notorite', 'Suivre Condor sur RS', 'Presence Condor sur RS', 'Decouverte Produit Condor sur RS',
                          'Quel Produit decouvert sur RS', 'Participation Condor Pour la marque', 'Proposition Ecrites'], axis=1)


# Handle missing values if needed

    numeric_data.fillna(0, inplace=True)

# Performing PCA
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data)
    pca = PCA()
    pca_result = pca.fit_transform(scaled_data)
    results_dics = []
    for index,item in enumerate(pca_result):
        results_dics.append({})
        results_dics[index]['val1'] = item[0]
        results_dics[index]['val2'] = item[1]
        results_dics[index]['val3'] = item[2]

    print(pca_result)  #will be used for the scatter plot 
    print("----------------------------------------------------------------------------------------------")
    explained_variance_ratio = pca.explained_variance_ratio_ 
    results_dics_var = []
    for index,item in enumerate(explained_variance_ratio):
        results_dics_var.append({})
        results_dics_var[index]['comp'] = 'comp' + str(index)
        results_dics_var[index]['var'] = item
    print(results_dics_var)

    # print(explained_variance_ratio)  #will be used for the bar plot of variations 
    print("----------------------------------------------------------------------------------------------")
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)  #this will be used for the loading plot 
    print(loadings)


    result = {
        "pca_result": results_dics,
        "explained_variance_ratio": results_dics_var,
        "loadings": loadings.tolist()
    }

    return jsonify(result)