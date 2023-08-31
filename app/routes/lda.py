# from flask import Flask,jsonify
# import pandas as pd
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt
# import numpy as np 
# from sklearn.manifold import TSNE
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from flask_cors import CORS
# from flask import Blueprint,request
# from data_utils import load_data

# lda_bp = Blueprint('lda', __name__)

# @lda_bp.route('/LDA')
# def LdaImplementation():
#     file_path = './data2.csv'
#     data = load_data(file_path)

   
#     # Prepare the data
#     X_numeric = data[['gpslon', 'gpslat']].values

# # Convert categorical columns to integers
#     data['isparrain'] = data['isparrain'].astype(int)
#     data['isanonyme'] = data['isanonyme'].astype(int)

# # Create a categorical target variable based on 'isparrain' and 'isanonyme'
#     target = data['isparrain'] + 2 * data['isanonyme']  # Assuming both are binary (0 or 1)

# # Perform Linear Discriminant Analysis
#     lda = LinearDiscriminantAnalysis()
#     X_lda = lda.fit_transform(X_numeric, target)

#     X_lda_list = X_lda.tolist()
#     print(X_lda_list)
#     return jsonify(X_lda_list)


from flask import Flask, jsonify, request
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from flask_cors import CORS
from flask import Blueprint
from data_utils import load_data
from sklearn.impute import SimpleImputer


lda_bp = Blueprint('lda', __name__)

@lda_bp.route('/LDA', methods=['POST'])
def LdaImplementation():
    # Get the data from the request
    request_data = request.json
    features_columns = request_data['features']  # Feature column names
    target_columns = request_data['target']       # Target column names

    # Load your data into a DataFrame (replace this with your data loading method)
    file_path = './data2.csv'
    data = load_data(file_path)
    # For this example, let's assume you have a 'data' DataFrame loaded
    
    # Convert column names to lowercase
    # features_columns = [col.lower() for col in features_columns]
    # target_columns = [col.lower() for col in target_columns]

    # Convert content of each row in features columns to lowercase
    data[features_columns] = data[features_columns].applymap(lambda x: x.lower() if isinstance(x, str) else x)

    #Convert content of each row in targets columns to lowercase
    data[target_columns] = data[target_columns].applymap(lambda x: x.lower() if isinstance(x, str) else x)

   
    # Extract the feature and target data
    features_df = data[features_columns]
    target_df = data[target_columns]

    # Encode categorical features using one-hot encoding (if any)
    categorical_features = features_df.select_dtypes(include=['object'])
    numerical_features = features_df.select_dtypes(exclude=['object'])

    
    # onehot_encoder = OneHotEncoder()
    # encoded_categorical_features = onehot_encoder.fit_transform(categorical_features).toarray()

    # Encode categorical features using get_dummies
    encoded_categorical_features = pd.get_dummies(features_df, columns=categorical_features.columns)

    # Combine the encoded features and numerical features
    final_features = pd.concat([encoded_categorical_features, numerical_features], axis=1)

    # Combine the encoded features and numerical features
    # final_features = pd.concat([pd.DataFrame(encoded_categorical_features), numerical_features], axis=1)

    # Preprocess the data to handle missing values using SimpleImputer
    imputer = SimpleImputer(strategy='mean')
    final_features_imputed = imputer.fit_transform(final_features)

    # Perform Linear Discriminant Analysis for each target variable
    lda_results = {}
    for target_col in target_columns:
        target = target_df[target_col]
        # Handle missing values in the target
        target = target.fillna(-1)  # Replace NaN with a placeholder value, or choose an appropriate value
        if target.dtype == 'object':  # Categorical target
            target_labels = LabelEncoder().fit_transform(target)
        else:  # Numerical target
            target_labels = target

        lda = LinearDiscriminantAnalysis()
        X_lda = lda.fit_transform(final_features_imputed, target_labels)

        # X_lda_list = X_lda.tolist()
        # lda_results[target_col] = X_lda_list
         # Create a list of dictionaries for each component
        component_dicts = []
        for row in X_lda:
            component_dict = {}
            for i, val in enumerate(row):
                component_dict[f'val{i + 1}'] = val
            component_dicts.append(component_dict)

        lda_results[target_col] = component_dicts

    return jsonify(lda_results)


