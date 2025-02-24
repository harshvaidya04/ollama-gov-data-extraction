import requests
import json
from docParser import extract_content_from_pdf
from docParserOCR import extract_text_from_pdf
from datetime import date
from DeviceConstants import model

def generateOutput(pdf_link, apply_link):
    try:
        raw_text = extract_text_from_pdf(pdf_link)
        if(raw_text==''):
            return json.loads(raw_text)
            
        with open('../scripts/raw_text.txt','w',encoding='utf-8') as f:
            f.write(raw_text)
        
        print("raw text extracted")
        
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
        
        # user_prompt = f"""
        
        #     From the raw data provided,
        #     Extract appropriate information regarding the exam, events or notices or any admit card or result and store it in reference json format.
        #     Consider only those events which are currently active or upcoming as of the date {date.today()}.
        #     just add the events that are listed in the given raw text. 
            
        #     basic structure:
        #     {basic_structure}
            
        #     here is the example of response. Refer to this response:
        #     {reference_structure}

        #     here is the raw data: 
        #     {raw_text}
            
        #     Instructions:
            
        #     1.Basic Structure: 
        #     Generate JSON that strictly follows the key structure given in the basic struture. Do not add any additional parent-level keys beyond what's specified in the basic structure. 

        #     2.Data Extraction:
        #     Extract only the data present in the provided raw text.
        #     Extraction proper content for the keys specified in basic structure from the raw text. Interpret the raw text and identify proper name, dates, etc.
        #     Provide proper name to event in the name key as per the reference from the pdf.
        #     If a particular key's data is not available, omit it entirely from the JSON.
        #     The keys of the json should be same as specified in basic structure. Rest all information must be nested under details key.
            
        #     3.Event Type Restriction: 
        #     The event_type value must strictly be one of the following: "Exam", "AdmitCard", or "Result".
            
        #     4.Document Links and Apply Link:
        #     Include the following placeholders as simple strings:
        #     Document links: "{pdf_link}"
        #     Apply link: "{apply_link}"
            
        #     5.Details Section Rules:
        #     Store any additional relevant information from the raw text under the details object.
        #     Do not include keys with null values.
        #     Additional nested objects within details are allowed if they are relevant to the raw text but not explicitly mentioned in the reference.
            
        #     6.Response Output:
        #     Return only the generated JSON.
        #     Exclude any introductory or explanatory text. The JSON must represent a well-structured and machine-readable response based solely on the raw text input.
            
        #     7.Date validation:
        #     Consider only those events which are upcoming or currently running. Don't include events which are older than date {date.today()}.
            
        #     8.Give proper JSON with information from the provided raw text only. Take care that the json object conditions are followed. Generate only valid json. After generating the json, re-check it if the format of json as well as nested json objects are proper or not. If the format is not proper, then convert it to a valid format and return the valid json only. Nothing else.
            
        #     Give me only the proper JSON Object with proper opening and ending brackets as response, not the code to generate it. The keys should be same as in basic structure. Rest all details should be nested as json objects under the details key. Refer the reference structure and output me a similar json response. The keys inside details section may vary as per the raw content. But other keys and structure should remain as it is.
        #     """
            
            # Give me only json as per the reference format only. The keys of the generated json should be same as basic structure format of json. If that particular data is present in raw text then include it, otherwise don't include anything extra. All the additional details should be displayed as json objects nested under the details object. Only specified keys should be created at parent level as per basic structure. Event type should be either "Exam", "AdmitCard" or "Result" only. Also add "{pdf_link}" as simple string in document links array and "{apply_link}" as simple string to apply_link. In details section, don't include null object. Additionally you can also add additional objects in details which are there in raw text but not mentioned in reference. All the content of json should come from raw text. Reference is just for referring the structure, don't include that data in final response. Return only the generated json, no additional text.
        
        empty_object = {}
        
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
        
        # user_prompt = f"""
        #     You are an expert data extraction AI specialized in parsing PDF documents into structured JSON. Your task is to extract precise information from raw text while strictly adhering to the required output format.

        #     Reference JSON structure:
        #     {basic_structure}

        #     STRICT EXTRACTION RULES:
        #     1. MANDATORY FIELDS - These fields MUST be populated with accurate data or default values:
        #     - name: Extract the Title or Subject from the raw text. If unclear, use the organization/institution name.
        #     - date_of_notification: Use the exact publication/notification date in YYYY-MM-DD format. If absent, use {date.today()}.
        #     - date_of_commencement: Extract the start date in YYYY-MM-DD format. If absent, use empty string.
        #     - end_date: Extract the deadline/closing date in YYYY-MM-DD format. If absent, use empty string.
        #     - apply_link: Always use exactly {apply_link} - no modifications.
        #     - event_type: Classify ONLY as "Exam", "Result", or "AdmitCard" based on document content.
        #     - document_links: Always include {pdf_link} as the first element. Add any additional document links found.

        #     2. DATE VALIDATION:
        #     - All dates must be in YYYY-MM-DD format
        #     - Verify logical date progression (notification ≤ commencement ≤ end_date)
        #     - Only include events that are active or upcoming as of {date.today()}
        #     - If a date appears invalid or inconsistent, leave as empty string rather than guessing

        #     3. CONTENT GUIDELINES:
        #     - Strictly do not generate any example data , only take data from the raw data
        #     - document_links must be an array of simple strings, not objects
        #     - Do not create additional top-level keys beyond those in the reference structure
        #     - Place any supplementary information in the "details" object
        #     - Empty values should be "" (strings), [] (arrays), or (objects) as appropriate
        #     - Never return null values except where explicitly permitted in the reference structure
        #     - Strictly do not generate any example links , if link is not found then keep it blank 

        #     4. MANDATORY OUTPUT JSON FORMAT:
        #     - Structure must be same as reference json structure.
        #     - Keys: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type" and "document_links" must be present with specified conditions.
        #     - Additional information must be in json object nested under the "details" key.
        #     - "event_type" must strictly contain a suitable value from ("Exam","Result", "AdmitCard")
        #     - The output MUST ONLY contain the specified keys in the json as top level.
        #     - TOP LEVEL KEYS: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type", "document_links" and "details" as per the above specified value type for each key.
        #     - Strictly do not generate any example links , if link is not found then keep it blank 


        #     Raw Text to Process:
        #     {raw_text}

        #     OUTPUT REQUIREMENTS:
        #     - Return ONLY a valid, properly formatted JSON object
        #     - Do not include explanations, notes, or markdown formatting
        #     - Verify the output matches all requirements before submitting
        #     - Double-check that all mandatory fields are populated according to rules
        #     - Ensure the JSON is properly escaped and valid for direct parsing
        #     - The output MUST ONLY contain the specified keys in the json as top level.
        #     - TOP LEVEL KEYS: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type", "document_links" and "details" as per the above specified value type for each key.
        #     - "event_type" must strictly contain a suitable value from ("Exam","Result", "AdmitCard")
        #     """
        
        # user_prompt = f"""
        #         You are an AI tasked with **extracting structured information** from unstructured text. Your goal is to **generate a JSON object that strictly follows a predefined reference structure** with **no missing or extra keys**. The output must always match the reference structure and maintain high accuracy.

        #         **Reference JSON structure:**  
        #         {basic_structure}

        #         ##  STRICT EXTRACTION RULES:
        #          MANDATORY FIELDS - These fields MUST be populated with accurate data or default values:
        #         - name: Extract the Title or Subject from the raw text. If unclear, use the organization/institution name.
        #         - date_of_notification: Use the exact publication/notification date in YYYY-MM-DD format. If absent, use {date.today()}.
        #         - date_of_commencement: Extract the start date in YYYY-MM-DD format. If absent, use empty string.
        #         - end_date: Extract the deadline/closing date in YYYY-MM-DD format. If absent, use empty string.
        #         - apply_link: Always use exactly {apply_link} - no modifications.
        #         - event_type: Classify ONLY as "Exam", "Result", or "AdmitCard" based on document content.
        #         - document_links: Always include {pdf_link} as the first element. Add any additional document links found.
        #         - Structure must be same as reference json structure.
        #         - Keys: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type" and "document_links" must be present with specified conditions.
        #         - Additional information must be in json object nested under the "details" key.
        #         - "event_type" must strictly contain a suitable value from ("Exam","Result", "AdmitCard")
        #         - The output MUST ONLY contain the specified keys in the json as top level.
        #         - TOP LEVEL KEYS: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type", "document_links" and "details" as per the above specified value type for each key.
        #         - Strictly do not generate any example links , if link is not found then keep it blank

        #         ## any other details apart from the mandatory keys/fields shall be strictly nested under details key 

        #         ---
        #         ## 🔹 **Instructions for Data Extraction:**
                
        #         **1️⃣ Adhere Strictly to the Given Structure:**  
        #         - Every key in the reference structure **must** be present.  
        #         - If data is missing, use appropriate defaults:  
        #         - Empty string (`""`) for missing text fields.  
        #         - Empty list (`[]`) for missing array fields.  
        #         - Empty object (`{empty_object}`) for missing nested structures.  
        #         - `null` only if explicitly required.  
        #         - The **"details"** key is optional and should only contain additional structured information that does not fit into the predefined keys.

        #         **2️⃣ Extracting and Validating Information:**  
        #         - **Name (`name`)**: This key **must not be empty**. Extract the most accurate name from the raw text.  
        #         - **Dates (`date_of_notification`, `date_of_commencement`, `end_date`)**:  
        #         - Extract dates carefully to ensure they are **accurate**.  
        #         - If a correct date is unavailable, leave it empty (`""`).  
        #         - If `date_of_notification` is missing, default it to **today's date**: `{date.today()}`.  
        #         - **Event Type (`event_type`)**: Must be one of these three values only: `"Exam"`, `"Result"`, or `"AdmitCard"`.  
        #         - **Links:**  
        #         - `document_links`: Store `{pdf_link}` as a simple string inside the array. Do **not** format it as an object.  
        #         - `apply_link`: Must be a **single valid string** containing `{apply_link}`.  

        #         **3️⃣ Ensuring Data Relevance and Timeliness:**  
        #         - **Only extract active or upcoming events** based on the current date: `{date.today()}`.  
        #         - **Avoid past events** unless explicitly mentioned as still relevant.  
        #         - **Do not fabricate or assume data**—only extract what is clearly present.  

        #         ---
        #         ## 🚀 **Final JSON Output Expectations:**  
        #         - The output must be a **well-formed JSON object** that adheres **strictly to the predefined structure**.  
        #         - **No incorrect values or assumptions**—if data is missing, use the appropriate placeholders.  
        #         - Extract only **relevant** information from the raw text and **do not add extra keys** beyond the reference structure.  

        #         ---
        #         **🔍 Raw Text for Extraction:**  
        #         {raw_text}
                
        #         **🎯 Your task:** Extract structured information as per the above guidelines and return a **precisely formatted JSON object**.  
        #     """

        # user_prompt = f"""
        #         ## 🎯 **TASK OVERVIEW:**  
        #         You are an AI tasked with **extracting structured information** from unstructured text.  
        #         Your goal is to **generate a JSON object that adheres 100% to a predefined reference structure**.  
        #         The output must **strictly** follow this structure **every single time**—with no missing, extra, or incorrectly formatted keys.  

        #         ---
        #         ## 📌 **REFERENCE JSON STRUCTURE (MUST FOLLOW STRICTLY)**  
        #         {basic_structure}  

        #         ---
        #         ## 🔥 **STRICT EXTRACTION RULES (DO NOT DEVIATE)**  

        #         **✅ MANDATORY FIELDS** (Must always be present and correctly formatted):  
        #         - `"name"` → Extract from the raw text (Title or Subject). If unclear, use the organization/institution name.  
        #         - `"date_of_notification"` → Extract the notification date in **YYYY-MM-DD** format. If missing, default to `{date.today()}`.  
        #         - `"date_of_commencement"` → Extract the starting date in **YYYY-MM-DD** format. If missing, use `""`.  
        #         - `"end_date"` → Extract the closing/deadline date in **YYYY-MM-DD** format. If missing, use `""`.  
        #         - `"apply_link"` → Must **always** contain `{apply_link}` (no modifications).  
        #         - `"event_type"` → Must **strictly** be one of: `"Exam"`, `"Result"`, or `"AdmitCard"`.  
        #         - `"document_links"` → Always include `{pdf_link}` as the **first element**. If additional links exist, add them.  
        #         - `"details"` → Any **extra information** must be stored inside this object. Do **not** create additional top-level keys.  

        #         ---
        #         ## ⚠️ **STRICT RULES TO ENFORCE FORMAT**  
        #         - **The output JSON must match the reference structure 100%.**  
        #         - **No missing, incorrect, or extra keys.**  
        #         - **If data is unavailable, use appropriate defaults**:  
        #           - Empty string (`""`) for missing text.  
        #           - Empty list (`[]`) for missing array fields.  
        #           - Empty object (`{empty_object}`) for missing nested structures.  
        #           - `null` only if explicitly required.  
        #         - `"event_type"` **must** be one of **"Exam"**, **"Result"**, or **"AdmitCard"**. **Do not use any other values.**  
        #         - **Do not generate any example links.** If a link is missing, leave it as an **empty string (`""`)**.  
        #         - **Only include upcoming or active events.** Ignore past events unless explicitly mentioned as still relevant.  
        #         - **Do not fabricate or assume information.** Extract only what is clearly present in `{raw_text}`.  

        #         ---
        #         ## 📌 **DATA VALIDATION & EXTRACTION REQUIREMENTS**  

        #         **✅ Name (`name`)**:  
        #         - This **must not be empty**. Extract the most relevant name from the raw text.  
        #         - If unclear, use the **organization/institution name**.  

        #         **✅ Dates (`date_of_notification`, `date_of_commencement`, `end_date`)**:  
        #         - **Ensure correctness**—do not provide incorrect or estimated dates.  
        #         - If a date is missing, use defaults as defined above.  
        #         - `"date_of_notification"` defaults to `{date.today()}` if not provided.  

        #         **✅ Links (`document_links` & `apply_link`)**:  
        #         - `"document_links"` must be a **list of plain strings**, with `{pdf_link}` as the **first element**.  
        #         - `"apply_link"` must be a **single valid string**, containing exactly `{apply_link}`.  

        #         ---
        #         ## 🚀 **FINAL JSON OUTPUT REQUIREMENTS**  
        #         - The output **MUST** be a **valid JSON object** that strictly follows `{basic_structure}`.  
        #         - **No extra keys** should be added beyond `"details"`.  
        #         - **All data must be formatted correctly** per the instructions above.  
        #         - **Every run must produce consistent results** with **no deviations**.  

        #         ---
        #         ## 🔍 **RAW TEXT TO PROCESS:**  
        #         {raw_text}

        #         ---
        #         **🎯 Your task:** Extract structured information per these **strict** guidelines and return a **100% correctly formatted JSON object**.  
        #     """

        #     [SYSTEM]
        #     You are a highly precise PDF data extraction expert AI. Your sole purpose is to parse documents into structured JSON following exact specifications. You must maintain perfect accuracy and format compliance. NEVER generate or invent any data - use ONLY information found in the raw text.

        #     [TASK]
        #     Extract and structure information EXCLUSIVELY from the provided raw text into JSON format. DO NOT generate, assume, or add any information not present in the input text.

        #     [OUTPUT SCHEMA]
        #     {basic_structure}

        #     [CRITICAL FORMAT RULES]
        #     YOU MUST:
        #       - Structure must be same as reference json structure.
        #       - Keys: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type" and "document_links" must be present with specified conditions.
        #       - Additional information must be in json object nested under the "details" key.
        #       - "event_type" must strictly contain a suitable value from ("Exam","Result", "AdmitCard")
        #       - The output MUST ONLY contain the specified keys in the json as top level.
        #       - TOP LEVEL KEYS: "name", "date_of_notification", "date_of_commencement", "end_date", "apply_link", "event_type", "document_links" and "details" as per the above specified value type for each key.
        #       - Strictly do not generate any example links , if link is not found then keep it blank 

        #     [MANDATORY TOP-LEVEL KEYS]
        #     These MUST exist exactly as shown:
        #     1. name (string)
        #     2. date_of_notification (string: YYYY-MM-DD)
        #     3. date_of_commencement (string: YYYY-MM-DD)
        #     4. end_date (string: YYYY-MM-DD)
        #     5. apply_link (string)
        #     6. event_type (string: "Exam" or "Result" or "AdmitCard")
        #     7. document_links (array of strings only)
        #     8. details (object for all other data)

        #     [VALIDATION]
        #     - Compare output structure to reference JSON before returning
        #     - Verify ALL required keys exist
        #     - Verify ALL keys match reference exactly
        #     - Verify data types match reference
        #     - Verify nesting matches reference
        #     - NO extra top-level keys
        #     - document_links must be string array only
        #     - dates must be YYYY-MM-DD
        #     - Use empty strings "", empty arrays [], or empty objects  for missing data

        #     [OUTPUT SCHEMA]
        #     {basic_structure}

        #     [EXTRACTION RULES]
        #     1. MANDATORY FIELDS (100% REQUIRED):
        #     name:
        #     - Extract document Title/Subject FROM RAW TEXT ONLY
        #     - Fall back to organization name if unclear
        #     - NEVER leave empty
        #     - NO generated or example data

        #     date_of_notification:
        #     - Extract ONLY from raw text in YYYY-MM-DD format
        #     - Use exact publication date when found in text
        #     - Default to {date.today()} ONLY if not found in text
        #     - NO generated dates

        #     date_of_commencement:
        #     - Extract ONLY from raw text in YYYY-MM-DD format
        #     - Leave as "" if not found in text
        #     - NO assumptions, guesses, or generated dates

        #     end_date:
        #     - Extract ONLY from raw text in YYYY-MM-DD format
        #     - Extract deadline/closing date from text
        #     - Leave as "" if not found in text
        #     - NO generated dates

        #     apply_link:
        #     - Use EXACTLY: {apply_link}
        #     - NO modifications or generated links

        #     event_type:
        #     - ONLY allowed values: "Exam", "Result", "AdmitCard"
        #     - Classify based SOLELY on document content
        #     - Must choose one based on raw text context
        #     - NO default or assumed values

        #     document_links:
        #     - MUST be an array of strings ONLY
        #     - First element must be: {pdf_link}
        #     - Additional URLs MUST BE FROM RAW TEXT ONLY
        #     - NO generated, example, or placeholder links
        #     - Empty array [] if no additional links in text
        #     - NO metadata or descriptions
        #     - STRICTLY string array of actual links from text

        #     details:
        #     - ALL additional information FROM RAW TEXT must be nested here
        #     - ONLY include data found in input text
        #     - NO generated, assumed, or example data
        #     - NO placeholder or default values

        #     2. DATE VALIDATION REQUIREMENTS:
        #     - Format: YYYY-MM-DD only
        #     - Dates must come FROM RAW TEXT
        #     - Only use {date.today()} as fallback for notification date
        #     - Use "" for any date not found in text

        #     3. CONTENT RULES:
        #     - EXTRACT ONLY from provided raw text
        #     - NO GENERATED DATA WHATSOEVER
        #     - NO EXAMPLE DATA
        #     - NO PLACEHOLDER VALUES
        #     - NO ASSUMED INFORMATION
        #     - ONLY use information present in raw text
        #     - Leave fields empty if data not found in text

        #     4. JSON STRUCTURE REQUIREMENTS:
        #     - Match reference structure exactly
        #     - Required top-level keys (ONLY THESE, NO OTHERS):
        #     * name (from text only)
        #     * date_of_notification (from text or today's date)
        #     * date_of_commencement (from text only)
        #     * end_date (from text only)
        #     * apply_link (exact value provided)
        #     * event_type (from text context)
        #     * document_links (from text only)
        #     * details (from text only)
        #     - NO additional or generated data anywhere

        #     [INPUT TEXT]
        #     {raw_text}

        #     [RESPONSE REQUIREMENTS]
        #     - Use ONLY data from input text
        #     - NO generated content
        #     - NO example data
        #     - NO placeholder values
        #     - NO assumed information
        #     - Leave fields empty if not in text
        #     - Follow schema exactly
        #     - Return only valid JSON

        #     [FORMAT]
        #     Return raw JSON object only using exclusively data from input text.
        #     """


        # call_ollama_api(user_prompt)
        return call_ollama_api(user_prompt)
    except Exception:
        return False

