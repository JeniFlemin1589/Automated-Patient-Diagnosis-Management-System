
# Patient Diagnosis Management System

## Overview
The **Patient Diagnosis Management System** is a Streamlit-based web application designed to manage patient information, upload medical reports, and generate diagnosis letters. It allows healthcare professionals to add patients, view patient details, and upload medical reports in different formats such as PDF, DOCX, or TXT. It also leverages the power of OpenAI's GPT model to generate and update diagnosis letters based on the medical report content.

## Features
- **Add New Patient**: Allows the user to add new patient information including their ID, name, age, gender, and medical report.
- **View Patient Details**: Enables the user to search and view patient information by name.
- **Generate Diagnosis Letter**: Automatically generates a diagnosis letter based on the medical report using GPT.
- **Update Diagnosis Letter**: Allows the user to upload a new diagnosis report and generate an updated diagnosis letter.

## Technologies Used
- **Streamlit**: For creating the web application interface.
- **OpenAI GPT**: For generating diagnosis letters from medical reports.
- **SQLite**: For managing patient data.
- **PyPDF2**: For extracting text from PDF reports.
- **python-docx**: For extracting text from DOCX reports.
- **dotenv**: For securely loading environment variables (API keys).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/patient-diagnosis-management.git
    cd patient-diagnosis-management
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    - For macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
    - For Windows:
      ```bash
      venv\Scripts\activate
      ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up the `.env` file to store your OpenAI API key:
    - Create a `.env` file in the root directory of the project.
    - Add the following content to the `.env` file:
      ```
      open_api_key=your-openai-api-key-here
      ```

6. Initialize the database:
    ```bash
    python db_setup.py
    ```

## Usage

1. Start the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open the app in your browser (usually accessible at `http://localhost:8501`).

## File Structure
```
patient-diagnosis-management/
│
├── app.py                # Main application code (Streamlit app)
├── api_handler.py        # Contains the logic for interacting with OpenAI API
├── db_setup.py           # Initializes the SQLite database for patient data
├── file_manager.py       # Manages file uploads and text extraction
├── requirements.txt      # List of dependencies for the project
├── .env                  # Environment file containing the OpenAI API key
└── uploads/              # Folder where uploaded medical reports are stored
```

## Classes
### `PatientManager`
- Registers and retrieves patient information from the SQLite database.

### `FileManager`
- Manages file uploads, saves uploaded files, and extracts text from PDF and DOCX files.

### `ApiInteraction`
- Interacts with the OpenAI GPT API to generate and update diagnosis letters based on medical reports.

## Database
The database (`patients.db`) stores patient information including:
- `patient_id`: Unique identifier for each patient.
- `name`: Patient's name.
- `age`: Patient's age.
- `gender`: Patient's gender.
- `medical_report_path`: Path to the uploaded medical report.
- `diagnosis_letter_path`: Path to the generated diagnosis letter.

## Requirements
- Python 3.7 or higher
- Streamlit
- OpenAI API Key
- SQLite3 (used internally in the code)

### Dependencies (requirements.txt)
```text
streamlit>=1.0.0
openai>=0.27.0
python-dotenv>=0.19.0
PyPDF2>=2.0.0
python-docx>=0.8.11
```
