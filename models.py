import sqlite3
from datetime import datetime

class Patient:
    def __init__(self, patient_id, name, age, gender, medical_report_path=None, diagnosis_letter_path=None):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.medical_report_path = medical_report_path
        self.diagnosis_letter_path = diagnosis_letter_path

    def save_to_db(self):
        """Save or update the patient in the database, including medical report and diagnosis letter paths."""
        conn = sqlite3.connect('patients.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO patients (patient_id, name, age, gender, medical_report_path, diagnosis_letter_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.patient_id, self.name, self.age, self.gender, self.medical_report_path, self.diagnosis_letter_path))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_name(name):
        """Retrieve a patient from the database by name."""
        conn = sqlite3.connect('patients.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT patient_id, name, age, gender, medical_report_path, diagnosis_letter_path
            FROM patients WHERE name = ?
        ''', (name,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return Patient(*result)
        return None

    @staticmethod
    def get_by_id(patient_id):
        """Retrieve a patient from the database by patient_id."""
        conn = sqlite3.connect('patients.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT patient_id, name, age, gender, medical_report_path, diagnosis_letter_path
            FROM patients WHERE patient_id = ?
        ''', (patient_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return Patient(*result)
        return None

    def update_medical_report_path(self, report_path):
        """Update the medical report file path."""
        self.medical_report_path = report_path
        self.save_to_db()

    def update_diagnosis_letter_path(self, letter_path):
        """Update the diagnosis letter file path."""
        self.diagnosis_letter_path = letter_path
        self.save_to_db()

    def read_diagnosis_letter_content(self):
        """Read the content of the diagnosis letter file."""
        if self.diagnosis_letter_path:
            try:
                with open(self.diagnosis_letter_path, 'rb') as file:
                    content = file.read()
                return content
            except Exception as e:
                return f"Error reading diagnosis letter: {e}"
        return "No diagnosis letter available."

