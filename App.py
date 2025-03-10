
import streamlit as st
from patient_manager import PatientManager
from file_manager import FileManager
from api_handler import ApiInteraction

st.title("Patient Diagnosis Management System")
manager = PatientManager()

patient = None
new_report_path = None

menu = st.sidebar.radio("Navigation", ["Add Patient", "View Patient"])

if menu == "Add Patient":
    st.header("Add New Patient")
    
    patient_id = st.text_input("Patient ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    st.header("Add Medical Report")
    uploaded_file = st.file_uploader("Upload Medical Report (PDF, DOCX, TXT)")

    if uploaded_file:
        file_path = FileManager.save_uploaded_file(uploaded_file)
        st.write(f"File saved at: {file_path}")
    
    st.header("Generate Diagnosis Letter")
    if uploaded_file:
        report_content = FileManager.extract_text_from_file(file_path)
        diagnosis_path = f"diagnosis_{patient_id}.txt"
        
        if st.button("Generate Diagnosis Letter"):
            diagnosis_file = ApiInteraction.generate_diagnosis_letter(report_content)
            if diagnosis_file:
                st.write(f"Diagnosis letter generated and saved at: {diagnosis_file}")

                patient = manager.register_patient(
                    patient_id, 
                    name, 
                    age, 
                    gender, 
                    medical_report_path=file_path,  
                    diagnosis_letter_path=diagnosis_file  
                )


elif menu == "View Patient":
    st.header("View Patient Details")

    if 'patient' not in st.session_state:
        st.session_state.patient = None

    search_name = st.text_input("Search by Patient Name")

    if st.button("Search Patient"):
        patient = manager.get_patient_by_name(search_name)
        
        if patient:
            st.session_state.patient = patient
        else:
            st.warning("No patient found with this name.")
            st.session_state.patient = None
    
    patient = st.session_state.patient
    
    if patient:
        st.write(f"**ID:** {patient.patient_id}")
        st.write(f"**Name:** {patient.name}")
        st.write(f"**Age:** {patient.age}")
        st.write(f"**Gender:** {patient.gender}")
        st.write(f"**Medical Report Path:** {patient.medical_report_path}")
        # st.write(f"**Diagnosis Report Path:** {patient.diagnosis_letter_path}")


        latest_diagnosis_path = patient.diagnosis_letter_path

        if latest_diagnosis_path:
            st.subheader("Latest Diagnosis Letter")
            
            try:
                latest_diagnosis_content = latest_diagnosis_path
                
                if latest_diagnosis_content:
                    st.write(latest_diagnosis_content, height=300)
                else:
                    st.warning("The diagnosis letter is empty or could not be read.")
            except Exception as e:
                st.error(f"An error occurred while reading the file: {e}")

        
        uploaded_new_report = st.file_uploader("Upload New Diagnosis Report", type=["pdf", "docx", "txt"], key="new_report_uploader")
        
        if uploaded_new_report and st.button("Update Diagnosis Letter"):
            try:
                new_report_path = FileManager.save_uploaded_file(uploaded_new_report)
                new_report_content = FileManager.extract_text_from_file(new_report_path)
                
                # updated_path = f"updated_diagnosis_{patient.patient_id}.txt"
                updated_file = ApiInteraction.generate_updated_letter(
                    previous_letter=latest_diagnosis_content, 
                    new_report=new_report_content
                )
                
                if updated_file:
                    # with open(updated_path, 'w') as file:
                    # file.write(updated_file)
                    
                    patient.update_diagnosis_letter_path(updated_file)
                    st.success("Diagnosis letter updated successfully!")
                    
                    st.session_state.patient = patient
                    
                    st.subheader("Updated Diagnosis Letter")
                    st.write(updated_file)
                else:
                    st.error("Failed to generate updated diagnosis letter.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.info("Search for a patient to view details.")

