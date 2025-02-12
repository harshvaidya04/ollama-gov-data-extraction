import json
from jsonOutputGenerator import generateOutput
import os

# generateOutput("https://psc.ap.gov.in/Documents/NotificationDocuments/Admitcard_172024_23012025.pdf")

supremeData = {}
with open("documentLinksSupreme.json",'r', encoding='utf-8') as f:
    supremeData = json.load(f)
    
# central
orgs = supremeData["central"]

for org in orgs[1:2]:
    if(org["name"] != "UPSC"):
        organization = org["name"]
        applyLink = org["applyLink"]
        links = org["links"]

        events = []
        for link in links:
            output = generateOutput(link, applyLink)
            events.append(output)
            
        with open(f"Formatted_data/Central/{organization}.json","w", encoding='utf-8') as f:
            json.dump(events,f)
        
        print("stored in",organization,"json")

print("Central done")


# state
# states = supremeData['state']

# for state in states:
#     stateName = state['name']
#     orgs = state['organizations']
    
#     if(not os.path.exists(f'Formatted_data/States/{stateName}')):
#         os.mkdir(f'Formatted_data/States/{stateName}')
    
#     for org in orgs:
#         organization = org["name"]
#         applyLink = org['applyLink']
#         links = org["links"]
        
#         events = []
#         for link in links:
#             output = generateOutput(link, applyLink)
#             events.append(output)
            
#         with open(f"Formatted_data/States/{stateName}/{organization}.json","w", encoding='utf-8') as f:
#             json.dump(events,f)
        
#         print("stored in",organization,"json")
        
# print('states done')


# UPSC
# orgs = supremeData["central"]
# UPSC = next((org for org in orgs if org["name"] == "UPSC"), None)

# if(not os.path.exists(f'Formatted_data/Multiple/UPSC')):
#     os.mkdir(f'Formatted_data/Multiple/UPSC')
    
# orgs = UPSC["organizations"]

# for org in orgs:
#     organization = org["name"]
#     applyLink = org["applyLink"]
#     links = org["links"]

#     events = []
#     for link in links:
#         output = generateOutput(link, applyLink)
#         events.append(output)
        
#     with open(f"Formatted_data/Multiple/UPSC/{organization}.json","w", encoding='utf-8') as f:
#         json.dump(events,f)
    
#     print("stored in",organization,"json")

# print("UPSC done")