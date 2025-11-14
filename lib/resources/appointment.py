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
from datetime import datetime, timedelta, timezone
from faker import Faker

from typing import Dict, Any

from common import get_fhir_version
from lib.data.encounter_reasons import ENCOUNTER_REASON_CODES


# Initialize Faker to generate random data
fake = Faker()


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
    # Ensure timezone is included (start/end are instants, require timezone)
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    
    end_time = start_time + timedelta(minutes=random.choice([15, 30, 45]))
    # Ensure timezone is included
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=timezone.utc)
    
    created_time = datetime.now(timezone.utc)

    # Select a random encounter reason
    reason_code = random.choice(ENCOUNTER_REASON_CODES)
    
    # Get FHIR version to determine reason field structure
    fhir_version = get_fhir_version()
    
    status = random.choice(["booked", "fulfilled", "cancelled"])
    description = f"Follow-up visit for {fake.word()}"
    
    # Create base appointment structure
    appointment = {
        "resourceType": "Appointment",
        "id": appointment_id,
        "status": status,
        "description": description,
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "created": created_time.isoformat(),
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
    
    # Add text narrative (best practice)
    appointment["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Appointment</b><a name="{appointment_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Appointment &quot;{appointment_id}&quot; </p>
            </div>
            <p><b>status</b>: {status}</p>
            <p><b>description</b>: {description}</p>
            <p><b>start</b>: {start_time.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
            <p><b>end</b>: {end_time.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
            <p><b>created</b>: {created_time.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
            <p><b>participant</b>: Patient/{patient_id}, Practitioner/{practitioner_id}, Location/{location_id}</p>
            <p><b>reason</b>: {reason_code['display']}</p>
        </div>"""
    }
    
    return appointment
