from datetime import date

empty_object = {}

basic_structure = """{
        name:name of event or the event for which the document is given
        date_of_notification:the date when the notification come
        date_of_commencement:date of starting the application
        end_date:ending of the exam date
        apply_link:only application link for the exam
        event_type:one from the {Exam,Result,AdmitCard}
        document_links:[array of strings]
        details:other details regarding it as in below json 
        }"""

reference_structure = """
{
    "name": "",
    "date_of_notification": "",
    "date_of_commencement": "",
    "end_date": "",
    "apply_link": "",
    "event_type":"",
    "document_links": [],
    "details": {
    "vacancies": {
        "total": ,
        "breakdown": { },
        }
    },
    "eligibility": {
        "age_limit": "",
        "education": { },
        "nationality": [ ]
    },
    "fee": {
        "amount": "",
        "exemptions": ,
    },
    "exam_centers": [],
    "important_dates": { },
    "scheme_of_exam": {
        "subjects": { },
    "contact_details": { }
    }
}
"""

def prompt1 (raw_text,pdf_link, apply_link):
     
    user_prompt = f"""
            
                From the raw data provided,
                Extract appropriate information regarding the exam, events or notices or any admit card or result and store it in reference json format.
                Consider only those events which are currently active or upcoming as of the date {date.today()}.
                just add the events that are listed in the given raw text. 
                
                basic structure:
                {basic_structure}
                
                here is the example of response. Refer to this response:
                {reference_structure}

                here is the raw data: 
                {raw_text}
                
                Instructions:
                
                1.Basic Structure: 
                Generate JSON that strictly follows the key structure given in the basic struture. Do not add any additional parent-level keys beyond what's specified in the basic structure. 

                2.Data Extraction:
                Extract only the data present in the provided raw text.
                Extraction proper content for the keys specified in basic structure from the raw text. Interpret the raw text and identify proper name, dates, etc.
                Provide proper name to event in the name key as per the reference from the pdf.
                If a particular key's data is not available, omit it entirely from the JSON.
                The keys of the json should be same as specified in basic structure. Rest all information must be nested under details key.
                
                3.Event Type Restriction: 
                The event_type value must strictly be one of the following: "Exam", "AdmitCard", or "Result".
                
                4.Document Links and Apply Link:
                Include the following placeholders as simple strings:
                Document links: "{pdf_link}"
                Apply link: "{apply_link}"
                
                5.Details Section Rules:
                Store any additional relevant information from the raw text under the details object.
                Do not include keys with null values.
                Additional nested objects within details are allowed if they are relevant to the raw text but not explicitly mentioned in the reference.
                
                6.Response Output:
                Return only the generated JSON.
                Exclude any introductory or explanatory text. The JSON must represent a well-structured and machine-readable response based solely on the raw text input.
                
                7.Date validation:
                Consider only those events which are upcoming or currently running. Don't include events which are older than date {date.today()}.
                
                8.Give proper JSON with information from the provided raw text only. Take care that the json object conditions are followed. Generate only valid json. After generating the json, re-check it if the format of json as well as nested json objects are proper or not. If the format is not proper, then convert it to a valid format and return the valid json only. Nothing else.
                
                Give me only the proper JSON Object with proper opening and ending brackets as response, not the code to generate it. The keys should be same as in basic structure. Rest all details should be nested as json objects under the details key. Refer the reference structure and output me a similar json response. The keys inside details section may vary as per the raw content. But other keys and structure should remain as it is.
                """
    return user_prompt

def prompt2(raw_text, pdf_link, apply_link):
    user_prompt = f"""
            You are an AI tasked with extracting structured information from unstructured text. Given a raw text extracted from a PDF, you must generate a JSON object that strictly follows a predefined reference structure.all the keys in that reference structure must be there.  
            
            Reference JSON structure:
            {basic_structure}
            
            Instructions:
            Extract relevant information from the provided raw text.
            Fill in all predefined keys with values obtained from the raw text.
            If certain information is missing from the raw text, leave it as an empty string (""), empty list ([]), empty object ({empty_object}), or null as appropriate,.
            The "details" key is optional and should contain any additional structured information that is relevant but does not fit into other predefined keys.
            
            Raw Text:
            {raw_text}
            
            Add {pdf_link} in document_links and {apply_link} in apply_link.
            apply_link must contain a single string.
            Event Type should be either "Exam", "Result" or "AdmitCard" only.
            document_links is an array of simple strings and not json objects.
            Name key should not be empty. Extract a valid name from rawtext.
            Date_of_notification, date_of_commencement and end_date should not be null or empty until no date is specified. 
            Make sure that date is correct. 
            Don't provide wrong information and date.
            Only relevant information extracted from raw text should be considered while creating the json. 
            If couldn't find a correct date, leave it empty. 
            If date_of_notification is not present, set it to {date.today()}
            Only consider those events which are currently active or upcoming as per the date {date.today()}.
            
            Generate a well-formed JSON object based on the above guidelines. The keys: name, date_of_notification, date_of_commencement, end_date, apply_link, event_type and document_links are mandatory. Any other data should be described under details key only. Don't create separate key for that data at top level. Ensure correct formatting and structure.
        """
        
    return user_prompt
        
