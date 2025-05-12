import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load environment variables for secure API key management
load_dotenv(find_dotenv())

# Initialize OpenAI client with the API key from environment variables
client = OpenAI(api_key=os.environ.get('open_api_key'))

# Set default parameters for OpenAI API requests
temperature = 0.3
max_tokens = 500

class ApiInteraction:
    """
    A helper class to interface with the OpenAI API for generating and updating medical diagnosis letters.
    """

    def __init__(self):
        """
        Initializes the API interaction class and verifies the presence of the API key.
        """
        self.api_key = os.environ.get('open_api_key')
        if not self.api_key:
            raise ValueError("API key is missing from environment variables.")

        # Assign the API key to the OpenAI client
        client.api_key = self.api_key

    def generate_diagnosis_letter(report_content):
        """
        Creates a detailed diagnosis letter from a given medical report using GPT API.
        
        Args:
            report_content (str): Text content of the patient's medical report.
        
        Returns:
            str: The generated diagnosis letter.
        """
        prompt = f"""
        You are a professional medical assistant. Based on the following patient's medical report, extract key details and produce a comprehensive diagnosis letter formatted as follows:

        Extract the following:
        1. **Patient Name** and relevant info from the Patient Information section.
        2. **Date of Appointment**
        3. **Physician’s Name**
        4. **Hospital Name**
        5. **Contact Details** (hospital/doctor)
        6. **Blood Test Results**
        7. **ECG Report Findings**
        8. **Thyroid Ultrasound Report Insights**
        9. **Additional Tests and Findings**
        10. **Doctor’s Diagnosis & Treatment Recommendations**
        11. **Follow-Up Actions and Appointments**
        12. **Report Date**

        Using this info, fill in the template below:

        **Patient Diagnosis Letter Template**:

        Dear Patient,

        Thank you for your last visit. Based on your medical report, here are the findings:

        **Findings:**
        - **Symptoms/Observations**: [Key symptoms/observations]
        - **Test Results**:
            - Blood Test Results: [Summary]
            - ECG Report: [Summary]
            - Thyroid Ultrasound: [Summary]
            - Additional Tests: [Summary]
        
        **Diagnosis:**
        [Diagnosis details]

        **Treatment Plan:**
        [Medications/Therapies]

        **Follow-Up:**
        [Follow-up instructions or schedules]

        Please contact our office if you have any questions or concerns.

        Medical Report:
        {report_content}
        """

        # Call GPT API for completion
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return completion.choices[0].message.content

    def generate_updated_letter(previous_letter, new_report):
        """
        Produces an updated diagnosis letter integrating new medical data with prior diagnosis.

        Args:
            previous_letter (str): The previously generated diagnosis letter.
            new_report (str): The latest medical report for updating diagnosis.
        
        Returns:
            str: The revised diagnosis letter.
        """
        prompt = f"""
        You are a professional medical assistant. Given the previous diagnosis letter and a new medical report, update the diagnosis letter accordingly.
        Use this template:

        Dear [Patient Name],

        Based on your previous diagnosis and the recent medical report, here is your updated diagnosis:

        **Previous Diagnosis Summary:**
        {previous_letter}

        **New Findings from the Recent Medical Report:**
        {new_report}

        **Updated Diagnosis and Recommendations:**
        [Updated diagnosis and treatment plan]

        Please contact our office if you have any further questions or concerns.

        Sincerely,
        [Doctor’s Name]
        [Hospital Name]
        [Contact Information]
        """

        # Call GPT API for the updated letter
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return completion.choices[0].message.content
