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

    phone_number = fake.phone_number()
    
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
        "telecom": [{"system": "phone", "value": phone_number}],
        "address": [address]
    }
    
    # Add text narrative (best practice)
    clinic["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Organization</b><a name="{clinic_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Organization &quot;{clinic_id}&quot; </p>
            </div>
            <p><b>name</b>: {clinic_name}</p>
            <p><b>type</b>: Healthcare Provider</p>
            <p><b>telecom</b>: {phone_number} (phone)</p>
            <p><b>address</b>: {address['line'][0]}, {address['city']}, {address['state']} {address['postalCode']}</p>
        </div>"""
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
    
    # Add text narrative (best practice)
    location["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Location</b><a name="{location_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Location &quot;{location_id}&quot; </p>
            </div>
            <p><b>name</b>: {clinic_name}</p>
            <p><b>address</b>: {address['line'][0]}, {address['city']}, {address['state']} {address['postalCode']}</p>
            <p><b>physicalType</b>: Site</p>
            <p><b>managingOrganization</b>: <a href="organization-{clinic_id}.html">Organization/{clinic_id}</a></p>
        </div>"""
    }
    
    return clinic, location
