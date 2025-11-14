"""
Generates FHIR Observation resources with realistic data.
"""
import uuid
import random
from datetime import timedelta, timezone
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
    # Ensure timezone is included in datetime strings (FHIR requirement)
    if effective_date.tzinfo is None:
        effective_date = effective_date.replace(tzinfo=timezone.utc)
    
    issued_date = effective_date + timedelta(minutes=random.randint(30, 120))
    # Ensure timezone is included (issued is an instant, requires timezone)
    if issued_date.tzinfo is None:
        issued_date = issued_date.replace(tzinfo=timezone.utc)

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
            "unit": observation["unit"]
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

    # Add performer (best practice - always include if available, except for entered-in-error)
    if practitioner_id and status != "entered-in-error":
        obs_resource["performer"] = [
            {
                "reference": f"Practitioner/{practitioner_id}"
            }
        ]
    
    # Add text narrative (best practice)
    obs_resource["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Observation</b><a name="{observation_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Observation &quot;{observation_id}&quot; </p>
            </div>
            <p><b>status</b>: {status}</p>
            <p><b>category</b>: {category['coding'][0]['display']}</p>
            <p><b>code</b>: {observation['text']} ({observation['system']}#{observation['code']})</p>
            <p><b>subject</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>effective</b>: {effective_date.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
            <p><b>value</b>: {value} {observation['unit']}</p>
            <p><b>interpretation</b>: {INTERPRETATION_CODES[interpretation]['display']}</p>
        </div>"""
    }

    return obs_resource
