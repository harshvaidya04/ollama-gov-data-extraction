import json
from docLinksExtractor import get_document_links
import os

def generateSupremeUpdatedLinks():
    # json initiation
    supremeData = {
        "state":[],
        "central":[]
    }

    newLinksFilePaths = []
    
    # reading existing data
    with open("documentLinksSupreme.json",'r', encoding='utf-8') as f:
        existingSupremeData = json.load(f)


    # Central
    centralData = []
    with open("../Server/data/LinksData/Central/Central.csv", 'r', encoding='utf-8') as f:
        centralData = f.read().split('\n')[1:]
        
    for (idx,cd) in enumerate(centralData):
        data = cd.split(',')
        websiteName = data[0]
        websiteLink = data[1]
        newState = {}
        links = get_document_links(url=websiteLink)
        
        try:
            existingLinks = set(existingSupremeData['central'][idx]["links"])
            newLinks = [link for link in links if link not in existingLinks]
        except Exception:
            newLinks = []
        
        if(len(newLinks) > 0):
            existingSupremeData['central'][idx]['links'].extend(newLinks)
            newLinksFilePaths.append(f'data\\Fomatted_data\\Central\\{websiteName}.json')
        
        newState["name"]=websiteName
        newState["applyLink"]=websiteLink
        newState["links"]=newLinks
        supremeData["central"].append(newState)
        
    print("Central done")


    # UPSC
    UPSCData = []
    with open("../Server/data/LinksData/Multiple/UPSC.csv",'r', encoding='utf-8') as f:   
        UPSCData = f.read().split('\n')[1:]
        
    UPSCRecord = {
        "name":"UPSC",
        "organizations":[]
    }
    
    existingUPSC = [org for org in existingSupremeData['central'] if org['name']=='UPSC'][0]

    for (idx,ud) in enumerate(UPSCData):
        data = ud.split(',')
        websiteName = data[0]
        websiteLink = data[1]
        
        newRecord = {}
        links = get_document_links(url=websiteLink)
        
        try:
            existingLinks = set(existingUPSC['organizations'][idx]['links'])
            newLinks = [link for link in links if link not in existingLinks]
        except Exception:
            newLinks = []
        
        
        if(len(newLinks) > 0):
            for org in existingSupremeData['central']:
                if org['name']=='UPSC':
                    org["links"].extend(newLinks)
                
            newLinksFilePaths.append(f'data\\Fomatted_data\\Multiple\\UPSC\\{websiteName}.json')
        
        newRecord["name"]=data[0]
        newRecord["applyLink"]=websiteLink
        newRecord["links"]=newLinks
        UPSCRecord["organizations"].append(newRecord)
        
    supremeData["central"].append(UPSCRecord)

    print("UPSC done")


    # State
    states = os.listdir('../Server/data/LinksData/States')

    for (stateIdx,state) in enumerate(states):   
        newState = {}
        stateName = state.split('.')[0]    
        newState["name"]=stateName
        newState["organizations"]=[]
        
        stateOrganizations=[]
        with open(f"../Server/data/LinksData/States/{state}",'r', encoding='utf-8') as f:
            stateOrganizations = f.read().split("\n")[1:]
        
        existingState = existingSupremeData['state'][stateIdx]
        
        for (idx,so) in enumerate(stateOrganizations):
            data = so.split(',')
            orgName = data[0]
            orgWebsite = data[1]
            
            links = get_document_links(orgWebsite)
            
            try:
                existingLinks = set(existingState['organizations'][idx]['links'])
                newLinks = [link for link in links if link not in existingLinks]
            except Exception:
                newLinks = []
            
            if(len(newLinks) > 0):
                existingSupremeData['state'][stateIdx]['organizations'][idx]['links'].extend(newLinks)
                newLinksFilePaths.append(f'data\\Fomatted_data\\States\\{stateName}\\{orgName}.json')
            
            newOrg = {}
            newOrg["name"] = orgName
            newOrg["applyLink"] = orgWebsite
            newOrg["links"] = newLinks
            
            newState["organizations"].append(newOrg)    

        supremeData["state"].append(newState)
        print(state, "done")
        
    print("States done")        

        
    with open("../scripts/documentUpdatedLinksSupreme.json","w") as f:
        json.dump(supremeData,f, indent=2)
        
    print("Saved New Links")
    
    with open('../scripts/NewLinksFilePaths.json','w',encoding='utf-8') as f:
        json.dump(newLinksFilePaths,f)
        
    print("Saved File Paths")
    
    with open('../scripts/documentLinksSupreme.json','w',encoding='utf-8') as f:
        json.dump(existingSupremeData,f)

    print("Updated Existing links")

if __name__ == '__main__':
    generateSupremeUpdatedLinks()