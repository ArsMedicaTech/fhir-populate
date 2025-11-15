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

    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
    phone_number = fake.phone_number()
    email = fake.email()
    address_line = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    postal_code = fake.zipcode()
    
    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{
            "use": "official",
            "family": last_name,
            "given": [first_name]
        }],
        "telecom": [
            {"system": "phone", "value": phone_number, "use": "mobile"},
            {"system": "email", "value": email}
        ],
        "gender": gender,
        "birthDate": birth_date.isoformat(),
        "address": [{
            "use": "home",
            "line": [address_line],
            "city": city,
            "state": state,
            "postalCode": postal_code,
            "country": "US"
        }]
    }
    
    # Add text narrative (best practice)
    patient["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Patient</b><a name="{patient_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Patient &quot;{patient_id}&quot; </p>
            </div>
            <p><b>name</b>: {first_name} {last_name}</p>
            <p><b>gender</b>: {gender}</p>
            <p><b>birthDate</b>: {birth_date.strftime('%Y-%m-%d')}</p>
            <p><b>telecom</b>: {phone_number} (mobile), {email} (email)</p>
            <p><b>address</b>: {address_line}, {city}, {state} {postal_code}</p>
        </div>"""
    }
    
    return patient


def generate_patient_custom(first_name: str = None, last_name: str = None, 
                            gender: str = None, birth_date: str = None) -> Dict[str, Any]:
    """
    Generates a single FHIR Patient resource with custom attributes.
    If attributes are not provided, random values are used.

    :param first_name: Optional first name for the patient.
    :param last_name: Optional last name for the patient.
    :param gender: Optional gender (male, female, other, unknown).
    :param birth_date: Optional birth date in ISO format (YYYY-MM-DD).
    :return: A dictionary representing the FHIR Patient resource.
    """
    patient_id = str(uuid.uuid4())
    first_name = first_name or fake.first_name()
    last_name = last_name or fake.last_name()
    gender = gender or random.choice(["male", "female", "other", "unknown"])

    if birth_date:
        from datetime import datetime
        try:
            # Parse the date string and create a date object
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
        except:
            birth_date_obj = fake.date_of_birth(minimum_age=18, maximum_age=90)
    else:
        birth_date_obj = fake.date_of_birth(minimum_age=18, maximum_age=90)
    
    phone_number = fake.phone_number()
    email = fake.email()
    address_line = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    postal_code = fake.zipcode()
    
    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{
            "use": "official",
            "family": last_name,
            "given": [first_name]
        }],
        "telecom": [
            {"system": "phone", "value": phone_number, "use": "mobile"},
            {"system": "email", "value": email}
        ],
        "gender": gender,
        "birthDate": birth_date_obj.isoformat(),
        "address": [{
            "use": "home",
            "line": [address_line],
            "city": city,
            "state": state,
            "postalCode": postal_code,
            "country": "US"
        }]
    }
    
    # Add text narrative (best practice)
    patient["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Patient</b><a name="{patient_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Patient &quot;{patient_id}&quot; </p>
            </div>
            <p><b>name</b>: {first_name} {last_name}</p>
            <p><b>gender</b>: {gender}</p>
            <p><b>birthDate</b>: {birth_date_obj.strftime('%Y-%m-%d')}</p>
            <p><b>telecom</b>: {phone_number} (mobile), {email} (email)</p>
            <p><b>address</b>: {address_line}, {city}, {state} {postal_code}</p>
        </div>"""
    }
    
    return patient