"""
Generates FHIR Procedure resources for testing purposes.
"""
import uuid
import random
from datetime import timezone
from faker import Faker

from typing import Dict, Any

from lib.data.procedures import PROCEDURES, PROCEDURE_STATUSES, PROCEDURE_CATEGORIES


# Initialize Faker to generate random data
fake = Faker()


def generate_procedure(patient_id: str, practitioner_id: str) -> Dict[str, Any]:
    """
    Generates a single FHIR Procedure resource.

    :param patient_id: The ID of the patient for the procedure.
    :param practitioner_id: The ID of the practitioner who performed the procedure.
    :return: A dictionary representing the FHIR Procedure resource.
    """
    procedure_id = str(uuid.uuid4())
    procedure = random.choice(PROCEDURES)
    status = random.choice(PROCEDURE_STATUSES)
    category = random.choice(PROCEDURE_CATEGORIES)

    # Generate a random performed date within the last year
    performed_date = fake.date_time_between(start_date='-1y', end_date='now')
    # Ensure timezone is included in datetime strings (FHIR requirement)
    if performed_date.tzinfo is None:
        performed_date = performed_date.replace(tzinfo=timezone.utc)

    procedure_resource = {
        "resourceType": "Procedure",
        "id": procedure_id,
        "status": status,
        "category": category,
        "code": {
            "coding": [
                {
                    "system": procedure["system"],
                    "code": procedure["code"],
                    "display": procedure["display"]
                }
            ],
            "text": procedure["text"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "performer": [
            {
                "actor": {
                    "reference": f"Practitioner/{practitioner_id}"
                }
            }
        ],
        "performedDateTime": performed_date.isoformat()
    }
    
    # Add text narrative (best practice)
    category_display = category.get('coding', [{}])[0].get('display', '') if isinstance(category, dict) and 'coding' in category else ''
    procedure_resource["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Procedure</b><a name="{procedure_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Procedure &quot;{procedure_id}&quot; </p>
            </div>
            <p><b>status</b>: {status}</p>
            <p><b>category</b>: {category_display}</p>
            <p><b>code</b>: {procedure['text']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> ({procedure['system']}#{procedure['code']})</span></p>
            <p><b>subject</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>performer</b>: <a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a></p>
            <p><b>performed</b>: {performed_date.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
        </div>"""
    }
    
    return procedure_resource
