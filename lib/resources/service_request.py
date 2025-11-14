"""
ServiceRequest resource generation function.
"""
import uuid
import random
from faker import Faker
from typing import Dict, Any

from common import get_fhir_version
from lib.data.service_requests import (SERVICE_REQUEST_TYPES, SERVICE_REQUEST_STATUSES, 
                                     SERVICE_REQUEST_INTENTS, SERVICE_REQUEST_PRIORITIES,
                                     SERVICE_REQUEST_REASONS, BODY_SITE_CODES)


# Initialize Faker to generate random data
fake = Faker()


def generate_service_request(patient_id: str, practitioner_id: str, encounter_id: str = None) -> Dict[str, Any]:
    """
    Generates a single FHIR ServiceRequest resource.
    
    :param patient_id: The ID of the patient for the service request.
    :param practitioner_id: The ID of the practitioner who requested the service.
    :param encounter_id: Optional ID of the encounter this service request is associated with.
    :return: A dictionary representing the FHIR ServiceRequest resource.
    """
    service_request_id = str(uuid.uuid4())
    service_type = random.choice(SERVICE_REQUEST_TYPES)
    status = random.choice(SERVICE_REQUEST_STATUSES)
    intent = random.choice(SERVICE_REQUEST_INTENTS)
    priority = random.choice(SERVICE_REQUEST_PRIORITIES)
    reason = random.choice(SERVICE_REQUEST_REASONS)
    body_site = random.choice(BODY_SITE_CODES)
    
    # Generate occurrence date (when the service should be performed)
    occurrence_date = fake.date_time_between(start_date='-30d', end_date='+30d')
    # Ensure timezone is included in datetime strings (FHIR requirement)
    if occurrence_date.tzinfo is None:
        from datetime import timezone
        occurrence_date = occurrence_date.replace(tzinfo=timezone.utc)
    
    # Generate authored date (when the request was created)
    authored_date = fake.date_time_between(start_date='-7d', end_date='now')
    # Ensure timezone is included in datetime strings (FHIR requirement)
    if authored_date.tzinfo is None:
        from datetime import timezone
        authored_date = authored_date.replace(tzinfo=timezone.utc)
    
    # Get FHIR version to determine field structure
    fhir_version = get_fhir_version()
    
    # Create the service request resource
    service_request = {
        "resourceType": "ServiceRequest",
        "id": service_request_id,
        "status": status,
        "intent": intent,
        "priority": priority,
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "occurrenceDateTime": occurrence_date.isoformat(),
        "authoredOn": authored_date.isoformat(),
        "requester": {
            "reference": f"Practitioner/{practitioner_id}",
            "display": f"Dr. {fake.last_name()}"
        }
    }
    
    # Add code field based on FHIR version
    if fhir_version == "R4":
        # FHIR R4: code is a CodeableConcept directly
        service_request["code"] = {
            "coding": [
                {
                    "system": service_type["system"],
                    "code": service_type["code"],
                    "display": service_type["display"]
                }
            ],
            "text": service_type["text"]
        }
    else:  # FHIR R5
        # FHIR R5: code uses concept wrapper
        service_request["code"] = {
            "concept": {
                "coding": [
                    {
                        "system": service_type["system"],
                        "code": service_type["code"],
                        "display": service_type["display"]
                    }
                ],
                "text": service_type["text"]
            }
        }
    
    # Add reason field based on FHIR version
    if fhir_version == "R4":
        # FHIR R4 uses reasonCode (array of CodeableConcept)
        service_request["reasonCode"] = [
            {
                "text": reason
            }
        ]
    else:  # FHIR R5
        # FHIR R5 uses reason with CodeableReference
        service_request["reason"] = [
            {
                "concept": {
                    "text": reason
                }
            }
        ]
    
    # Add encounter reference if provided
    if encounter_id:
        service_request["encounter"] = {
            "reference": f"Encounter/{encounter_id}"
        }
    
    # Add body site extension
    service_request["extension"] = [
        {
            "url": "http://hl7.org/fhir/StructureDefinition/bodysitecode",
            "valueCodeableConcept": {
                "coding": [
                    {
                        "system": body_site["system"],
                        "code": body_site["code"],
                        "display": body_site["display"]
                    }
                ]
            }
        }
    ]
    
    # Add text narrative
    service_request["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: ServiceRequest</b><a name="{service_request_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource ServiceRequest &quot;{service_request_id}&quot; </p>
            </div>
            <p><b>status</b>: {status}</p>
            <p><b>intent</b>: {intent}</p>
            <p><b>priority</b>: {priority}</p>
            <h3>Codes</h3>
            <table class="grid">
                <tr><td>-</td><td><b>Concept</b></td></tr>
                <tr><td>*</td><td>{service_type['text']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> ({service_type['system']}#{service_type['code']})</span></td></tr>
            </table>
            <p><b>subject</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>occurrence</b>: {occurrence_date.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
            <p><b>requester</b>: <a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a></p>
            <h3>Reasons</h3>
            <table class="grid">
                <tr><td>-</td><td><b>Concept</b></td></tr>
                <tr><td>*</td><td>{reason} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> ()</span></td></tr>
            </table>
        </div>"""
    }
    
    return service_request
