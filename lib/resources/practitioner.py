"""
Module to generate FHIR Practitioner resources with random data.
"""
import uuid
import random
from faker import Faker

from typing import Dict, Any

from lib.data.specialties import PRACTITIONER_SPECIALTIES


# Initialize Faker to generate random data
fake = Faker()


def generate_practitioner() -> Dict[str, Any]:
    """
    Generates a single FHIR Practitioner resource.

    :return: A dictionary representing the FHIR Practitioner resource.
    """
    practitioner_id = str(uuid.uuid4())
    first_name = fake.first_name()
    last_name = fake.last_name()
    specialty = random.choice(PRACTITIONER_SPECIALTIES)

    return {
        "resourceType": "Practitioner",
        "id": practitioner_id,
        "name": [{
            "use": "official",
            "family": last_name,
            "given": [first_name],
            "prefix": ["Dr."]
        }],
        "qualification": [{
            "code": {
                "coding": [{
                    "system": "http://snomed.info/sct",
                    "code": specialty["code"],
                    "display": specialty["display"]
                }],
                "text": specialty["display"]
            }
        }],
        "telecom": [
            {"system": "phone", "value": fake.phone_number(), "use": "work"}
        ]
    }
