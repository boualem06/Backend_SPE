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
from data_utils import load_data

lda_bp = Blueprint('lda', __name__)

@lda_bp.route('/LDA')
def LdaImplementation():
    file_path = './data2.csv'
    data = load_data(file_path)
    # Prepare the data
    X_numeric = data[['gpslon', 'gpslat']].values

# Convert categorical columns to integers
    data['isparrain'] = data['isparrain'].astype(int)
    data['isanonyme'] = data['isanonyme'].astype(int)

# Create a categorical target variable based on 'isparrain' and 'isanonyme'
    target = data['isparrain'] + 2 * data['isanonyme']  # Assuming both are binary (0 or 1)

# Perform Linear Discriminant Analysis
    lda = LinearDiscriminantAnalysis()
    X_lda = lda.fit_transform(X_numeric, target)

    X_lda_list = X_lda.tolist()
    print(X_lda_list)
    return jsonify(X_lda_list)