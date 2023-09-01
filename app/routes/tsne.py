
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
    result_list = []
    for point in X_tsne:
        result_list.append({"val1": float(point[0]), "val2": float(point[1])})  # Convert to Python float
    
    return jsonify(result_list)



