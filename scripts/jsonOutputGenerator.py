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