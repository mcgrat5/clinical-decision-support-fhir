from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ehr_db"]
patients = db["Patient"].find()
age_collection = db["age_screening_assessments"]

# Helper to calculate age
def calculate_age(birthdate_str):
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
        today = datetime.today()
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    except:
        return None

# Sample medical context
CHRONIC_CONDITIONS = [
    "Hypertension (SNOMED CT: 38341003)",
    "Type 2 Diabetes Mellitus (SNOMED CT: 44054006)",
    "Hyperlipidemia (SNOMED CT: 55822004)",
    "None"
]

MEDICATIONS = [
    "Lisinopril (RxCUI: 29046)",
    "Metformin (RxCUI: 860975)",
    "Atorvastatin (RxCUI: 83367)",
    "None"
]

# Loop over patients age > 45
for patient in patients:
    birth_date = patient.get("birthDate")
    age = calculate_age(birth_date)

    if age and age > 45:
        patient_id = patient.get("id")
        print(f"🏥 Generating screening data for patient {patient_id}, age {age}")
        base_date = datetime.today()

        # Generate 1–2 screening logs
        for i in range(random.randint(1, 2)):
            assessment = {
                "patient_id": patient_id,
                "encounter_id": f"age-{i+1}",
                "assessor": f"AutoSeeder NP",
                "assessment_date": base_date - timedelta(days=30 * i),
                "age_at_assessment": age,
                "screening_needed": True if random.random() < 0.85 else False,
                "recommended_medication": random.choice(MEDICATIONS),
                "associated_condition": random.choice(CHRONIC_CONDITIONS)
            }
            age_collection.insert_one(assessment)

print("Age-based screenings seeded for patients over 45.")
