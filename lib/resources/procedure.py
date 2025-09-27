"""
Generates FHIR Procedure resources for testing purposes.
"""
import uuid
import random
from faker import Faker

from typing import Dict, Any

from lib.data.procedures import PROCEDURES, PROCEDURE_STATUSES, PROCEDURE_CATEGORIES


# Initialize Faker to generate random data
fake = Faker()


def generate_procedure(patient_id: str, practitioner_id: str) -> Dict[str, Any]:
    """
    Generates a single FHIR Procedure resource.

    :param patient_id: The ID of the patient for the procedure.
    :param practitioner_id: The ID of the practitioner who performed the procedure.
    :return: A dictionary representing the FHIR Procedure resource.
    """
    procedure_id = str(uuid.uuid4())
    procedure = random.choice(PROCEDURES)
    status = random.choice(PROCEDURE_STATUSES)
    category = random.choice(PROCEDURE_CATEGORIES)

    # Generate a random performed date within the last year
    performed_date = fake.date_time_between(start_date='-1y', end_date='now')

    return {
        "resourceType": "Procedure",
        "id": procedure_id,
        "status": status,
        "category": category,
        "code": {
            "coding": [
                {
                    "system": procedure["system"],
                    "code": procedure["code"],
                    "display": procedure["display"]
                }
            ],
            "text": procedure["text"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "performer": [
            {
                "actor": {
                    "reference": f"Practitioner/{practitioner_id}"
                }
            }
        ],
        "performedDateTime": performed_date.isoformat()
    }
