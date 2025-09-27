"""
Generates FHIR Condition resources for patients.
"""
import uuid
import random
from faker import Faker

from typing import Dict, Any

from lib.data.icd import CONDITIONS_ICD10


# Initialize Faker to generate random data
fake = Faker()


def generate_condition(patient_id: str) -> Dict[str, Any]:
    """
    Generates a single FHIR Condition resource for a given patient.

    :param patient_id: The ID of the patient to whom the condition belongs.
    :return: A dictionary representing the FHIR Condition resource.
    """
    condition_id = str(uuid.uuid4())
    condition_info = random.choice(CONDITIONS_ICD10)

    return {
        "resourceType": "Condition",
        "id": condition_id,
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active"
            }]
        },
        "verificationStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed"
            }]
        },
        "code": {
            "coding": [{
                "system": "http://hl7.org/fhir/sid/icd-10",
                "code": condition_info["code"],
                "display": condition_info["display"]
            }],
            "text": condition_info["display"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "onsetDateTime": fake.date_time_this_decade(before_now=True, after_now=False).isoformat()
    }
