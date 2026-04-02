from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB
def get_patient_by_id(patient_id):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ehr_db"]
    patient = db["Patient"].find_one({"id": patient_id})
    client.close()
    return patient

# Register CDS services
@app.route("/cds-services", methods=["GET"])
def service_discovery():
    return jsonify({
        "services": [
            {
                "hook": "patient-view",
                "id": "age-risk-check",
                "title": "Age-Based Risk Screening Check",
                "description": "Recommends follow-up screening for patients older than 45.",
                "prefetch": {}
            }
        ]
    })

# CDS Hook logic
@app.route("/cds-services/age-risk-check", methods=["POST"])
def age_risk_check():
    data = request.get_json()
    patient_id = data.get("context", {}).get("patientId")
    patient = get_patient_by_id(patient_id)

    if not patient:
        return jsonify({"cards": []})

    birth_date = patient.get("birthDate")
    try:
        birth = datetime.strptime(birth_date, "%Y-%m-%d")
        age = datetime.now().year - birth.year - ((datetime.now().month, datetime.now().day) < (birth.month, birth.day))
    except:
        age = None

    if age and age > 45:
        card = {
            "summary": "Age-Based Screening Recommended",
            "detail": f"Patient is {age} years old. Recommend scheduling a follow-up screening.",
            "indicator": "info",
            "source": {
                "label": "Age Risk CDS Service",
                "url": "http://localhost:5005"
            },
            "links": [
                {
                    "label": "View Patient Dashboard",
                    "url": f"http://localhost:8502/?patient_id={patient_id}",
                    "type": "smart"
                }
            ]
        }
        return jsonify({"cards": [card]})

    return jsonify({"cards": []})

if __name__ == "__main__":
    app.run(host="localhost", port=5005, debug=True)