def prompt3(raw_text,pdf_link, apply_link):

    user_prompt = f"""
        You are an expert data extraction AI specialized in parsing PDF documents into structured JSON. Your task is to extract precise information from raw text while strictly adhering to the required output format.

        Reference JSON structure:
        {basic_structure}

        STRICT EXTRACTION RULES:
        1. MANDATORY FIELDS - These fields MUST be populated with accurate data or default values:
        - name: Extract the Title or Subject from the raw text. If unclear, use the organization/institution name.
        - date_of_notification: Use the exact publication/notification date in YYYY-MM-DD format. If absent, use {date.today()}.
        - date_of_commencement: Extract the start date in YYYY-MM-DD format. If absent, use empty string.
        - end_date: Extract the deadline/closing date in YYYY-MM-DD format. If absent, use empty string.
        - apply_link: Always use exactly {apply_link} - no modifications.
        - event_type: Classify ONLY as "Exam", "Result", or "AdmitCard" based on document content.
        - document_links: Always include {pdf_link} as the first element. Add any additional document links found.

        2. DATE VALIDATION:
        - All dates must be in YYYY-MM-DD format
        - Verify logical date progression (notification ≤ commencement ≤ end_date)
        - Only include events that are active or upcoming as of {date.today()}
        - If a date appears invalid or inconsistent, leave as empty string rather than guessing

        3. CONTENT GUIDELINES:
        - Strictly do not generate any example data , only take data from the raw text
        - document_links must be an array of simple strings, not objects
        - Do not create additional top-level keys beyond those in the reference structure
        - Place any supplementary information in the "details" object
        - Empty values should be "" (strings), [] (arrays), or (objects) as appropriate
        - Never return null values except where explicitly permitted in the reference structure
        - Strictly do not generate any example links , if link is not found then keep it blank 

        4. MANDATORY OUTPUT JSON FORMAT:
        - Structure must be same as reference json structure.
        - Keys: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type" and "document_links" must be present with specified conditions.
        - Additional information must be in json object nested under the "details" key.
        - "event_type" must strictly contain a suitable value from ("Exam","Result", "AdmitCard")
        - The output MUST ONLY contain the specified keys in the json as top level.
        - TOP LEVEL KEYS: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type", "document_links" and "details" as per the above specified value type for each key.
        - Strictly do not generate any example links , if link is not found then keep it blank 


        Raw Text to Process:
        {raw_text}

        OUTPUT REQUIREMENTS:
        - Return ONLY a valid, properly formatted JSON object
        - Do not include explanations, notes, or markdown formatting
        - Verify the output matches all requirements before submitting
        - Double-check that all mandatory fields are populated according to rules
        - Ensure the JSON is properly escaped and valid for direct parsing
        - The output MUST ONLY contain the specified keys in the json as top level.
        - TOP LEVEL KEYS: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type", "document_links" and "details" as per the above specified value type for each key.
        - "event_type" must strictly contain a suitable value from ("Exam","Result", "AdmitCard")
        """
    return user_prompt

def prompt4(raw_text,pdf_link, apply_link):
    user_prompt = f"""
        You are an AI tasked with extracting structured information from unstructured text. Given a raw text extracted from a PDF, you must generate a JSON object that strictly follows a predefined reference structure.all the keys in that reference structure must be there.  
        
        Reference JSON structure:
        {basic_structure}
        
        Instructions:
        Extract relevant information from the provided raw text.
        Fill in all predefined keys with values obtained from the raw text.
        If certain information is missing from the raw text, leave it as an empty string (""), empty list ([]), empty object ({empty_object}), or null as appropriate,.
        The "details" key is optional and should contain any additional structured information that is relevant but does not fit into other predefined keys.
        
        Raw Text:
        {raw_text}
        
        Add {pdf_link} in document_links and {apply_link} in apply_link.
        apply_link must contain a single string.
        Event Type should be either "Exam", "Result" or "AdmitCard" only.
        document_links is an array of simple strings and not json objects.
        Name key should not be empty. Extract a valid name from rawtext.
        Date_of_notification, date_of_commencement and end_date should not be null or empty until no date is specified.
        Make sure that date is correct.
        Don't provide wrong information and date.
        Only relevant information extracted from raw text should be considered while creating the json.
        If couldn't find a correct date, leave it empty.
        If date_of_notification is not present, set it to {date.today()}
        Only consider those events which are currently active or upcoming as per the date {date.today()}.
        
        Generate a well-formed JSON object based on the above guidelines. The keys: name, date_of_notification, date_of_commencement, end_date, apply_link, event_type and document_links are mandatory. Any other data should be described under details key only. Don't create separate key for that data at top level. Ensure correct formatting and structure.
    """
    
    return user_prompt