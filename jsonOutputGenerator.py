import requests
import json
from docParser import extract_content_from_pdf

def generateOutput(pdf_link, apply_link):
    raw_text = extract_content_from_pdf(pdf_link)
    
    print("raw text extracted")
    
    basic_structure = """{
    name:name of event
    date_of_notification:the date when the notification come
    date_of_commencement:date of starting the application
    end_date:ending of the exam date
    apply_link:application link for the exam
    event_type:{Exam,Result,AdmitCard}
    document_links:related documents given
    details:other details regarding it as per below json format
    }"""

    reference_structure = """
    {
        "name": "",
        "date_of_notification": "",
        "date_of_commencement": "",
        "end_date": "",
        "apply_link": "",
        "event_type":"Exam",
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
    
    user_prompt = f"""
    
        From the raw data provided,
        Extract appropriate information regarding the exam, events or notices or any admit card or result and store it in json format.
        Consider only those events which are currently active or upcoming.
        
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
        If a particular key's data is not available, omit it entirely from the JSON.
        
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
        
        Give me the JSON Object as response, not the code to generate it.
        """
        
        # Give me only json as per the reference format only. The keys of the generated json should be same as basic structure format of json. If that particular data is present in raw text then include it, otherwise don't include anything extra. All the additional details should be displayed as json objects nested under the details object. Only specified keys should be created at parent level as per basic structure. Event type should be either "Exam", "AdmitCard" or "Result" only. Also add "{pdf_link}" as simple string in document links array and "{apply_link}" as simple string to apply_link. In details section, don't include null object. Additionally you can also add additional objects in details which are there in raw text but not mentioned in reference. All the content of json should come from raw text. Reference is just for referring the structure, don't include that data in final response. Return only the generated json, no additional text.
    
    
    # call_ollama_api(user_prompt)
    return call_ollama_api(user_prompt)

def call_ollama_api(prompt, output_file="output.json"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:3b",  # Replace with your model name
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
        start_index = response.find("{")
        end_index = response.rfind("}") + 1

        # Extract the JSON portion of the string
        jsonResponse = response[start_index:end_index]
        
        with open("output.txt", 'w', encoding='utf-8') as file:
            file.write(jsonResponse)
            
        with open("output.json", 'w', encoding='utf-8') as file:
            json.dump(json.loads(jsonResponse), file, indent=4)


        print(f"Generated response saved to {output_file}")
        
        return json.loads(jsonResponse)
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"API call or JSON parsing failed: {e}")


if __name__ == "__main__":
    
    
    with open('raw_text.txt','r', encoding='utf-8') as f:
        raw_text = f.read()
    
    basic_structure = """{
    name:name of event
    date_of_notification:the date when the notification come
    date_of_commencement:date of starting the application
    end_date:ending of the exam date
    apply_link:application link for the exam
    event_type:{Exam,Result,AdmitCard}
    document_links:related documents given
    details:other details regarding it as per below json format
    }"""

    reference_structure = """
    {
        "name": "National Defence Academy & Naval Academy Examination (II), 2025",
        "date_of_notification": "28-05-2025",
        "date_of_commencement": "14-09-2025",
        "end_date": "17-06-2025",
        "apply_link": "https://upsconline.gov.in",
        "event_type":"Exam",
        "document_links": [],
        "details": {
        "vacancies": {
            "total": 400,
            "breakdown": {
            "army": 208,
            "navy": 42,
            "air_force": {
                "flying": 92,
                "ground_duties_technical": 18,
                "ground_duties_non_technical": 10
            },
            "naval_academy": 36
            }
        },
        "eligibility": {
            "age_limit": "Born between 02-01-2007 and 01-01-2010",
            "education": {
            "army": "12th Class pass",
            "navy_air_force": "12th Class pass with Physics, Chemistry, and Mathematics"
            },
            "nationality": [
            "Indian citizen",
            "Subject of Nepal",
            "Person of Indian origin migrated from specified countries"
            ]
        },
        "fee": {
            "amount": "₹100",
            "exemptions": ["SC/ST candidates", "Female candidates", "Wards of JCOs/NCOs/ORs"]
        },
        "exam_centers": ["Agartala", "Ghaziabad", "Navi Mumbai", "..."],
        "important_dates": {
            "application_correction_window": "18-06-2025 to 24-06-2025",
            "results": "October 2025",
            "ssb_interviews": "November 2025 to January 2026"
        },
        "scheme_of_exam": {
            "subjects": {
            "mathematics": {
                "duration": "2.5 hours",
                "marks": 300
            },
            "general_ability_test": {
                "duration": "2.5 hours",
                "marks": 600
            }
            },
            "ssb_test": {
            "marks": 900
            }
        },
        "contact_details": {
            "facilitation_counter": "011-23385271, 011-23381125, 011-23098543",
            "address": "UPSC Office, Gate C, New Delhi"
        }
        }
    }
    """
    
    user_prompt = f"""
    
        From the raw data provided,
        Extract appropriate information regarding the exam, events or notices or any admit card or result and store it in json format.
        Consider only those events which are currently active or upcoming.
        reference json format:
        {basic_structure}
        
        here is the example of response. Imitate this response:
        {reference_structure}

        here is the raw data: 
        {raw_text}
        
        Give me only json as per the reference format only. The keys of the generated json should be same as given reference json. If that particular data is present in raw text then include it, otherwise don't include anything extra.
        """
        # here is the refernce JSON Format:
        # [
        # {reference_structure}   
        # ]  
    
    
    # call_ollama_api(user_prompt)
    call_ollama_api(user_prompt)
