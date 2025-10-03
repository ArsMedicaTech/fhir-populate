"""
Module to generate FHIR Appointment resources with realistic data.

This module supports both FHIR R4 and R5 versions. The version is determined by the
FHIR_VERSION environment variable:
- Set FHIR_VERSION=R4 for FHIR R4 (default)
- Set FHIR_VERSION=R5 for FHIR R5

The main difference is in the reason field structure:
- FHIR R4: Uses 'reasonCode' with CodeableConcept
- FHIR R5: Uses 'reason' with CodeableReference
"""
import uuid
import random
import os
from datetime import datetime, timedelta
from faker import Faker

from typing import Dict, Any

from lib.data.encounter_reasons import ENCOUNTER_REASON_CODES


# Initialize Faker to generate random data
fake = Faker()


def get_fhir_version() -> str:
    """
    Get the FHIR version from environment variable or default to R4.
    
    :return: FHIR version string ('R4' or 'R5')
    """
    fhir_version = os.getenv('FHIR_VERSION', 'R4').upper()
    if fhir_version not in ['R4', 'R5']:
        print(f"Warning: Invalid FHIR_VERSION '{fhir_version}', defaulting to R4")
        fhir_version = 'R4'
    return fhir_version


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

    # Select a random encounter reason
    reason_code = random.choice(ENCOUNTER_REASON_CODES)
    
    # Get FHIR version to determine reason field structure
    fhir_version = get_fhir_version()
    
    # Create base appointment structure
    appointment = {
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
    
    # Add reason field based on FHIR version
    if fhir_version == "R4":
        # FHIR R4 uses reasonCode with CodeableConcept
        appointment["reasonCode"] = [
            {
                "coding": [
                    {
                        "system": reason_code["system"],
                        "code": reason_code["code"],
                        "display": reason_code["display"]
                    }
                ],
                "text": reason_code["display"]
            }
        ]
    else:  # FHIR R5
        # FHIR R5 uses reason with CodeableReference
        appointment["reason"] = [
            {
                "concept": {
                    "coding": [
                        {
                            "system": reason_code["system"],
                            "code": reason_code["code"],
                            "display": reason_code["display"]
                        }
                    ],
                    "text": reason_code["display"]
                }
            }
        ]
    
    return appointment
