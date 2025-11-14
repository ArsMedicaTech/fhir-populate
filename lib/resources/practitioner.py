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
    phone_number = fake.phone_number()

    practitioner = {
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
            {"system": "phone", "value": phone_number, "use": "work"}
        ]
    }
    
    # Add text narrative (best practice)
    practitioner["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Practitioner</b><a name="{practitioner_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Practitioner &quot;{practitioner_id}&quot; </p>
            </div>
            <p><b>name</b>: Dr. {first_name} {last_name}</p>
            <p><b>qualification</b>: {specialty['display']}</p>
            <p><b>telecom</b>: {phone_number} (work)</p>
        </div>"""
    }
    
    return practitioner
