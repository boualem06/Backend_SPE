import pandas as pd
import random
import string
from flask import Blueprint,jsonify,request
from data_utils import load_data

anonymization_bp = Blueprint("anonymization", __name__)

@anonymization_bp.route("/anonymization" )
def anonymize_csv():
    # data = request.get_json()
    # output_file = data.get("output_file")
    # input_file = data.get("input_file")
    # df = load_data(input_file)
    # # df = pd.read_csv(input_file)
    # anonymization_map = {}
    # # columns_to_anonymize =  "AnneeDeNaissance","username", "datecreat", "datedeb", "datefin", "raisonsociale", "cliadr", "cliville", "enqueteur", "daterepon", "uidrpnd", "adresse", "wilaya", "sexe", "sitfam", "sitprof", "nivetude", "niveau", "profession" 
    # columns_to_anonymize = data.get("columns_to_anonymize")
    # df.fillna("", inplace=True)  
    # df.rename({"annï¿½ï¿½":"AnneeDeNaissance"},axis=1,  inplace=True, errors="raise")
    # df "AnneeDeNaissance"  = df "AnneeDeNaissance" .astype(int, errors="ignore")

    # for column in columns_to_anonymize:
    #     anonymization_map column  = {}
        
    #     if column == "username":
    #         for index, value in df column .items():
    #             anonymized_username = "".join(random.choice(string.ascii_lowercase) for _ in range(len(value)))
    #             anonymization_map column  value  = anonymized_username
    #             df.at index, column  = anonymized_username
        
    #     elif column in  "raisonsociale", "cliadr", "cliville", "enqueteur", "adresse" :
    #         for index, value in df column .items():
    #             anonymized_value = "Anonymized"
    #             anonymization_map column  value  = anonymized_value
    #             df.at index, column  = anonymized_value
        
    #     elif column == "sitfam":
    #         for index, value in df column .items():
    #             anonymized_value = random.choice( "MARIE", "CELIBATAIRE" )
    #             anonymization_map column  value  = anonymized_value
    #             df.at index, column  = anonymized_value
        
    #     elif column == "sitprof":
    #         for index, value in df column .items():
    #             anonymized_value = random.choice( "AU_FOYER", "A_SON_COMPTE", "SALARIE", "ETUDIANT" )
    #             anonymization_map column  value  = anonymized_value
    #             df.at index, column  = anonymized_value
        
    #     elif column == "nivetude":
    #         for index, value in df column .items():
    #             anonymized_value = random.choice( "MASTER_INGENIEUR", "DOCTEUR", "LICENCE", "FORMATION_PROF", "BAC" )
    #             anonymization_map column  value  = anonymized_value
    #             df.at index, column  = anonymized_value
        
    #     elif column == "AnneeDeNaissance":
    #         for index, value in df column .items():
    #             birth_year = int(value)
    #             anonymized_birth_year = random.randint(birth_year - 10, birth_year + 10)
    #             anonymization_map column  value  = anonymized_birth_year
    #             df.at index, column  = anonymized_birth_year
        
    #     elif column == "niveau":
    #         for index, value in df column .items():
    #             anonymized_value = random.randint(1, 5)
    #             anonymization_map column  value  = anonymized_value
    #             df.at index, column  = anonymized_value

    #     elif column == "sexe":
    #         for index, value in df column .items():
    #             anonymized_value = random.choice( "H", "F" )
    #             anonymization_map column  value  = anonymized_value
    #             df.at index, column  = anonymized_value
        
    #     # Similar anonymization logic can be applied for other columns
        
    # df.to_csv(output_file, index=False)
     return 'Hello, World!'

# input_file = "data2.csv"
# output_file = "anonymized_output.csv"
# # columns_to_anonymize =  "username", "datecreat", "datedeb", "datefin", "raisonsociale", "cliadr", "cliville", "enqueteur", "daterepon", "uidrpnd", "adresse", "wilaya", "sexe", "sitfam", "sitprof", "nivetude", "niveau", "profession" 

# anonymization_map = anonymize_csv(input_file, output_file, columns_to_anonymize)
# print(anonymization_map)







