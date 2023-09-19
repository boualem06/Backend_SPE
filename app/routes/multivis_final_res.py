import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify,Blueprint
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


from data_utils import load_data

multivis_final_res_bp = Blueprint('multivis_final_res', __name__)

var="hello"

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
    
    threshold = 70  # Adjust the threshold as needed

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
    temp_array=[]
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
        temp_dict={}
        final_dic["column_name"]=column_name 
        temp_dict["column_name"]=column_name 
        #print(column_name)
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
                #print(word_heighest_sim)
                final_dic[word_heighest_sim]=count
                temp_dict[word_heighest_sim]=list_similaire_words
        #     #print(word)
        # #print(word_heighest_sim)
        #     print(list_similaire_words)
        #     print("====================================================")
        
        
        final_res.append(final_dic)
        temp_array.append(temp_dict)
    return (final_res,temp_array)



@multivis_final_res_bp.route('/multivis_final_res', methods=['POST'])
def visualize_data_and_plot():
    try:
        file_path = "data2.csv"  # Replace with your actual file path
        df = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')

        column_names = request.json['column_names']
        data_temp=request.json['data_temp']

        print(data_temp)
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

        arra_sim=calculating_similarities(all_response_data)
        result,temp_array = sum_similar_words(all_response_data, arra_sim)
        
        final_resss=[]
        for index,dic in enumerate(result) :
            dicc={}
            dicc['column_name']=dic["column_name"]
            for key,value in dic.items():
        #dic[key]=temp_array[index][key]
                if dicc.get((data_temp[index][key])) is not None:
                    dicc[(data_temp[index][key])]=dicc[(data_temp[index][key])]+value
                else:
                    dicc[(data_temp[index][key])]=value
            final_resss.append(dicc)

        
        return jsonify(final_resss)

    except Exception as e:
        return jsonify({"error": str(e)})

    


