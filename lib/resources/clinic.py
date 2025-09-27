"""
This module generates FHIR Organization and Location resources representing a clinic.
"""
import uuid
import random
from faker import Faker

from typing import Dict, Any, Tuple


# Initialize Faker to generate random data
fake = Faker()


def generate_clinic_and_location() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Generates a FHIR Organization (as a Clinic) and a corresponding Location resource.

    :return: A tuple containing two dictionaries: the FHIR Organization and Location resources.
    """
    clinic_id = str(uuid.uuid4())
    location_id = str(uuid.uuid4())
    clinic_name = f"{fake.city()} {random.choice(['Community', 'General', 'Wellness'])} Clinic"

    address = {
        "line": [fake.street_address()],
        "city": fake.city(),
        "state": fake.state_abbr(),
        "postalCode": fake.zipcode(),
        "country": "US"
    }

    clinic = {
        "resourceType": "Organization",
        "id": clinic_id,
        "name": clinic_name,
        "type": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                "code": "prov",
                "display": "Healthcare Provider"
            }]
        }],
        "telecom": [{"system": "phone", "value": fake.phone_number()}],
        "address": [address]
    }

    location = {
        "resourceType": "Location",
        "id": location_id,
        "name": clinic_name,
        "address": address,
        "physicalType": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
                "code": "si",
                "display": "Site"
            }]
        },
        "managingOrganization": {
            "reference": f"Organization/{clinic_id}"
        }
    }
    return clinic, location