# {
#   "column_names":  "Raisons Utilisation RS", "Top Of Mind Marque","Top Of Mind Marque DZ" ,
#   "multivis_final_res": {"column_name": "Raisons Utilisation RS", "consultation page marque": "consultation page marque1", "decouverte cultures": "decouverte cultures1", "faireconnaissance": "faireconnaissance1", "pour des raisons professionnelles": "pour des raisons professionnelles1", "suivre actualite": "suivre actualite1","travail": "travail1", "veille ï¿½ï¿½ï¿½ï¿½": "veille ï¿½ï¿½ï¿½ï¿½1"},
#     {"column_name": "Top Of Mind Marque", "apple": "apple1", "ariston": "ariston1", "beko": "beko1", "bershka": "bershka1", "bosh": "bosh1", "brand": "brand1", "christian louboutain": "christian louboutain1", "condor": "condor1", "crostor": "crostor1", "data center": "data center1", "dell": "dell1", "enieme":"enieme1", "geant": "geant1", "gï¿½ï¿½": "gï¿½ï¿½1", "hwawi": "hwawi1", "iphone": "iphone1", "irys": "irys1", "lb": "lb1", "lg": "lg1", "mac": "mac1", "moulinex": "moulinex1", "panasonic": "panasonic1", "philips": "philips1", "pionner dj": "pionner dj1", "samsung": "samsung1", "seb": "seb1", "showme": "showme1", "simense": "simense1", "smartphone": "smartphone1", "sonashi": "sonashi1", "sony":"sony1" , "star sat":"ariston1", "stream":"ariston1", "tablette": "ariston1", "tv": "ariston1", "wirpool": "ariston1", "xomi": "ariston1", "zara": "ariston1", "ýýýýýýýý ýýýýýýýý": "ariston1"}, {"column_name": "Top Of Mind Marque DZ", "aucune": "ariston1", "beko": "ariston1", "bms": "ariston1", "brandt": "ariston1", "condor": "ariston1", "cobra": "ariston1", "cristor": "ariston1", "enie": "ariston1", "enieme": "ariston1", "unie": "ariston1", "uniem": "ariston1", "iris": "ariston1", "geant": "ariston1", "gï¿½ï¿½": "ariston1", "gï¿½ï¿½ï¿½ï¿": "ariston1", "i dont know": "ariston1", "irys": "ariston1", "kiowa": "ariston1", "lg": "ariston1", "raylan": "ariston1", "samsung": "ariston1", "stream": "ariston1", "starlight": "ariston1", "starsat": "ariston1", "ýýniýýme": "ariston1", "ýýýýýýýýýýýý": "ariston1"}  
                  
# }



# {
#   "column_names":  "Raisons Utilisation RS", "Top Of Mind Marque","Top Of Mind Marque DZ" ,
#   "data_temp": {"column_name": "Raisons Utilisation RS", "consultation page marque": "consultation page marque1", "decouverte cultures": "decouverte cultures1", "faireconnaissance": "faireconnaissance1", "pour des raisons professionnelles": "pour des raisons professionnelles1", "suivre actualite": "suivre actualite1","travail": "travail1", "veille ï¿½ï¿½ï¿½ï¿½": "veille ï¿½ï¿½ï¿½ï¿½1"},
#     {"column_name": "Top Of Mind Marque", "apple": "apple1", "ariston": "ariston1", "beko": "beko1", "bershka": "bershka1", "bosh": "bosh1", "brand": "brand1", "christian louboutain": "christian louboutain1", "condor": "condor1", "crostor": "crostor1", "data center": "data center1", "dell": "dell1", "enieme":"enieme1", "geant": "geant1", "gï¿½ï¿½": "gï¿½ï¿½1", "hwawi": "hwawi1", "iphone": "iphone1", "irys": "irys1", "lb": "lb1", "lg": "lg1", "mac": "mac1", "moulinex": "moulinex1", "panasonic": "panasonic1", "philips": "philips1", "pionner dj": "pionner dj1", "samsung": "samsung1", "seb": "seb1", "showme": "showme1", "simense": "simense1", "smartphone": "smartphone1", "sonashi": "sonashi1", "sony":"sony1" , "star sat":"ariston1", "stream":"ariston1", "tablette": "ariston1", "tv": "ariston1", "wirpool": "ariston1", "xomi": "ariston1", "zara": "ariston1", "ýýýýýýýý ýýýýýýýý": "ariston1"}, {"column_name": "Top Of Mind Marque DZ", "aucune": "ariston1", "beko": "ariston1", "bms": "ariston1", "brandt": "ariston1", "condor": "ariston1", "cobra": "ariston1", "cristor": "ariston1", "enie": "ariston1", "enieme": "ariston1", "unie": "ariston1", "uniem": "ariston1", "iris": "ariston1", "geant": "ariston1", "gï¿½ï¿½": "ariston1", "gï¿½ï¿½ï¿½ï¿": "ariston1", "i dont know": "ariston1", "irys": "ariston1", "kiowa": "ariston1", "lg": "ariston1", "raylan": "ariston1", "samsung": "ariston1", "stream": "ariston1", "starlight": "ariston1", "starsat": "ariston1", "ýýniýýme": "ariston1", "ýýýýýýýýýýýý": "ariston1"}  
# }



 
#   {
#     "column_name": "Raisons Utilisation RS",
#     "consultation page marque": 
#       "consultation page marque"
#     ,
#     "decouverte cultures":  
#       "decouverte cultures"
#      ,
#     "faireconnaissance":  
#       "faireconnaissance"
#      ,
#     "pour des raisons professionnelles":  
#       "pour des raisons professionnelles"
#      ,
#     "suivre actualite":  
#       "suivre actualite"
#      ,
#     "travail":  
#       "travail"
#      ,
#     "veille ï¿½ï¿½ï¿½ï¿½":  
#       "veille ï¿½ï¿½ï¿½ï¿½"
     
