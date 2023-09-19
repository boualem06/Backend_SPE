

from flask import Flask, jsonify, request, send_file
from flask import Blueprint
import pandas as pd
from flask import jsonify
import os
import io

vars_bp = Blueprint('vars', __name__)

@vars_bp.route('/vars')
def get_vars():
    file_path = './data2.csv'
    data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')
    data = data.drop(data.iloc[:, 0:13], axis=1)
    data.rename({'annï¿½ï¿½': 'AnneeDeNaissance'},
                axis=1,  inplace=True, errors='raise')
    print(data.columns.tolist())
    root_folder = os.getcwd()  # Get the current working directory as the root folder
    csv_data = []

    # for filename in os.listdir(root_folder):
    #     if filename.endswith('.csv'):
    #         file_path = os.path.join(root_folder, filename)
    #         data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')

    #         data = data.drop(data.iloc[:, 13:], axis=1)
    #         csv_data.append({
    #             'filename': filename,
    #             'data': data
    #         })

    # print(csv_data)
    response_data = []
    for res in data.columns.tolist():
        response_data.append({
            "key":res, "value":res
        })

    return jsonify(response_data)


@vars_bp.route('/download', methods=['POST'])
def download():

    data_type = request.json['data_type']  # Get the selected data type (json or csv)
    original_filename = request.json['original_filename']  # Get the original CSV filename

    print(data_type)

    if data_type not in ('json', 'csv') or not original_filename:
        return "Invalid request."
    file_path = './data2.csv'

    data = pd.read_csv(original_filename, delimiter=';', encoding='ISO-8859-1')
    data = data.drop(data.iloc[:, 0:13], axis=1)

    if data_type == 'json':
        data_str = pd.DataFrame(data).to_json(orient='records')
        download_name = 'data.json'
        mimetype = 'application/json'
    elif data_type == 'csv':
        data_str = pd.DataFrame(data).to_csv(index=False)
        download_name = 'data.csv'
        mimetype = 'text/csv'
    data_stream = io.BytesIO(data_str.encode('utf-8'))

    response = send_file(
        data_stream,
        as_attachment=True,
        download_name=download_name,
        mimetype=mimetype
    )

    return response

@vars_bp.route('/filesList', methods=['GET'])
def filesList():
    root_folder = os.getcwd()  # Get the current working directory as the root folder
    csv_files = [f for f in os.listdir(root_folder) if f.endswith('.csv')]
    csv_data = []

    for filename in os.listdir(root_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(root_folder, filename)
            data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')
            data = data.drop(data.iloc[:, 13:], axis=1)         
            csv_data.append({
                'filename': filename,
                'data': data.to_json()
            })

    return jsonify(csv_data)
