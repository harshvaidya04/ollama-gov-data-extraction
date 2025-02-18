import json
from jsonOutputGenerator import generateOutput
import os

# generateOutput("https://psc.ap.gov.in/Documents/NotificationDocuments/Admitcard_172024_23012025.pdf")

supremeData = {}
SupremeFailedData = {
    "state":[],
    "central":[]
}



def generateSupremeJson(supremeData):    
    # central
    orgs = supremeData["central"]

    for org in orgs[1:2]:
        if(org["name"] != "UPSC"):
            organization = org["name"]
            applyLink = org["applyLink"]
            links = org["links"]

            events = []
            failedLinks=[]
            for link in links:
                output = generateOutput(link, applyLink)
                if(output):
                    events.append(output)
                else:
                    failedLinks.append(link)
            
            failedObject = {
                "name": organization,
                "applyLink": applyLink,
                "links": failedLinks
            }
            
            SupremeFailedData["central"].append(failedObject)        
                
            file_path = f"Formatted_data/Central/{organization}.json"

           # Step 1: Check if file exists and read existing data
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

            # Step 2: Append new events to the list
            existingEvents.extend(events)

            # Step 3: Write back the updated list to the file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(existingEvents, f, ensure_ascii=False, indent=4)
            
            print("stored in",organization)

    print("Central done")


    # state
    # states = supremeData['state']

    # for state in states[6:7]:
    #     stateName = state['name']
    #     orgs = state['organizations']
        
    #     if(not os.path.exists(f'Formatted_data/States/{stateName}')):
    #         os.mkdir(f'Formatted_data/States/{stateName}')
        
    #     failedState = {
    #         "name": stateName,
    #         "organizations": []
    #     }
        
    #     for org in orgs[:1]:
    #         organization = org["name"]
    #         applyLink = org['applyLink']
    #         links = org["links"]
            
    #         events = []
    #         failedLinks=[]
            
    #         for link in links:
    #             output = generateOutput(link, applyLink)
    #             if(output):
    #                 events.append(output)
    #             else:
    #                 failedLinks.append(link)
            
    #         failedObject = {
    #             "name":organization,
    #             "applyLink":applyLink,
    #             "links": failedLinks
    #         }
            
    #         failedState["organizations"].append(failedObject)
    #         SupremeFailedData["state"].append(failedState)
            
                    
            # file_path = f"Formatted_data/States/{stateName}/{organization}.json"

            # os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # if os.path.exists(file_path):
            #     with open(file_path, "r", encoding="utf-8") as f:
            #         try:
            #             existingEvents = json.load(f)  # Load existing JSON data
            #             if not isinstance(existingEvents, list):  # Ensure it's a list
            #                 existingEvents = []
            #         except json.JSONDecodeError:
            #             existingEvents = []  # If JSON is corrupted or empty, reset it to an empty list
            # else:
            #     existingEvents = []  # If file doesn't exist, start with an empty list

            # existingEvents.extend(events)

            # with open(file_path, "w", encoding="utf-8") as f:
            #     json.dump(existingEvents, f, ensure_ascii=False, indent=4)
            
    #         print("stored in",organization,"json")
            
    # print('states done')


    # UPSC
    # orgs = supremeData["central"]
    # UPSC = next((org for org in orgs if org["name"] == "UPSC"), None)

    # if(not os.path.exists(f'Formatted_data/Multiple/UPSC')):
    #     os.mkdir(f'Formatted_data/Multiple/UPSC')
        
    # orgs = UPSC["organizations"]

    # failedUPSC = {
    #     "name":"UPSC",
    #     "organizations":[]
    # }

    # for org in orgs:
    #     organization = org["name"]
    #     applyLink = org["applyLink"]
    #     links = org["links"]

    #     events = []
    #     failedLinks=[]
    #     for link in links:
    #         output = generateOutput(link, applyLink)
    #         if(output):
    #             events.append(output)
    #         else:
    #             failedLinks.append(link)
            
    #     failedObject = {
    #         "name":organization,
    #         "applyLink": applyLink,
    #         "links": failedLinks
    #     }
        
    #     failedUPSC["organizations"].append(failedObject)
            
        # file_path = f"Formatted_data/Multiple/UPSC/{organization}.json"

        # os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # if os.path.exists(file_path):
        #     with open(file_path, "r", encoding="utf-8") as f:
        #         try:
        #             existingEvents = json.load(f)  # Load existing JSON data
        #             if not isinstance(existingEvents, list):  # Ensure it's a list
        #                 existingEvents = []
        #         except json.JSONDecodeError:
        #             existingEvents = []  # If JSON is corrupted or empty, reset it to an empty list
        # else:
        #     existingEvents = []  # If file doesn't exist, start with an empty list

        # existingEvents.extend(events)

        # with open(file_path, "w", encoding="utf-8") as f:
        #     json.dump(existingEvents, f, ensure_ascii=False, indent=4)
                
    #     print("stored in",organization,"json")

    # print("UPSC done")


    with open ("SupremeFailedLinks.json",'w+', encoding='utf-8') as f:
        json.dump(SupremeFailedData,f) 
        
if __name__ == '__main__':
    with open("documentLinksSupreme.json",'r', encoding='utf-8') as f:
        supremeData = json.load(f)
    
        
    generateSupremeJson(supremeData)
    
    generateSupremeJson(SupremeFailedData)