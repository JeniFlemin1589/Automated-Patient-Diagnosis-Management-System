import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load environment variables for the API key
load_dotenv(find_dotenv())

# Initialize OpenAI client with the API key - using your key
client = OpenAI(api_key=os.environ.get('open_api_key'))

# Set parameters for OpenAI requests
temperature = 0.3
max_tokens = 500

class ApiInteraction:
    """
    A class to interact with the OpenAI API to generate diagnosis letters
    from medical reports, as well as update letters based on new medical information.
    """

    def __init__(self):
        """
        Initializes the API interaction class and checks if the API key exists in environment variables.
        """
        self.api_key = os.environ.get('open_api_key')
        if not self.api_key:
            raise ValueError("API key is missing from the environment variables")

        # Set the API key for the OpenAI client
        client.api_key = self.api_key

    def generate_diagnosis_letter(report_content):
        """
        Generates a detailed diagnosis letter based on the patient's medical report using GPT API.
        
        Parameters:
            report_content (str): The content of the patient's medical report.
        
        Returns:
            str: The generated diagnosis letter.
        """
        prompt = f"""
        You are a professional medical assistant. Based on the following patient's medical report, extract the necessary details and generate a detailed diagnosis letter in a structured format. 

        Extract the following information from the report:
        
        1. **Patient Name**: Extract the patient's name and any relevant from Patient Information section.
        2. **Date of Appointment**: Extract the date of the appointment.
        3. **Physician’s Name**: Extract the doctor's name from Patient Information section.
        4. **Hospital Name**: Extract the hospital name from the report.
        5. **Contact Information**: Extract any contact information provided for the hospital/doctor.
        6. **Blood Test Results**: Extract relevant blood test results.
        7. **Electrocardiogram (ECG) Report**: Extract relevant information related to the ECG report.
        8. **Thyroid Ultrasound Report**: Extract relevant information related to the thyroid ultrasound report.
        9. **Additional Tests**: Extract any additional test results or findings.
        10. **Doctor’s Recommendations**: Extract details on the diagnosis and treatment recommendations.
        11. **Follow-Up Appointments**: Extract details regarding follow-up appointments or any recommended actions.
        12. **Date of Report**: Extract details from Patient Information.

        Based on this information, fill in the following diagnosis letter template:

        **Patient Diagnosis Letter Template**:

        Dear Patient,

        Thank you for your last visit . Based on your medical report, here are the findings:

        **Findings:**
        - **Symptoms/Observations**: [Extract key symptoms and observations from the report]
        - **Test Results**:
            - Blood Test Results: [Summarize relevant blood test results]
            - Electrocardiogram (ECG) Report: [Summarize ECG results]
            - Thyroid Ultrasound Report: [Summarize thyroid ultrasound results]
            - Additional Tests: [Summarize any additional test results]
        
        **Diagnosis:**
        [Provide the diagnosis based on the doctor’s recommendations and initial findings]

        **Treatment Plan:**
        [Outline the recommended treatment plan, including any medications or therapies]

        **Follow-Up:**
        [Provide details about the follow-up appointment and any instructions for the patient]

        Please contact our office if you have any questions or concerns.

        
        Medical Report:
        {report_content}
        """

        # Generate completion using OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Return the generated letter content
        return completion.choices[0].message.content

    def generate_updated_letter(previous_letter, new_report):
        """
        Generates an updated diagnosis letter based on the previous diagnosis letter and a new medical report.

        Parameters:
            previous_letter (str): The previously generated diagnosis letter.
            new_report (str): The new medical report to update the diagnosis.

        Returns:
            str: The updated diagnosis letter.
        """
        prompt = f"""
        You are a professional medical assistant. Given the previous diagnosis letter and a new medical report, update the diagnosis letter to reflect any changes in the patient's condition.
        Use the following updated letter template:

        Dear [Patient Name],

        Based on your previous diagnosis and the recent medical report, here is your updated diagnosis:

        **Previous Diagnosis Summary:**
        {previous_letter}

        **New Findings from the Recent Medical Report:**
        {new_report}

        **Updated Diagnosis and Recommendations:**
        [Provide the updated diagnosis and treatment recommendations]

        Please contact our office if you have any further questions or concerns.

        Sincerely,
        [Doctor’s Name]
        [Hospital Name]
        [Contact Information]
        """

        # Generate completion using OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Return the updated letter content
        return completion.choices[0].message.content


