
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
    
    request_data = request.json
    features_columns = request_data['features']  
    target_columns = request_data['target']       

    file_path = request.json["original_filename"]
    data = pd.read_csv("./files/" + file_path, delimiter=";", encoding="ISO-8859-1")
   
    # file_path = './data2.csv'
    # data = load_data(file_path)
    
     # Drop rows with null targets
    data = data.dropna(subset=target_columns)
   

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

    
    

    # Encode categorical features using get_dummies
    encoded_categorical_features = pd.get_dummies(features_df, columns=categorical_features.columns)

    # Combine the encoded features and numerical features
    final_features = pd.concat([encoded_categorical_features, numerical_features], axis=1)

   

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

       
        component_dicts = []
        for row in X_lda:
            component_dict = {}
            for i, val in enumerate(row):
                component_dict[f'val{i + 1}'] = val
            component_dicts.append(component_dict)

        lda_results[target_col] = component_dicts

    return jsonify(lda_results)


