"""
Module to generate FHIR MedicationRequest resources with realistic data.
"""
import uuid
import random
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

    return {
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
