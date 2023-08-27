from flask import Flask,jsonify
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.manifold import TSNE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from flask_cors import CORS
#from umap import UMAP



app = Flask(__name__)

CORS(app)

@app.route('/PCA')
def PcaImplementation():
    file_path = './data2.csv'
    data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')
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


@app.route('/TSNE')
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


@app.route('/LDA')
def LdaImplementation():
    file_path = './data2.csv'
    data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')
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

if __name__ == '__main__':
    app.run(debug=True)