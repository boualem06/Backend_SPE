from flask import Flask,jsonify
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.manifold import TSNE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from flask_cors import CORS
from flask import Blueprint


tsne_bp = Blueprint('tsne', __name__)

@tsne_bp.route('/TSNE')
def TsneImplementation():
    file_path = './data2.csv'
    data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')
    data.drop(data.columns[40], axis=1, inplace=True)

    X_numeric = data[['gpslon', 'gpslat']].values

# Convert categorical columns to integers
    data['isparrain'] = data['isparrain'].astype(int)
    data['isanonyme'] = data['isanonyme'].astype(int)

# Combine categorical and numeric data
    X_combined = pd.concat([data[['isparrain', 'isanonyme']], pd.DataFrame(X_numeric, columns=['gpslon', 'gpslat'])], axis=1)

# Perform t-SNE
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    X_tsne = tsne.fit_transform(X_combined)

    X_tsne_list = X_tsne.tolist()
    return jsonify(X_tsne_list)

