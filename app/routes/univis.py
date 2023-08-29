# import pandas as pd
# from flask import Flask, request, jsonify

# from flask import Blueprint
# from data_utils import load_data


# univis_bp = Blueprint('univis', __name__)



# @univis_bp.route('/univis', methods=['POST'])
# def visualize_data():
#     try:
#         file_path = "data2.csv"  # Replace with your actual file path
#         df = load_data(file_path)
        
#         column_names = request.json['column_names']  # List of column names

#         all_response_data = []

#         for column_name in column_names:
#             # Extract unique responses from the specified column
#             unique_responses = df[column_name].unique()

#             # Remove 'null' and NaN values from the unique_responses list
#             unique_responses = [response for response in unique_responses if pd.notna(response) and response != 'null']

#             # Create a dictionary to store response frequencies
#             response_counts = {response: 0 for response in unique_responses}

#             # Count the occurrences of each response
#             for response in df[column_name]:
#                 if pd.notna(response) and response != 'null':
#                     response_counts[response] += 1

#             response_data = {
#                 "column_name": column_name,
#                 "response_counts": response_counts
#             }
#             all_response_data.append(response_data)

#         return jsonify(all_response_data)

#     except Exception as e:
#         return jsonify({"error": str(e)})


import pandas as pd
from flask import Flask, request, jsonify

from flask import Blueprint
from data_utils import load_data

univis_bp = Blueprint('univis', __name__)

@univis_bp.route('/univis', methods=['POST'])
def visualize_data():
    try:
        file_path = "data2.csv"  # Replace with your actual file path
        df = load_data(file_path)

        column_names = request.json['column_names']  # List of column names

        all_response_data = []

        for column_name in column_names:
            # Extract unique responses from the specified column
            unique_responses = df[column_name].unique()

            # Remove 'null' and NaN values from the unique_responses list
            unique_responses = [response for response in unique_responses if pd.notna(response) and response != 'null']

            # Remove commas and empty responses from the possible responses
            cleaned_responses = []
            for response in unique_responses:
                if isinstance(response, str):  # Check if the response is a string
                    cleaned_response = response.replace(',', '').strip()
                    if cleaned_response != "":
                        cleaned_responses.append(cleaned_response)

            # Create a dictionary to store response frequencies
            response_counts = {response: 0 for response in cleaned_responses}

            # Count the occurrences of each response
            for response in df[column_name]:
                if isinstance(response, str):
                    cleaned_response = response.replace(',', '').strip()
                    if pd.notna(cleaned_response) and cleaned_response != "":
                        response_counts[cleaned_response] += 1

            response_data = {
                "column_name": column_name,
                "response_counts": response_counts
            }
            all_response_data.append(response_data)

        return jsonify(all_response_data)

    except Exception as e:
        return jsonify({"error": str(e)})



