from models import Patient

class PatientManager:
    def register_patient(self, patient_id, name, age, gender, medical_report_path=None, diagnosis_letter_path=None):
        patient = Patient(patient_id, name, age, gender, medical_report_path, diagnosis_letter_path)
        patient.save_to_db()
        return patient

    def get_patient_by_name(self, name):
        return Patient.get_by_name(name)
