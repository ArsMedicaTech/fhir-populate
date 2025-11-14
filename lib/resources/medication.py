"""
Module to generate FHIR MedicationRequest resources with realistic data.
"""
import uuid
import random
from datetime import timezone
from faker import Faker

from typing import Dict, Any

from lib.data.medications import MEDICATIONS, MEDICATION_STATUSES, MEDICATION_INTENTS


# Initialize Faker to generate random data
fake = Faker()


def generate_medication_request(patient_id: str, practitioner_id: str) -> Dict[str, Any]:
    """
    Generates a single FHIR MedicationRequest resource.

    :param patient_id: The ID of the patient for the medication request.
    :param practitioner_id: The ID of the practitioner who prescribed the medication.
    :return: A dictionary representing the FHIR MedicationRequest resource.
    """
    medication_request_id = str(uuid.uuid4())
    medication = random.choice(MEDICATIONS)
    status = random.choice(MEDICATION_STATUSES)
    intent = random.choice(MEDICATION_INTENTS)

    # Generate a random authored date within the last year
    authored_date = fake.date_time_between(start_date='-1y', end_date='now')
    # Ensure timezone is included in datetime strings (FHIR requirement)
    if authored_date.tzinfo is None:
        authored_date = authored_date.replace(tzinfo=timezone.utc)

    medication_request = {
        "resourceType": "MedicationRequest",
        "id": medication_request_id,
        "status": status,
        "intent": intent,
        "medicationCodeableConcept": {
            "text": medication["name"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "requester": {
            "reference": f"Practitioner/{practitioner_id}"
        },
        "authoredOn": authored_date.isoformat(),
        "dosageInstruction": [
            {
                "timing": {
                    "code": {
                        "text": medication["timing"]
                    }
                },
                "route": {
                    "text": medication["route"]
                },
                "doseAndRate": [
                    {
                        "doseQuantity": {
                            "value": medication["dosage"]["value"],
                            "unit": medication["dosage"]["unit"]
                        }
                    }
                ]
            }
        ]
    }
    
    # Add text narrative (best practice)
    medication_request["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: MedicationRequest</b><a name="{medication_request_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource MedicationRequest &quot;{medication_request_id}&quot; </p>
            </div>
            <p><b>status</b>: {status}</p>
            <p><b>intent</b>: {intent}</p>
            <p><b>medication</b>: {medication['name']}</p>
            <p><b>subject</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>requester</b>: <a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a></p>
            <p><b>authoredOn</b>: {authored_date.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
            <p><b>dosage</b>: {medication['dosage']['value']} {medication['dosage']['unit']} {medication['timing']} via {medication['route']}</p>
        </div>"""
    }
    
    return medication_request
