import json
from jsonOutputGenerator import generateOutput
import os

# generateOutput("https://psc.ap.gov.in/Documents/NotificationDocuments/Admitcard_172024_23012025.pdf")

    
# global supremeData
# global SupremeFailedData
# supremeData = {}


    # with open ('SupremeFailedLinksTemp.json','r',encoding='utf-8') as f:
    #     try:
    #         SupremeFailedDataTemp = json.load(f)
    #         if isinstance(SupremeFailedDataTemp,dict):
    #             SupremeFailedData = SupremeFailedDataTemp
    #     except Exception:
    #         pass


    
def generateSupremeJson(supremeData):    
    SupremeFailedData = {
    "state":[],
    "central":[]
    }
    
    
    # central
    # orgs = supremeData["central"]

    # for org in orgs[17:]:
    # # for org in orgs[7:]:
    #     if(org["name"] != "UPSC"):
    #         organization = org["name"]
    #         applyLink = org["applyLink"]
    #         links = org["links"]

    #         file_path = f"../Server/data/Formatted_data/Central/{organization}.json"
    #         if(not os.path.exists(file_path)):
    #             with open(file_path,'a') as f:
    #                 pass

    #         failedLinks=[]
    #         for link in links[:5]:
                
                
                
    #             output = generateOutput(link, applyLink)
    #             if(output):
                    
                    

    #                 # Step 1: Check if file exists and read existing data
    #                 if os.path.exists(file_path):
    #                     with open(file_path, "r", encoding="utf-8") as f:
    #                         try:
    #                             existingEvents = json.load(f)  # Load existing JSON data
    #                             if not isinstance(existingEvents, list):  # Ensure it's a list
    #                                 existingEvents = []
    #                         except json.JSONDecodeError:
    #                             existingEvents = []  # If JSON is corrupted or empty, reset it to an empty list
    #                 else:
    #                     existingEvents = []  # If file doesn't exist, start with an empty list

    #                 # Step 2: Append new events to the list
    #                 existingEvents.append(output)

    #                 # Step 3: Write back the updated list to the file
    #                 with open(file_path, "w", encoding="utf-8") as f:
    #                     json.dump(existingEvents, f, ensure_ascii=False, indent=4)
                        
    #             else:
    #                 failedLinks.append(link)
            
    #         failedObject = {
    #             "name": organization,
    #             "applyLink": applyLink,
    #             "links": failedLinks
    #         }
            
    #         SupremeFailedData["central"].append(failedObject)        
    #         with open ('../scripts/SupremeFailedLinksTemp.json','w',encoding='utf-8') as f:
    #             json.dump(SupremeFailedData,f)
            
    #         print("stored in",organization)

    # print("Central done")


    # state
    # states = supremeData['state']

    # for state in states:
    #     stateName = state['name']
    #     orgs = state['organizations']
        
    #     if(not os.path.exists(f'../Server/data/Formatted_data/States/{stateName}')):
    #         os.mkdir(f'../Server/data/Formatted_data/States/{stateName}')
        
    #     failedState = {
    #         "name": stateName,
    #         "organizations": []
    #     }
        
    #     for org in orgs[7:]:
    #         organization = org["name"]
    #         applyLink = org['applyLink']
    #         links = org["links"]
            
            
    #         file_path = f"../Server/data/Formatted_data/States/{stateName}/{organization}.json"
    #         if(not os.path.exists(file_path)):
    #             with open(file_path,'a') as f:
    #                 pass
            
    #         failedLinks=[]
            
    #         for link in links[:5]:
    #             output = generateOutput(link, applyLink)
    #             if(output):

    #                 os.makedirs(os.path.dirname(file_path), exist_ok=True)

    #                 if os.path.exists(file_path):
    #                     with open(file_path, "r", encoding="utf-8") as f:
    #                         try:
    #                             existingEvents = json.load(f)  # Load existing JSON data
    #                             if not isinstance(existingEvents, list):  # Ensure it's a list
    #                                 existingEvents = []
    #                         except json.JSONDecodeError:
    #                             existingEvents = []  # If JSON is corrupted or empty, reset it to an empty list
    #                 else:
    #                     existingEvents = []  # If file doesn't exist, start with an empty list

    #                 existingEvents.append(output)

    #                 with open(file_path, "w", encoding="utf-8") as f:
    #                     json.dump(existingEvents, f, ensure_ascii=False, indent=4)
                        
                        
    #             else:
    #                 failedLinks.append(link)
            
    #         failedObject = {
    #             "name":organization,
    #             "applyLink":applyLink,
    #             "links": failedLinks
    #         }
            
    #         failedState["organizations"].append(failedObject)
            
            
            
            
            
    #         print("stored in",organization,"json")
            
    #     SupremeFailedData["state"].append(failedState)
        
    #     with open ('../scripts/SupremeFailedLinksTemp.json','w',encoding='utf-8') as f:
    #         json.dump(SupremeFailedData,f)
            
    # print('states done')


    # UPSC
    orgs = supremeData["central"]
    UPSC = next((org for org in orgs if org["name"] == "UPSC"), None)

    if(not os.path.exists(f'../Server/data/Formatted_data/Multiple/UPSC')):
        os.mkdir(f'../Server/data/Formatted_data/Multiple/UPSC')
        
    orgs = UPSC["organizations"]

    failedUPSC = {
        "name":"UPSC",
        "organizations":[]
    }
    
    for org in orgs:
        organization = org["name"]
        applyLink = org["applyLink"]
        links = org["links"]


        file_path = f"../Server/data/Formatted_data/Multiple/UPSC/{organization}.json"
        if(not os.path.exists(file_path)):
            with open(file_path,'a') as f:
                pass

        failedLinks=[]
        for link in links[:5]:
            output = generateOutput(link, applyLink)
            if(output):

                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        try:
                            existingEvents = json.load(f)  # Load existing JSON data
                            if not isinstance(existingEvents, list):  # Ensure it's a list
                                existingEvents = []
                        except json.JSONDecodeError:
                            existingEvents = []  # If JSON is corrupted or empty, reset it to an empty list
                else:
                    existingEvents = []  # If file doesn't exist, start with an empty list
                
                existingEvents.append(output)

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(existingEvents, f, ensure_ascii=False, indent=4)
                
            else:
                failedLinks.append(link)
            
        failedObject = {
            "name":organization,
            "applyLink": applyLink,
            "links": failedLinks
        }
        
        failedUPSC["organizations"].append(failedObject)
                
        print("stored in",organization,"json")

    SupremeFailedData['central'].append(failedUPSC)
    
    with open ("../scripts/SupremeFailedLinksTemp.json",'w+', encoding='utf-8') as f:
        json.dump(SupremeFailedData,f) 
    
    print("UPSC done")


    with open ("../scripts/SupremeFailedLinks.json",'w+', encoding='utf-8') as f:
        json.dump(SupremeFailedData,f) 
        
    print("final Failed Save Done")
    
    return SupremeFailedData  
        
if __name__ == '__main__':
    
    with open("../scripts/documentLinksSupreme.json",'r', encoding='utf-8') as f:
        supremeData = json.load(f)
    
        
    SupremeFailedData = generateSupremeJson(supremeData)
    
    
    generateSupremeJson(SupremeFailedData)
    

def initializeSupremeJsonGenerator():
    with open("../scripts/documentLinksSupreme.json",'r', encoding='utf-8') as f:
        supremeData = json.load(f)
    
        
    SupremeFailedData = generateSupremeJson(supremeData)

    
    generateSupremeJson(SupremeFailedData)

def updateSupremeJsonGenerator():
    with open("../scripts/documentUpdateLinksSupreme.json",'r', encoding='utf-8') as f:
        supremeData = json.load(f)
    
    
    SupremeFailedData = generateSupremeJson(supremeData)

    
    generateSupremeJson(SupremeFailedData)