def call_ollama_api(prompt, output_file="output.json"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,  # Replace with your model name
        "prompt": prompt,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()

        responses = [json.loads(entry) for entry in response.text.split('\n') if entry.strip()]
        
        response = responses[0]["response"]
        
        with open('../scripts/response.txt','w',encoding='utf-8') as f:
            f.write(response)
        
        start_index = response.find("{")
        end_index = response.rfind("}") + 1

        # Extract the JSON portion of the string
        jsonResponse = response[start_index:end_index]
        
        with open("../scripts/output.txt", 'w', encoding='utf-8') as file:
            file.write(jsonResponse)
            
        with open("../scripts/output.json", 'w', encoding='utf-8') as file:
            json.dump(json.loads(jsonResponse), file, indent=4)


        print(f"Generated response saved to {output_file}")
        
        return json.loads(jsonResponse)
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"API call or JSON parsing failed: {e}")


if __name__ == "__main__":
    
    
    # with open('raw_text.txt','r', encoding='utf-8') as f:
    #     raw_text = f.read()
    
    # basic_structure = """{
    # name:name of event
    # date_of_notification:the date when the notification come
    # date_of_commencement:date of starting the application
    # end_date:ending of the exam date
    # apply_link:application link for the exam
    # event_type:{Exam,Result,AdmitCard}
    # document_links:related documents given
    # details:other details regarding it as per below json format
    # }"""

    # reference_structure = """
    # {
    #     "name": "National Defence Academy & Naval Academy Examination (II), 2025",
    #     "date_of_notification": "28-05-2025",
    #     "date_of_commencement": "14-09-2025",
    #     "end_date": "17-06-2025",
    #     "apply_link": "https://upsconline.gov.in",
    #     "event_type":"Exam",
    #     "document_links": [],
    #     "details": {
    #     "vacancies": {
    #         "total": 400,
    #         "breakdown": {
    #         "army": 208,
    #         "navy": 42,
    #         "air_force": {
    #             "flying": 92,
    #             "ground_duties_technical": 18,
    #             "ground_duties_non_technical": 10
    #         },
    #         "naval_academy": 36
    #         }
    #     },
    #     "eligibility": {
    #         "age_limit": "Born between 02-01-2007 and 01-01-2010",
    #         "education": {
    #         "army": "12th Class pass",
    #         "navy_air_force": "12th Class pass with Physics, Chemistry, and Mathematics"
    #         },
    #         "nationality": [
    #         "Indian citizen",
    #         "Subject of Nepal",
    #         "Person of Indian origin migrated from specified countries"
    #         ]
    #     },
    #     "fee": {
    #         "amount": "₹100",
    #         "exemptions": ["SC/ST candidates", "Female candidates", "Wards of JCOs/NCOs/ORs"]
    #     },
    #     "exam_centers": ["Agartala", "Ghaziabad", "Navi Mumbai", "..."],
    #     "important_dates": {
    #         "application_correction_window": "18-06-2025 to 24-06-2025",
    #         "results": "October 2025",
    #         "ssb_interviews": "November 2025 to January 2026"
    #     },
    #     "scheme_of_exam": {
    #         "subjects": {
    #         "mathematics": {
    #             "duration": "2.5 hours",
    #             "marks": 300
    #         },
    #         "general_ability_test": {
    #             "duration": "2.5 hours",
    #             "marks": 600
    #         }
    #         },
    #         "ssb_test": {
    #         "marks": 900
    #         }
    #     },
    #     "contact_details": {
    #         "facilitation_counter": "011-23385271, 011-23381125, 011-23098543",
    #         "address": "UPSC Office, Gate C, New Delhi"
    #     }
    #     }
    # }
    # """
    
    # user_prompt = f"""
    
    #     From the raw data provided,
    #     Extract appropriate information regarding the exam, events or notices or any admit card or result and store it in json format.
    #     Consider only those events which are currently active or upcoming.
    #     reference json format:
    #     {basic_structure}
        
    #     here is the example of response. Imitate this response:
    #     {reference_structure}

    #     here is the raw data: 
    #     {raw_text}
        
    #     Give me only json as per the reference format only. The keys of the generated json should be same as given reference json. If that particular data is present in raw text then include it, otherwise don't include anything extra.
    #     """
    #     # here is the refernce JSON Format:
    #     # [
    #     # {reference_structure}   
    #     # ]  
    
    
    # call_ollama_api(user_prompt)
    # call_ollama_api(user_prompt)
    resopnse = call_ollama_api(f"Give me month day and year from this data - {date.today()}")
    # print(resopnse)
    print((date.today()))