import pandas as pd
import random
import string
from flask import Blueprint,jsonify,request
from data_utils import load_data

anonymization_bp = Blueprint('anonymization', __name__)

@anonymization_bp.route('/anonymization', methods=['POST'])
def anonymize_csv():
    data = request.get_json()
    output_file = data.get('output_file')
    input_file = data.get('input_file')
    df = load_data(input_file)
    # df = pd.read_csv(input_file)
    anonymization_map = {}
    # columns_to_anonymize = ["AnneeDeNaissance","username", "datecreat", "datedeb", "datefin", "raisonsociale", "cliadr", "cliville", "enqueteur", "daterepon", "uidrpnd", "adresse", "wilaya", "sexe", "sitfam", "sitprof", "nivetude", "niveau", "profession"]
    columns_to_anonymize = data.get('columns_to_anonymize')
    df.fillna("", inplace=True)  
    df.rename({'annï¿½ï¿½':'AnneeDeNaissance'},axis=1,  inplace=True, errors='raise')
    df['AnneeDeNaissance'] = df['AnneeDeNaissance'].astype(int, errors='ignore')

    for column in columns_to_anonymize:
        anonymization_map[column] = {}
        
        if column == "username":
            for index, value in df[column].items():
                anonymized_username = ''.join(random.choice(string.ascii_lowercase) for _ in range(len(value)))
                anonymization_map[column][value] = anonymized_username
                df.at[index, column] = anonymized_username
        
        elif column in ["raisonsociale", "cliadr", "cliville", "enqueteur", "adresse"]:
            for index, value in df[column].items():
                anonymized_value = 'Anonymized'
                anonymization_map[column][value] = anonymized_value
                df.at[index, column] = anonymized_value
        
        elif column == "sitfam":
            for index, value in df[column].items():
                anonymized_value = random.choice(["MARIE", "CELIBATAIRE"])
                anonymization_map[column][value] = anonymized_value
                df.at[index, column] = anonymized_value
        
        elif column == "sitprof":
            for index, value in df[column].items():
                anonymized_value = random.choice(["AU_FOYER", "A_SON_COMPTE", "SALARIE", "ETUDIANT"])
                anonymization_map[column][value] = anonymized_value
                df.at[index, column] = anonymized_value
        
        elif column == "nivetude":
            for index, value in df[column].items():
                anonymized_value = random.choice(["MASTER_INGENIEUR", "DOCTEUR", "LICENCE", "FORMATION_PROF", "BAC"])
                anonymization_map[column][value] = anonymized_value
                df.at[index, column] = anonymized_value
        
        elif column == "AnneeDeNaissance":
            for index, value in df[column].items():
                birth_year = int(value)
                anonymized_birth_year = random.randint(birth_year - 10, birth_year + 10)
                anonymization_map[column][value] = anonymized_birth_year
                df.at[index, column] = anonymized_birth_year
        
        elif column == "niveau":
            for index, value in df[column].items():
                anonymized_value = random.randint(1, 5)
                anonymization_map[column][value] = anonymized_value
                df.at[index, column] = anonymized_value

        elif column == "sexe":
            for index, value in df[column].items():
                anonymized_value = random.choice(["H", "F"])
                anonymization_map[column][value] = anonymized_value
                df.at[index, column] = anonymized_value
        
        # Similar anonymization logic can be applied for other columns
        
    df.to_csv(output_file, index=False)
    return jsonify(anonymization_map)

# input_file = 'data2.csv'
# output_file = 'anonymized_output.csv'
# # columns_to_anonymize = ["username", "datecreat", "datedeb", "datefin", "raisonsociale", "cliadr", "cliville", "enqueteur", "daterepon", "uidrpnd", "adresse", "wilaya", "sexe", "sitfam", "sitprof", "nivetude", "niveau", "profession"]

# anonymization_map = anonymize_csv(input_file, output_file, columns_to_anonymize)
# print(anonymization_map)
