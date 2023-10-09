


import pandas as pd
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
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
    temp_array=[]
    simmm=[]
    for index, elem in enumerate(plt_count):
        arr_word_sim=[]
        column_name=elem["column_name"]
        response_counts=elem["response_counts"]
        obj={}
        obj[elem["column_name"]]=[]

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
        final_dic["values"]=[]
        temp_dict["column_name"]=column_name 
       
        for word, count in response_counts.items():
            list_similaire_words=elem_arra_sim["response_counts"][word]
            list_similaire_words.append(word)
            list_similaire_words=[w for w in list_similaire_words if w not in arr_word_sim]
       
            count=0
            for word_sim in list_similaire_words:
                if word_sim in response_counts :
                    count=count+response_counts[word_sim]
                    arr_word_sim.append(word_sim)
            if(list_similaire_words)    :
                word_heighest_sim=highest_sim_word(list_similaire_words)
                obj[elem["column_name"]].append({word_heighest_sim:list_similaire_words})

                final_dic["values"].append({column_name:word_heighest_sim,"value":count})
                temp_dict[word_heighest_sim]=list_similaire_words
      
        
        simmm.append(obj)
        final_res.append(final_dic)
        temp_array.append(temp_dict)
    return (final_res,temp_array,simmm)


#*****************************************************************************************************************
def send_graph(data_cloud):
    

# Example data (replace this with your list of dictionaries)

# Create a dictionary to store colors for each group of similar words
    colors = iter(plt.cm.tab10.colors)

# Initialize a dictionary to store group IDs for words
    word_groups = {}
    final_arr=[]
    temp_obj={}
    final_temp_obj_arr=[]
    # Extract data and prepare coordinates for scatter plot
    for col in data_cloud :
        temp_obj={}
        column_name=next(iter(col))
        temp_obj[column_name]=[]
        data=col[column_name]
        
        for item in data:

            key = list(item.keys())[0]
            similar_words = item[key]
            group_id = len(word_groups)  # Use the current number of groups as the group ID
            x_start = group_id * 3  # Adjust the x-coordinate based on the group ID
            y_start = 1  # Fixed y-coordinate for each group
            
            for word in similar_words:
                word_groups[word] = {'group_id': group_id, 'x': x_start, 'y': y_start}
                temp_obj[column_name].append({word:{'group_id': group_id, 'x': x_start, 'y': y_start}})
                y_start += 3  # Increment the y-coordinate for the next word in the groupinate for the next word in the group
        final_temp_obj_arr.append(temp_obj)
        # Plot scatter plot for the current group of similar words with assigned color
    return (final_temp_obj_arr)


#***************************************************************************************************
def create_plot_data(data_cloud, word_groups):

    plot_data = []
    for col in data_cloud:
        column_name=next(iter(col))
        data=col[column_name]
        plot_data_obj={column_name:[]}
        
        for item in data:
            key = list(item.keys())[0]  # Get the key from the dictionary
            similar_words = item[key]   # Get the list of similar words
            x_values=[]
            y_values=[]
            # Extract x and y coordinates for similar words
            target_key = column_name
            for obj in word_groups:
                if target_key in obj:
                    target_value = obj[target_key]
                    break


            #x_values = [d[word]['x'] for word in similar_words]
            for item_two in target_value:
                for key_two in item_two.keys():
                    if key_two in similar_words:
                        x_values.append(item_two[key_two]['x'])
                        y_values.append(item_two[key_two]['y'])
           # y_values = [d[word]['y'] for word in similar_words]

            # Create the plot object
            plot_object = {
                'name': key,
                'x': x_values,
                'y': y_values,
                'text': similar_words,
                'mode': 'markers+text',
                'type': 'scatter',
                'textfont': {
                    'family': 'Times New Roman'
                },
                'textposition': 'bottom center',
                'marker': {'size': 12}
            }

            # Append the object to the plot_data list
            plot_data_obj[column_name].append(plot_object)

        plot_data.append(plot_data_obj)
    return plot_data



@univis_bp.route('/univis', methods=['POST'])
def visualize_data():
    try:
        # file_path = "data2.csv"  
        file_path = request.json["original_filename"]
        df = pd.read_csv("./files/" + file_path, delimiter=";", encoding="ISO-8859-1")
        #df = load_data(file_path)

        column_names = request.json['column_names']  

        all_response_data = []

        for column_name in column_names:
            # Extract unique responses from the specified column
            unique_responses = df[column_name].unique()

            # Remove 'null' and NaN values from the unique_responses list
            unique_responses = [response for response in unique_responses if pd.notna(response) and response != 'null']

            # Remove commas and empty responses from the possible responses
            cleaned_responses = []
            for response in unique_responses:
                if isinstance(response, str) :  # Check if the response is a string
                    cleaned_response = response.replace(',', '').strip()
                    if cleaned_response != "":
                        cleaned_responses.append(cleaned_response)
                if isinstance(response,float):
                    cleaned_responses.append(response)
                

            # Create a dictionary to store response frequencies
            if (isinstance(cleaned_responses[0],str)):
                response_counts = {response: 0 for response in cleaned_responses}
            elif (isinstance(cleaned_responses[0],float)):
                response_counts={}
            # Count the occurrences of each response
            cn=0
            for response in df[column_name]:
                if isinstance(response, str)  :
                    cleaned_response = response.replace(',', '').strip()
                    if pd.notna(cleaned_response) and cleaned_response != "":
                        response_counts[cleaned_response] += 1
                elif(isinstance(response, float) ):
                     if pd.notna(response):
                        response_counts[str(cn)] =response
                        cn=cn+1
               


            response_data = {
                "column_name": column_name,
                "response_counts": response_counts
            }
            all_response_data.append(response_data)

        arra_sim=calculating_similarities(all_response_data)
        result,temp_array,simmm = sum_similar_words(all_response_data, arra_sim)
        word_groups=send_graph(simmm)
        plot_data=create_plot_data(simmm, word_groups)
        return jsonify({"result":result,"plot_data":plot_data})

    except Exception as e:
        return jsonify({"error": str(e)})



