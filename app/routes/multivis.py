import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify,Blueprint



from data_utils import load_data

multivis_bp = Blueprint('multivis', __name__)

@multivis_bp.route('/multivis', methods=['POST'])
def visualize_data_and_plot():
    try:
        file_path = "data2.csv"  # Replace with your actual file path
        df = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')

        column_names = request.json['column_names']

        all_response_data = []

        for column_name in column_names:
            # Get the correct column name using the df.columns attribute
            desired_column_name = column_name
            actual_column_name = [col for col in df.columns if desired_column_name.lower() in col.lower()][0]

            # Extract unique responses from the desired column
            all_responses = []

            # Iterate through each entry and split multiple responses
            for entry in df[actual_column_name]:
                responses = entry.split(',')
                all_responses.extend([response.lower().strip() for response in responses if response.strip() != ""])

            # Convert the list of responses into a Series
            response_series = pd.Series(all_responses)

            # Count the occurrences of each response
            response_counts = response_series.value_counts()

            # Convert response_counts to a dictionary for JSON serialization
            response_counts_dict = response_counts.to_dict()

            response_data = {
                "column_name": column_name,
                "response_counts": response_counts_dict
            }
            all_response_data.append(response_data)

        return jsonify(all_response_data)

    except Exception as e:
        return jsonify({"error": str(e)})


