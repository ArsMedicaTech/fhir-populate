"""
Generates FHIR Encounter resources with randomized attributes for testing purposes.
Supports both FHIR R4 and R5 versions based on FHIR_VERSION environment variable.
"""
import uuid
import random
from datetime import timedelta
from faker import Faker

from typing import Dict, Any

from common import get_fhir_version
from lib.data.encounters import (ENCOUNTER_CLASSES, ENCOUNTER_STATUSES,
                                ENCOUNTER_PRIORITIES, ENCOUNTER_REASONS, PARTICIPANT_TYPES)
from lib.data.encounter_reasons import ENCOUNTER_REASON_CODES

# Initialize Faker to generate random data
fake = Faker()

def generate_encounter(patient_id: str, practitioner_id: str, location_id: str, organization_id: str) -> Dict[str, Any]:
    """
    Generates a single FHIR Encounter resource.

    :param patient_id: The ID of the patient for the encounter.
    :param practitioner_id: The ID of the practitioner involved in the encounter.
    :param location_id: The ID of the location where the encounter occurred.
    :param organization_id: The ID of the organization providing the service.
    :return: A dictionary representing the FHIR Encounter resource.
    """
    encounter_id = str(uuid.uuid4())
    status = random.choice(ENCOUNTER_STATUSES)
    encounter_class = random.choice(ENCOUNTER_CLASSES)
    encounter_type = random.choice(ENCOUNTER_REASON_CODES)
    priority = random.choice(ENCOUNTER_PRIORITIES)
    reason = random.choice(ENCOUNTER_REASONS)
    participant_type = random.choice(PARTICIPANT_TYPES)

    # Generate encounter period (start and end times)
    start_time = fake.date_time_between(start_date='-1y', end_date='now')

    # Duration varies based on encounter type and status
    if status in ['finished', 'cancelled']:
        duration_minutes = random.randint(15, 120)  # 15 minutes to 2 hours
        end_time = start_time + timedelta(minutes=duration_minutes)
        period = {
            "start": start_time.isoformat(),
            "end": end_time.isoformat()
        }
    else:
        # For ongoing encounters, only start time
        period = {
            "start": start_time.isoformat()
        }

    # Generate identifier
    identifier_value = f"Encounter_{fake.last_name()}_{start_time.strftime('%Y%m%d')}"
    
    # Get FHIR version to determine field structure
    fhir_version = get_fhir_version()

    # Convert encounter_type to proper CodeableConcept structure
    # encounter_type comes from ENCOUNTER_REASON_CODES which has code/display/system
    # but type field needs CodeableConcept with coding array
    encounter_type_codeable = {
        "coding": [
            {
                "system": encounter_type.get("system", "http://snomed.info/sct"),
                "code": encounter_type.get("code", ""),
                "display": encounter_type.get("display", "")
            }
        ],
        "text": encounter_type.get("display", "")
    }
    
    # Create the encounter resource
    encounter_resource = {
        "resourceType": "Encounter",
        "id": encounter_id,
        "identifier": [
            {
                "use": "temp",
                "value": identifier_value
            }
        ],
        "status": status,
        "class": encounter_class,
        "type": [encounter_type_codeable],
        "priority": priority,
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "serviceProvider": {
            "reference": f"Organization/{organization_id}"
        },
        "location": [
            {
                "location": {
                    "reference": f"Location/{location_id}"
                }
            }
        ],
        "participant": [
            {
                "type": [participant_type],
                "actor": {
                    "reference": f"Practitioner/{practitioner_id}"
                }
            }
        ],
        "period": period
    }
    
    # Add reason field based on FHIR version
    if fhir_version == "R4":
        # FHIR R4 uses reasonCode with CodeableConcept
        encounter_resource["reasonCode"] = [
            {
                "coding": [
                    {
                        "system": encounter_type.get("system", "http://snomed.info/sct"),
                        "code": encounter_type.get("code", ""),
                        "display": encounter_type.get("display", reason)
                    }
                ],
                "text": reason
            }
        ]
    else:  # FHIR R5
        # FHIR R5 uses reason with CodeableReference
        encounter_resource["reason"] = [
            {
                "value": [
                    {
                        "concept": {
                            "coding": [
                                {
                                    "system": encounter_type.get("system", "http://snomed.info/sct"),
                                    "code": encounter_type.get("code", ""),
                                    "display": encounter_type.get("display", reason)
                                }
                            ],
                            "text": reason
                        }
                    }
                ]
            }
        ]

    # Add text narrative for generated encounters
    encounter_resource["text"] = {
        "status": "generated",
        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative: Encounter</b><a name=\"{encounter_id}\"> </a></p><div style=\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\">Resource Encounter &quot;{encounter_id}&quot; </p></div><p><b>identifier</b>: id: {identifier_value} (use: TEMP)</p><p><b>status</b>: {status}</p><p><b>class</b>: {encounter_class['coding'][0]['display']}</p><p><b>priority</b>: {priority['coding'][0]['display']}</p><p><b>type</b>: {encounter_type['display']}</p><p><b>subject</b>: <a href=\"patient-{patient_id}.html\">Patient/{patient_id}</a></p><p><b>serviceProvider</b>: <a href=\"organization-{organization_id}.html\">Organization/{organization_id}</a></p><p><b>reason</b>: {reason}</p></div>"
    }

    return encounter_resource
