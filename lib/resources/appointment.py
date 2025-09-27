"""
Module to generate FHIR Appointment resources with realistic data.
"""
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker

from typing import Dict, Any

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
    end_time = start_time + timedelta(minutes=random.choice([15, 30, 45]))

    # Select a random encounter reason
    reason_code = random.choice(ENCOUNTER_REASON_CODES)

    return {
        "resourceType": "Appointment",
        "id": appointment_id,
        "status": random.choice(["booked", "fulfilled", "cancelled"]),
        "description": f"Follow-up visit for {fake.word()}",
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "created": datetime.now().isoformat(),
        "reason": [
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
        ],
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
