"""
Generates FHIR Observation resources with realistic data.
"""
import uuid
import random
from datetime import timedelta
from faker import Faker

from typing import Dict, Any

from lib.data.observations import OBSERVATIONS, OBSERVATION_STATUSES, OBSERVATION_CATEGORIES, INTERPRETATION_CODES


# Initialize Faker to generate random data
fake = Faker()


def generate_observation(patient_id: str, practitioner_id: str) -> Dict[str, Any]:
    """
    Generates a single FHIR Observation resource.

    :param patient_id: The ID of the patient for the observation.
    :param practitioner_id: The ID of the practitioner who performed the observation.
    :return: A dictionary representing the FHIR Observation resource.
    """
    observation_id = str(uuid.uuid4())
    observation = random.choice(OBSERVATIONS)
    status = random.choice(OBSERVATION_STATUSES)
    category = random.choice(OBSERVATION_CATEGORIES)

    # Generate a random effective date within the last year
    effective_date = fake.date_time_between(start_date='-1y', end_date='now')
    issued_date = effective_date + timedelta(minutes=random.randint(30, 120))

    # Generate a realistic value based on normal ranges and interpretations
    interpretation = random.choice(list(observation["interpretations"].keys()))
    value_range = observation["interpretations"][interpretation]

    # Generate a value within the interpretation range
    if value_range["low"] == value_range["high"]:
        value = value_range["low"]
    else:
        value = round(random.uniform(value_range["low"], value_range["high"]), 2)

    # Create the observation resource
    obs_resource = {
        "resourceType": "Observation",
        "id": observation_id,
        "status": status,
        "category": [category],
        "code": {
            "coding": [
                {
                    "system": observation["system"],
                    "code": observation["code"],
                    "display": observation["display"]
                }
            ],
            "text": observation["text"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "effectiveDateTime": effective_date.isoformat(),
        "issued": issued_date.isoformat(),
        "valueQuantity": {
            "value": value,
            "unit": observation["unit"],
            "system": observation["unit_system"],
            "code": observation["unit_code"]
        },
        "interpretation": [
            {
                "coding": [
                    {
                        "system": INTERPRETATION_CODES[interpretation]["system"],
                        "code": INTERPRETATION_CODES[interpretation]["code"],
                        "display": INTERPRETATION_CODES[interpretation]["display"]
                    }
                ]
            }
        ]
    }

    # Add performer if status is not cancelled or entered-in-error
    if status not in ["cancelled", "entered-in-error"]:
        obs_resource["performer"] = [
            {
                "reference": f"Practitioner/{practitioner_id}"
            }
        ]

    return obs_resource
