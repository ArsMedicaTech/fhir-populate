"""
DiagnosticReport resource generation function.
"""
import uuid
import random
import base64
from datetime import datetime, timedelta, timezone
from faker import Faker
from typing import Dict, Any, List

from lib.data.diagnostic_reports import (DIAGNOSTIC_REPORT_TYPES, DIAGNOSTIC_REPORT_STATUSES, 
                                        DIAGNOSTIC_REPORT_CATEGORIES, LABORATORY_NAMES, PATHOLOGIST_NAMES)

# Initialize Faker to generate random data
fake = Faker()


def generate_diagnostic_report(patient_id: str, practitioner_id: str, encounter_id: str, 
                              observation_ids: List[str]) -> Dict[str, Any]:
    """
    Generates a single FHIR DiagnosticReport resource.
    
    :param patient_id: The ID of the patient for the diagnostic report.
    :param practitioner_id: The ID of the practitioner who authored the report.
    :param encounter_id: The ID of the encounter this report is associated with.
    :param observation_ids: List of observation IDs to include in the result field.
    :return: A dictionary representing the FHIR DiagnosticReport resource.
    """
    diagnostic_report_id = str(uuid.uuid4())
    report_type = random.choice(DIAGNOSTIC_REPORT_TYPES)
    status = random.choice(DIAGNOSTIC_REPORT_STATUSES)
    category = random.choice(DIAGNOSTIC_REPORT_CATEGORIES)
    laboratory_name = random.choice(LABORATORY_NAMES)
    pathologist_name = random.choice(PATHOLOGIST_NAMES)
    
    # Generate effective and issued dates
    effective_date = fake.date_time_between(start_date='-1y', end_date='now')
    # Ensure timezone is included in datetime strings (FHIR requirement)
    if effective_date.tzinfo is None:
        effective_date = effective_date.replace(tzinfo=timezone.utc)
    
    issued_date = effective_date + timedelta(minutes=random.randint(30, 180))
    # Ensure timezone is included (instants require timezone)
    if issued_date.tzinfo is None:
        issued_date = issued_date.replace(tzinfo=timezone.utc)
    
    # Generate a simple PDF-like content (base64 encoded)
    pdf_content = generate_simple_pdf_content(patient_id, report_type, laboratory_name, pathologist_name)
    
    # Create result references from observation IDs
    result_references = [{"reference": f"Observation/{obs_id}"} for obs_id in observation_ids]
    
    # Generate identifier
    identifier_value = f"RPT-{fake.random_number(digits=7)}"
    
    # Create the diagnostic report resource
    diagnostic_report = {
        "resourceType": "DiagnosticReport",
        "id": diagnostic_report_id,
        "meta": {
            "tag": [
                {
                    "system": "http://example.org/fhir/CodeSystem/workflow-codes",
                    "code": "01",
                    "display": "Needs Review"
                }
            ]
        },
        "identifier": [
            {
                "system": "http://acme.com/lab/reports",
                "value": identifier_value
            }
        ],
        "status": status,
        "category": [category],
        "code": {
            "coding": [
                {
                    "system": report_type["system"],
                    "code": report_type["code"],
                    "display": report_type["display"]
                }
            ],
            "text": report_type["text"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "encounter": {
            "reference": f"Encounter/{encounter_id}"
        },
        "effectiveDateTime": effective_date.isoformat(),
        "issued": issued_date.isoformat(),
        "performer": [
            {
                "reference": f"Practitioner/{practitioner_id}",
                "display": f"Dr. {pathologist_name}"
            }
        ],
        "result": result_references,
        "presentedForm": [
            {
                "contentType": "application/pdf",
                "language": "en-US",
                "data": pdf_content
            }
        ]
    }
    
    # Add text narrative
    diagnostic_report["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <h3>{report_type['text']} Report for Patient {patient_id} issued {issued_date.strftime('%d-%b %Y %H:%M')}</h3>
            <pre>
Test                  Units       Value       Reference Range
Sample Test 1         mg/dL       12.5        10.0 - 15.0
Sample Test 2         %           45.2        40.0 - 50.0
Sample Test 3         /HPF        2.1         0 - 5
            </pre>
            <p>{laboratory_name} signed: {pathologist_name}</p>
        </div>"""
    }
    
    return diagnostic_report


def generate_simple_pdf_content(patient_id: str, report_type: Dict[str, str], 
                               laboratory_name: str, pathologist_name: str) -> str:
    """
    Generates a simple PDF-like content as base64 encoded string.
    This is a minimal PDF structure for demonstration purposes.
    """
    # This is a very basic PDF structure - in a real implementation,
    # you would use a proper PDF generation library
    pdf_content = f"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 200
>>
stream
BT
/F1 12 Tf
100 700 Td
({report_type['text']} Report) Tj
0 -20 Td
(Patient ID: {patient_id}) Tj
0 -20 Td
(Laboratory: {laboratory_name}) Tj
0 -20 Td
(Pathologist: {pathologist_name}) Tj
0 -20 Td
(Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000204 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
454
%%EOF"""
    
    # Encode as base64
    return base64.b64encode(pdf_content.encode('utf-8')).decode('utf-8')