#   },
#   {
#     "apple":  
#       "apple"
#      ,
#     "ariston":  
#       "ariston"
#      ,
#     "beco":  
#       "beko"
#      ,
#     "bershka":  
#       "bershka"
#      ,
#     "bosh":  
#       "bosh",
      
#      ,
#     "brand":  
#       "brand",
      
#      ,
#     "christian louboutain":  
#       "christian louboutain"
#      ,
#     "column_name": "Top Of Mind Marque",
#     "condor":  
     
#       "condor"
#      ,
#     "crostor":  
#       "crostor"
#      ,
#     "data center":  
#       "data center"
#      ,
#     "dell":  
#       "dell"
#      ,
#     "enieme":  
#       "enieme",
      
#     "geant":  
#       "geant"
#      ,
#     "gï¿½ï¿½":  
#       "gï¿½ï¿½"
#      ,
#     "huawei":  
      
#       "hwawi"
#      ,
#     "iphone":  
#       "iphone"
#      ,
#     "irys":  
#       "irys"
    
#      ,
#     "lb":  
#       "lb"
#      ,
#     "lg":  
#       "lg"
#      ,
#     "mac":  
#       "mac"
#      ,
#     "molinex":  
#       "molinex",
    
#      ,
#     "panasonic":  
#       "panasonic"
#      ,
#     "philips":  
#       "philips"
#      ,
#     "pionner dj":  
#       "pionner dj"
#      ,
#     "samsung":  
      
#       "samsung"
#      ,
#     "seb":  
#       "seb"
#      ,
#     "showme":  
#       "showme"
#      ,
#     "simense":  
#       "simense"
#      ,
#     "smartphone":  
#       "smartphone"
#      ,
#     "sonashi":  
#       "sonashi"
#      ,
#     "sonny":  
#       "sonny",
    
#      ,
#     "star sat":  
#       "star sat"
#      ,
#     "stream":  
#       "stream"
#      ,
#     "tablette":  
#       "tablette"
#      ,
#     "tv":  
#       "tv"
#      ,
#     "wirpool":  
#       "wirpool",
 
#      ,
#     "xomi":  
#       "xiomi"
#      ,
#     "zara":  
#       "zara"
#      ,
#     "ýýýýýýýý ýýýýýýýý":  
    
#       "ýýýýýýýý ýýýýýýýý"
     
#   },
#   {
#     "aucune":  
#       "aucune"
#      ,
#     "beko":  
#       "beko"
#      ,
#     "bms":  
#       "bms"
#      ,
#     "brand":  
   
#       "brandt"
#      ,
#     "cobra":  
#       "cobra"
#      ,
#     "column_name": "Top Of Mind Marque DZ",
#     "condor":  
     
#       "condor"
#      ,
#     "cristor":  
#       "cristor"
#      ,
#     "eni":  
#       "eni",
#      ,
#     "eniem":  
#       "eniem"
#      ,
#     "gean":  
#       "gean",
#      ,
#     "gï¿½ï¿":  
#       "gï¿½ï¿"
#      ,
#     "gï¿½ï¿½":  
#       "gï¿½ï¿½",
#      ,
#     "i dont know":  
#       "i dont know"
#      ,
#     "iris":  
#       "iris"
#      ,
#     "kiowa":  
#       "kiowa"
#      ,
#     "lg":  
#       "lg"
#      ,
#     "raylan":  
#       "raylan"
#      ,
#     "samsung":  
#       "samsung"
#      ,
#     "sream":  
#       "sream",
#      ,
#     "starlight":  
#       "starlight"
#      ,
#     "starsat":  
#       "starsat"
#      ,
#     "ýýniýýme":  
#       "ýýniýýme"
#      ,
#     "ýýýýýýýýýý":  
#       "ýýýýýýýýýý",

     
#   }
 