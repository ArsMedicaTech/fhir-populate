"""
Generates FHIR Condition resources for patients.
"""
import uuid
import random
from datetime import timezone
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
    
    # Generate onset date with timezone
    onset_date = fake.date_time_this_decade(before_now=True, after_now=False)
    # Ensure timezone is included in datetime strings (FHIR requirement)
    if onset_date.tzinfo is None:
        onset_date = onset_date.replace(tzinfo=timezone.utc)

    condition = {
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
        "onsetDateTime": onset_date.isoformat()
    }
    
    # Add text narrative (best practice)
    condition["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Condition</b><a name="{condition_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Condition &quot;{condition_id}&quot; </p>
            </div>
            <p><b>clinicalStatus</b>: active</p>
            <p><b>verificationStatus</b>: confirmed</p>
            <p><b>code</b>: {condition_info['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (ICD-10#{condition_info['code']})</span></p>
            <p><b>subject</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>onset</b>: {onset_date.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
        </div>"""
    }
    
    return condition
