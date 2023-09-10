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
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


univis_bp = Blueprint('univis', __name__)









def levenshtein_distance(word1, word2):
    if len(word1) < len(word2):
        return levenshtein_distance(word2, word1)

    if len(word2) == 0:
        return len(word1)

    previous_row = range(len(word2) + 1)
    for i, c1 in enumerate(word1):
        current_row = [i + 1]
        for j, c2 in enumerate(word2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def highest_sim_word(word_list): #these function allows us to calculate the word that had the heighest similarities to the other words 
    
    most_similar_word = min(word_list, key=lambda word: sum(levenshtein_distance(word, other) for other in word_list))
    return most_similar_word

def calculating_similarities(data): #these function allows us to calculate the similaire words 
    
    threshold = 90  # Adjust the threshold as needed

    similar_words_data = []

    for dictionary in data:
        column_name = dictionary.get("column_name")
        response_counts = dictionary.get("response_counts")
        similar_words = {}

        for word in response_counts.keys():
            matches = process.extract(word, response_counts.keys(), scorer=fuzz.ratio)
            similar_words[word] = [match for match, score in matches if score >= threshold and match != word]

        similar_words_data.append({"column_name":column_name,
                                  "response_counts":similar_words})

    return (similar_words_data)


# ********************************************************************************

def sum_similar_words(plt_count,arra_sim):  #these function allows sum the values of similaire words together and take only the word theat have the max of similarities in these words
    final_res=[]
    arr_word_sim=[]
    for index, elem in enumerate(plt_count):
        arr_word_sim=[]
        column_name=elem["column_name"]
        response_counts=elem["response_counts"]
    
        search_key = 'column_name'
        search_value = column_name
        elem_arra_sim=None
    
        for i, d in enumerate(arra_sim):
            if search_key in d and d[search_key] == search_value:
                elem_arra_sim=d
                break
        final_dic={}
        final_dic["column_name"]=column_name 
        print(column_name)
        for word, count in response_counts.items():
            list_similaire_words=elem_arra_sim["response_counts"][word]
            list_similaire_words.append(word)
            list_similaire_words=[w for w in list_similaire_words if w not in arr_word_sim]
        #list_similaire_words=sorted(list_similaire_words)
            count=0
            for word_sim in list_similaire_words:
                if word_sim in response_counts :
                    count=count+response_counts[word_sim]
                    arr_word_sim.append(word_sim)
            if(list_similaire_words)    :
                word_heighest_sim=highest_sim_word(list_similaire_words)
                print(word_heighest_sim)
                final_dic[word_heighest_sim]=count
       
        #     print(word)
        # #print(word_heighest_sim)
        #     print(list_similaire_words)
        #     print("====================================================")
        
        
        final_res.append(final_dic)
    return (final_res)



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

        arra_sim=calculating_similarities(all_response_data)
        result = sum_similar_words(all_response_data, arra_sim)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})



