"""
ClinicalImpression resource generation function.
"""
import uuid
import random
from datetime import timedelta, timezone
from faker import Faker
from typing import Dict, Any

from common import get_fhir_version
from lib.data.clinical_impressions import (CLINICAL_IMPESSION_STATUSES, CLINICAL_IMPESSION_DESCRIPTIONS,
                                         CLINICAL_PROBLEMS, CLINICAL_FINDINGS, CLINICAL_SUMMARIES,
                                         INVESTIGATION_TYPES, INVESTIGATION_FINDINGS)


# Initialize Faker to generate random data
fake = Faker()


def generate_clinical_impression(patient_id: str, practitioner_id: str, encounter_id: str = None) -> Dict[str, Any]:
    """
    Generates a single FHIR ClinicalImpression resource.
    
    :param patient_id: The ID of the patient for the clinical impression.
    :param practitioner_id: The ID of the practitioner who made the clinical impression.
    :param encounter_id: Optional ID of the encounter this clinical impression is associated with.
    :return: A dictionary representing the FHIR ClinicalImpression resource.
    """
    clinical_impression_id = str(uuid.uuid4())
    status = random.choice(CLINICAL_IMPESSION_STATUSES)
    description = random.choice(CLINICAL_IMPESSION_DESCRIPTIONS)
    problem = random.choice(CLINICAL_PROBLEMS)
    summary = random.choice(CLINICAL_SUMMARIES)
    clinical_finding = random.choice(CLINICAL_FINDINGS)
    
    # Generate effective period (start and end times)
    start_time = fake.date_time_between(start_date='-7d', end_date='now')
    # Ensure timezone is included in datetime strings (FHIR requirement)
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    
    duration_minutes = random.randint(30, 180)  # 30 minutes to 3 hours
    end_time = start_time + timedelta(minutes=duration_minutes)
    
    # Generate date (when the impression was documented)
    date = end_time + timedelta(minutes=random.randint(5, 30))
    # Ensure timezone is included in datetime strings (FHIR requirement)
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    
    # Get FHIR version to determine field structure
    fhir_version = get_fhir_version()
    
    # Generate investigation findings
    num_findings = random.randint(2, 5)
    investigation_findings = random.sample(INVESTIGATION_FINDINGS, num_findings)
    investigation_type = random.choice(INVESTIGATION_TYPES)
    
    # Generate identifier
    identifier_value = f"CI-{fake.random_number(digits=5)}"
    
    # Create the clinical impression resource
    clinical_impression = {
        "resourceType": "ClinicalImpression",
        "id": clinical_impression_id,
        "identifier": [
            {
                "value": identifier_value
            }
        ],
        "status": status,
        "description": description,
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "effectivePeriod": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat()
        },
        "date": date.isoformat(),
        "problem": [
            {
                "display": problem
            }
        ],
        "summary": summary
    }
    
    # Add performer/assessor based on FHIR version
    if fhir_version == "R4":
        # FHIR R4 uses 'assessor' not 'performer'
        clinical_impression["assessor"] = {
            "reference": f"Practitioner/{practitioner_id}",
            "display": f"Dr. {fake.last_name()}"
        }
    else:  # FHIR R5
        # FHIR R5 uses 'performer'
        clinical_impression["performer"] = {
            "reference": f"Practitioner/{practitioner_id}",
            "display": f"Dr. {fake.last_name()}"
        }
    
    # Add finding field based on FHIR version
    if fhir_version == "R4":
        # FHIR R4: finding uses itemCodeableConcept directly
        clinical_impression["finding"] = [
            {
                "itemCodeableConcept": {
                    "coding": [
                        {
                            "system": clinical_finding["system"],
                            "code": clinical_finding["code"],
                            "display": clinical_finding["display"]
                        }
                    ]
                }
            }
        ]
    else:  # FHIR R5
        # FHIR R5: finding uses item wrapper
        clinical_impression["finding"] = [
            {
                "item": {
                    "concept": {
                        "coding": [
                            {
                                "system": clinical_finding["system"],
                                "code": clinical_finding["code"],
                                "display": clinical_finding["display"]
                            }
                        ]
                    }
                }
            }
        ]
    
    # Add encounter reference if provided
    if encounter_id:
        clinical_impression["encounter"] = {
            "reference": f"Encounter/{encounter_id}"
        }
    
    # Add investigation details
    investigation_items = []
    for finding in investigation_findings:
        investigation_items.append({
            "display": finding
        })
    
    clinical_impression["investigation"] = [
        {
            "code": {
                "text": investigation_type
            },
            "item": investigation_items
        }
    ]
    
    # Generate investigation items HTML
    investigation_items_html = ''.join([f'<item><display value="{finding}"/></item>' for finding in investigation_findings])
    
    # Generate finding display
    finding_code = clinical_finding['code']
    finding_system = clinical_finding['system'].split('/')[-1]
    
    # Add text narrative
    clinical_impression["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: ClinicalImpression</b><a name="{clinical_impression_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource ClinicalImpression &quot;{clinical_impression_id}&quot; </p>
            </div>
            <p><b>identifier</b>: id: {identifier_value}</p>
            <p><b>status</b>: {status}</p>
            <p><b>description</b>: {description}</p>
            <p><b>subject</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>encounter</b>: <a href="encounter-{encounter_id if encounter_id else 'unknown'}.html">Encounter/{encounter_id if encounter_id else 'unknown'}</a></p>
            <p><b>effective</b>: {start_time.strftime('%Y-%m-%dT%H:%M:%S%z')} --&gt; {end_time.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
            <p><b>date</b>: {date.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
            <p><b>{'assessor' if fhir_version == 'R4' else 'performer'}</b>: <a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a></p>
            <p><b>problem</b>: <span>: {problem}</span></p>
            <p><b>summary</b>: <span title="Investigation: {investigation_type} - {', '.join(investigation_findings)}">{summary}</span></p>
            <blockquote>
                <p><b>finding</b></p>
                <h3>Items</h3>
                <table class="grid">
                    <tr><td>-</td><td><b>Concept</b></td></tr>
                    <tr><td>*</td><td>{finding_code} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> ({finding_system}#{finding_code})</span></td></tr>
                </table>
            </blockquote>
        </div>"""
    }
    
    return clinical_impression
