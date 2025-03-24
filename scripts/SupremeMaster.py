from supremeLinksGenerator import generateSupremeLinks
from supremeJsonGenerator import initializeSupremeJsonGenerator
from UPSCEventLinksExtractor import extract_UPSC_links

def initMaster():
    # extract_UPSC_links()
    generateSupremeLinks()
    print("Links Scraped")
    initializeSupremeJsonGenerator()
    print("JSON GENERATION COMPLETE")
    print("GG")
print("GG")
initMaster()