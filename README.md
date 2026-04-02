# Clinical Decision Support System (FHIR + CDS Hooks)

Full stack clinical decision support system built with FHIR data, CDS Hooks, and interactive dashboards

## Overview
This project is a full-stack healthcare application that processes FHIR patient data and provides clinical decision support using CDS Hooks. This system is designed to analyze patient information and generates alerts for age-based preventive screening.

## Features
- CDS Hooks service triggering alerts for patients over age 45
- FHIR data ingestion from NDJSON datasets (Patient, Condition, Observation, MedicationRequest)
- Interactive Streamlit dashboard for patient insights
- MongoDB database for storing and querying structured clinical data
- Synthetic data generation for age-based screening assessments

## Architecture
- **Backend** Flask (CDS Hooks service)
- **Frontend** Streamlit dashboard
- **Database** MongoDB
- **Data Format:** FHIR NDJSON

## How it works
1) FHIR NDJSON data is ingested and stored in MongoDB
2) CDS Hooks service evaluates patient data (applies to patients age 45 and older)
3) Once triggered, the service returns a clinical recommendation
4) The Streamlit app visualizes patient conditions, medications, and screening data

## Screenshots
Examples of system interface and clinical data visualizations

### Patient Dashboard (Eligible for Screening)
![Dashboard](screenshots/dashboard_main.png)

### Clinical Conditions with ICD-10 Mapping
![Conditions](screenshots/clinical_conditions.png)

### Clinician Notes Interface
![Notes](screenshots/clinician_notes.png)

### Age Access Restriction
![Restriction](screenshots/age_restriction.png)

## Setup Instructions
1) Clone the repository
2) Install dependencies (Poetry):
    poetry install
3) Ensure MongoDB is running locally
4) Load FHIR NDJSON data into MongoDB
5) Run the CDS service:
    python cds_service.py
6) Launch the Streamlit app:
    streamlit run app.py

## Notes
- The full FHIR NDJSON datasets are not included due to the file size
- The system was tested using synthetic and de-identified patient data

## Future Improvements
- Expand CDS logic beyond age-based screening
- Add authetication and user roles
- Improve UI of dashboards
- Deploy as a cloud-based application

## Author
Connor McGrath