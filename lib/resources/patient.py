"""
Module to generate FHIR Patient resources.
"""
import uuid
import random
from faker import Faker

from typing import Dict, Any


# Initialize Faker to generate random data
fake = Faker()


def generate_patient() -> Dict[str, Any]:
    """
    Generates a single FHIR Patient resource.

    :return: A dictionary representing the FHIR Patient resource.
    """
    patient_id = str(uuid.uuid4())
    first_name = fake.first_name()
    last_name = fake.last_name()
    gender = random.choice(["male", "female", "other", "unknown"])

    return {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{
            "use": "official",
            "family": last_name,
            "given": [first_name]
        }],
        "telecom": [
            {"system": "phone", "value": fake.phone_number(), "use": "mobile"},
            {"system": "email", "value": fake.email()}
        ],
        "gender": gender,
        "birthDate": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        "address": [{
            "use": "home",
            "line": [fake.street_address()],
            "city": fake.city(),
            "state": fake.state_abbr(),
            "postalCode": fake.zipcode(),
            "country": "US"
        }]
    }
