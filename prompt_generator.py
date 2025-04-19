import json
import logging
from openai import OpenAI

class DischargeSummaryGenerator:
    def __init__(self, credentials_path='credentials.json', log_file='log.txt'):
        # Load credentials
        with open(credentials_path, 'r') as file:
            credentials = json.load(file)
        self.api_key = credentials['openai_api_key']
        self.base_url = credentials['base_url']

        # Set up logging
        logging.basicConfig(
            filename=log_file,
            filemode='w',
            level=logging.INFO,
            format='%(message)s'
        )

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def clean_data(self, data: dict) -> dict:
        """Cleans EHR data by removing sensitive information."""
        data.pop('patient_id', None)
        if 'patient_demographics' in data:
            data['patient_demographics'].pop('name', None)
        if 'notes' in data:
            for note in data['notes']:
                note.pop('author', None)

        return data

    def generate_letter(self, data: dict,additional_info: str) -> str:
        """Generates a discharge summary letter using the provided prompts and EHR data."""
        cleaned_data = self.clean_data(data)
        system_prompt = "You are a resident physician tasked with writing a discharge summary letter of a patient from the patient's Electronic Health Records."
        user_prompt = f"""\
The letter is written to a patient when leaving hospital after a stay for the review. It should be prose and not contain bullet points.
Include summary of stay including, if applicable, key issues, interventions, procedures, and treatments.
Include summary of condition at discharge.
Include recommendations for follow-up plans and ongoing treatment.
Write the text in the style of a discharge letter using medical terminology. Proceed chronologically, write factually, objectively and concretely, formally, professionally, politely, respectfully. Avoid generalizations, assumptions, verbose and cumbersome formulations, and redundancy. Do not invent or presume anything. Generally, formulate in the imperfect tense, reported speech from individuals (e.g., from patients) in subjunctive I, and medical assessments and diagnoses in the present tense.
Minimize hallucinations. Do not generate recommendations on your own or add anything. Write nothing about topics for which there is no information basis from the EHR.
Don't include all private information, such as ID and date of birth. Use ___ to represent names of patients and medical professionals.
{additional_info}
Now, write a discharge summary letter only using the patient's EHR data provided in the following context:
{json.dumps(cleaned_data)}"""

        # Call OpenAI API
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        response = completion.choices[0].message.content

        # Log the interaction
        logging.info(f'<system>\n{data}\n</system>')
        logging.info(f'<user>\n{user_prompt}\n</user>')
        logging.info(f'<assistant>:\n{response}\n</assistant>')

        return response