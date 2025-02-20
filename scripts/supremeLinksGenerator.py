import json
from docLinksExtractor import get_document_links
import os

def generateSupremeLinks():
    # json initiation
    supremeData = {
        "state":[],
        "central":[]
    }

    # # reading existing data
    # with open("documentLinksSupreme.json",'r', encoding='utf-8') as f:
    #     supremeData = json.load(f)


    # Central

    print("Extracting central")
    centralData = []
    with open("../Server/data/LinksData/Central/Central.csv", 'r', encoding='utf-8') as f:
        centralData = f.read().split('\n')[1:]
        
    for cd in centralData:
        data = cd.split(',')
        websiteName = data[0]
        websiteLink = data[1]
        newState = {}
        links = get_document_links(url=websiteLink)
        newState["name"]=websiteName
        newState["applyLink"]=websiteLink
        newState["links"]=links
        supremeData["central"].append(newState)
        
    print("Central done")


    # UPSC

    print("UPSC start")
    UPSCData = []
    with open("../Server/data/LinksData/Multiple/UPSC.csv",'r', encoding='utf-8') as f:   
        UPSCData = f.read().split('\n')[1:]
        
    UPSCRecord = {
        "name":"UPSC",
        "organizations":[]
    }

    for ud in UPSCData:
        data = ud.split(',')
        websiteName = data[0]
        websiteLink = data[1]
        
        newRecord = {}
        
        links = get_document_links(url=websiteLink)
        newRecord["name"]=data[0]
        newRecord["applyLink"]=websiteLink
        newRecord["links"]=links
        UPSCRecord["organizations"].append(newRecord)
        
    supremeData["central"].append(UPSCRecord)

    print("UPSC done")


    # State

    print("State start")
    states = os.listdir('../Server/data/LinksData/States')

    for state in states:   
        newState = {}
        stateName = state.split('.')[0]    
        newState["name"]=stateName
        newState["organizations"]=[]
        
        stateOrganizations=[]
        with open(f"../Server/data/LinksData/States/{state}",'r', encoding='utf-8') as f:
            stateOrganizations = f.read().split("\n")[1:]
            
        for so in stateOrganizations:
            data = so.split(',')
            orgName = data[0]
            orgWebsite = data[1]
            
            links = get_document_links(orgWebsite)
            
            newOrg = {}
            newOrg["name"] = orgName
            newOrg["applyLink"] = orgWebsite
            newOrg["links"] = links
            
            newState["organizations"].append(newOrg)    

        supremeData["state"].append(newState)
        print(state, "done")
        
    print("States done")        

        
    with open("../scripts/documentLinksSupreme.json","w") as f:
        json.dump(supremeData,f, indent=2)

    print("Links stored")

if __name__ == '__main__':
    generateSupremeLinks()