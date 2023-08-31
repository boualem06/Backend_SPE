# from flask import Flask,jsonify
# import pandas as pd
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt
# import numpy as np 
# from sklearn.manifold import TSNE
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from flask_cors import CORS
# from flask import Blueprint
# from data_utils import load_data


# tsne_bp = Blueprint('tsne', __name__)

# @tsne_bp.route('/TSNE')
# def TsneImplementation():
#     file_path = './data2.csv'
#     data = load_data(file_path)
#     data.drop(data.columns[40], axis=1, inplace=True)

#     X_numeric = data[['gpslon', 'gpslat']].values

# # Convert categorical columns to integers
#     data['isparrain'] = data['isparrain'].astype(int)
#     data['isanonyme'] = data['isanonyme'].astype(int)

# # Combine categorical and numeric data
#     X_combined = pd.concat([data[['isparrain', 'isanonyme']], pd.DataFrame(X_numeric, columns=['gpslon', 'gpslat'])], axis=1)

# # Perform t-SNE
#     tsne = TSNE(n_components=2, perplexity=30, random_state=42)
#     X_tsne = tsne.fit_transform(X_combined)

#     X_tsne_list = X_tsne.tolist()
#     return jsonify(X_tsne_list)



# from flask import Flask, jsonify, request
# import pandas as pd
# from sklearn.manifold import TSNE
# from flask_cors import CORS
# from flask import Blueprint
# from data_utils import load_data

# tsne_bp = Blueprint('tsne', __name__)

# @tsne_bp.route('/TSNE', methods=['POST'])
# def TsneImplementation():
#     # Get JSON data from the request
#     request_data = request.json
    
#     # Load data from CSV file
#     file_path = './data2.csv'
#     data = load_data(file_path)
    
#     # Get selected column names from the request
#     selected_columns = request_data['columns']
    
#     # Extract the selected columns from the data
#     selected_data = data[selected_columns]
    
#     # Remove rows with null values
#     selected_data = selected_data.dropna()
    
#     # Perform t-SNE
#     tsne = TSNE(n_components=2, perplexity=30, random_state=42)
#     X_tsne = tsne.fit_transform(selected_data)
    
#     # Convert t-SNE results to a list for JSON serialization
#     X_tsne_list = X_tsne.tolist()
    
#     return jsonify(X_tsne_list)


from flask import Flask, jsonify, request
import pandas as pd
from sklearn.manifold import TSNE
from flask_cors import CORS
from flask import Blueprint
from data_utils import load_data

tsne_bp = Blueprint('tsne', __name__)

@tsne_bp.route('/TSNE', methods=['POST'])
def TsneImplementation():
    # Get JSON data from the request
    request_data = request.json
    
    # Load data from CSV file
    file_path = './data2.csv'
    data = load_data(file_path)
    
    # Get selected column names from the request
    selected_columns = request_data['columns']
    
    # Filter out non-numeric columns
    numeric_columns = [col for col in selected_columns if pd.api.types.is_numeric_dtype(data[col])]
    
    if not numeric_columns:
        return jsonify({'error': 'No valid numeric columns selected'})
    
    # Extract the selected numeric columns from the data
    print("*****************************************************")
    print(numeric_columns)
    print("*****************************************************")
    selected_data = data[numeric_columns]
    
    # Remove rows with null values
    selected_data = selected_data.dropna()
    
    # Perform t-SNE
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    X_tsne = tsne.fit_transform(selected_data)
    
    # Convert t-SNE results to a list for JSON serialization
    X_tsne_list = X_tsne.tolist()
    
    return jsonify(X_tsne_list)



