"""
FHIR resource generation functions.
"""
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker

from typing import Dict, Any, Tuple

from lib.data.specialties import PRACTITIONER_SPECIALTIES
from lib.data.icd import CONDITIONS_ICD10

# Initialize Faker to generate random data
fake = Faker()


# --- FHIR Resource Generation Functions ---

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


def generate_condition(patient_id: str) -> Dict[str, Any]:
    """
    Generates a single FHIR Condition resource for a given patient.

    :param patient_id: The ID of the patient to whom the condition belongs.
    :return: A dictionary representing the FHIR Condition resource.
    """
    condition_id = str(uuid.uuid4())
    condition_info = random.choice(CONDITIONS_ICD10)

    return {
        "resourceType": "Condition",
        "id": condition_id,
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active"
            }]
        },
        "verificationStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed"
            }]
        },
        "code": {
            "coding": [{
                "system": "http://hl7.org/fhir/sid/icd-10",
                "code": condition_info["code"],
                "display": condition_info["display"]
            }],
            "text": condition_info["display"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "onsetDateTime": fake.date_time_this_decade(before_now=True, after_now=False).isoformat()
    }


def generate_appointment(patient_id: str, practitioner_id: str, location_id: str) -> Dict[str, Any]:
    """
    Generates a single FHIR Appointment resource.

    :param patient_id: The ID of the patient for the appointment.
    :param practitioner_id: The ID of the practitioner for the appointment.
    :param location_id: The ID of the location for the appointment.
    :return: A dictionary representing the FHIR Appointment resource.
    """
    appointment_id = str(uuid.uuid4())
    start_time = fake.date_time_this_month(before_now=False, after_now=True)
    end_time = start_time + timedelta(minutes=random.choice([15, 30, 45]))

    return {
        "resourceType": "Appointment",
        "id": appointment_id,
        "status": random.choice(["booked", "fulfilled", "cancelled"]),
        "description": f"Follow-up visit for {fake.word()}",
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "created": datetime.now().isoformat(),
        "participant": [
            {
                "actor": {"reference": f"Patient/{patient_id}"},
                "status": "accepted"
            },
            {
                "actor": {"reference": f"Practitioner/{practitioner_id}"},
                "status": "accepted"
            },
            {
                "actor": {"reference": f"Location/{location_id}"},
                "status": "accepted"
            }
        ]
    }
