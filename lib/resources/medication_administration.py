"""
MedicationAdministration resource generation function.
"""
import uuid
import random
from datetime import timedelta
from faker import Faker
from typing import Dict, Any, Optional

from lib.data.medication_administrations import (MEDICATION_ADMINISTRATION_STATUSES, MEDICATIONS,
                                               ADMINISTRATION_ROUTES, ADMINISTRATION_METHODS,
                                               ADMINISTRATION_REASONS, DOSAGE_TEXTS, DOSE_QUANTITIES,
                                               ADMINISTRATION_NOTES, PERFORMER_ROLES, SIGNATURE_TYPES)


# Initialize Faker to generate random data
fake = Faker()


def generate_medication_administration(patient_id: str, practitioner_id: str, 
                                    medication_request_id: Optional[str] = None,
                                    encounter_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Generates a single FHIR MedicationAdministration resource.
    
    :param patient_id: The ID of the patient receiving the medication.
    :param practitioner_id: The ID of the practitioner administering the medication.
    :param medication_request_id: Optional ID of the medication request this administration fulfills.
    :param encounter_id: Optional ID of the encounter this administration is associated with.
    :return: A dictionary representing the FHIR MedicationAdministration resource.
    """
    medication_admin_id = str(uuid.uuid4())
    status = random.choice(MEDICATION_ADMINISTRATION_STATUSES)
    medication = random.choice(MEDICATIONS)
    route = random.choice(ADMINISTRATION_ROUTES)
    method = random.choice(ADMINISTRATION_METHODS)
    reason = random.choice(ADMINISTRATION_REASONS)
    dosage_text = random.choice(DOSAGE_TEXTS)
    dose_quantity = random.choice(DOSE_QUANTITIES)
    note = random.choice(ADMINISTRATION_NOTES)
    performer_role = random.choice(PERFORMER_ROLES)
    signature_type = random.choice(SIGNATURE_TYPES)
    
    # Generate occurrence times
    start_time = fake.date_time_between(start_date='-30d', end_date='now')
    # For ongoing medications, don't set end time
    occurrence_period = {
        "start": start_time.isoformat()
    }
    
    # 30% chance of being completed (with end time)
    if random.random() < 0.3 and status in ["completed", "stopped"]:
        end_time = start_time + timedelta(hours=random.randint(1, 72))
        occurrence_period["end"] = end_time.isoformat()
    
    # Generate contained medication resource
    contained_medication_id = f"med{random.randint(1000, 9999)}"
    contained_medication = {
        "resourceType": "Medication",
        "id": contained_medication_id,
        "code": {
            "coding": [
                {
                    "system": medication["system"],
                    "code": medication["code"],
                    "display": medication["display"]
                }
            ]
        }
    }
    
    # Generate provenance for event history
    provenance_id = "signature"
    recorded_time = fake.date_time_between(start_date='-7d', end_date='now')
    signature_data = fake.text(max_nb_chars=20).encode('utf-8').hex()
    
    contained_provenance = {
        "resourceType": "Provenance",
        "id": provenance_id,
        "target": [
            {
                "reference": f"ServiceRequest/{str(uuid.uuid4())}"
            }
        ],
        "recorded": recorded_time.isoformat(),
        "agent": [
            {
                "role": [
                    {
                        "coding": [
                            {
                                "system": performer_role["system"],
                                "code": performer_role["code"],
                                "display": performer_role["display"]
                            }
                        ]
                    }
                ],
                "who": {
                    "reference": f"Practitioner/{practitioner_id}",
                    "display": f"Dr. {fake.last_name()}"
                }
            }
        ],
        "signature": [
            {
                "type": [
                    {
                        "system": signature_type["system"],
                        "code": signature_type["code"],
                        "display": signature_type["display"]
                    }
                ],
                "when": recorded_time.isoformat(),
                "who": {
                    "reference": f"Practitioner/{practitioner_id}",
                    "display": f"Dr. {fake.last_name()}"
                },
                "targetFormat": "application/fhir+xml",
                "sigFormat": "application/signature+xml",
                "data": signature_data
            }
        ]
    }
    
    # Create the medication administration resource
    medication_administration = {
        "resourceType": "MedicationAdministration",
        "id": medication_admin_id,
        "contained": [contained_medication, contained_provenance],
        "status": status,
        "medication": {
            "reference": {
                "reference": f"#{contained_medication_id}"
            }
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": f"Patient {patient_id[:8]}"
        },
        "occurencePeriod": occurrence_period,
        "performer": [
            {
                "actor": {
                    "reference": {
                        "reference": f"Practitioner/{practitioner_id}",
                        "display": f"Dr. {fake.last_name()}"
                    }
                }
            }
        ],
        "reason": [
            {
                "concept": {
                    "coding": [
                        {
                            "system": reason["system"],
                            "code": reason["code"],
                            "display": reason["display"]
                        }
                    ]
                }
            }
        ],
        "dosage": {
            "text": dosage_text,
            "route": {
                "coding": [
                    {
                        "system": route["system"],
                        "code": route["code"],
                        "display": route["display"]
                    }
                ]
            },
            "method": {
                "text": method
            },
            "dose": {
                "value": dose_quantity["value"],
                "unit": dose_quantity["unit"],
                "system": "http://unitsofmeasure.org",
                "code": dose_quantity["code"]
            }
        },
        "eventHistory": [
            {
                "reference": f"#{provenance_id}",
                "display": signature_type["display"]
            }
        ]
    }
    
    # Add medication request reference if provided
    if medication_request_id:
        medication_administration["request"] = {
            "reference": f"MedicationRequest/{medication_request_id}"
        }
    
    # Add encounter reference if provided
    if encounter_id:
        medication_administration["encounter"] = {
            "reference": f"Encounter/{encounter_id}",
            "display": f"Encounter {encounter_id[:8]}"
        }
    
    # Add note if present
    if random.random() < 0.7:
        medication_administration["note"] = [
            {
                "text": note
            }
        ]
    
    # Generate text narrative
    medication_administration["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: MedicationAdministration</b><a name="{medication_admin_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource MedicationAdministration &quot;{medication_admin_id}&quot; </p>
            </div>
            <p><b>status</b>: {status}</p>
            <h3>Medications</h3>
            <table class="grid">
                <tr><td>-</td><td><b>Reference</b></td></tr>
                <tr><td>*</td><td><a name="{contained_medication_id}"> </a><blockquote><p/><p><a name="{contained_medication_id}"> </a></p><p><b>code</b>: {medication['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-v3-ndc.html">National drug codes</a>#{medication['code']})</span></p></blockquote></td></tr>
            </table>
            <p><b>subject</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a> &quot;Patient {patient_id[:8]}&quot;</p>
            {f'<p><b>encounter</b>: <a href="encounter-{encounter_id}.html">Encounter/{encounter_id}</a></p>' if encounter_id else ''}
            <p><b>occurence</b>: {start_time.strftime('%Y-%m-%dT%H:%M:%S+01:00')} {'--&gt; (ongoing)' if 'end' not in occurrence_period else f'--&gt; {occurrence_period["end"]}'}</p>
            <blockquote>
                <p><b>performer</b></p>
                <h3>Actors</h3>
                <table class="grid">
                    <tr><td>-</td><td><b>Reference</b></td></tr>
                    <tr><td>*</td><td><a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a> &quot;Dr. {fake.last_name()}&quot;</td></tr>
                </table>
            </blockquote>
            <h3>Reasons</h3>
            <table class="grid">
                <tr><td>-</td><td><b>Concept</b></td></tr>
                <tr><td>*</td><td>{reason['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-reason-medication-given.html">Reason Medication Given Codes</a>#{reason['code']})</span></td></tr>
            </table>
            {f'<p><b>request</b>: <a href="medicationrequest-{medication_request_id}.html">MedicationRequest/{medication_request_id}</a></p>' if medication_request_id else ''}
            <h3>Dosages</h3>
            <table class="grid">
                <tr><td>-</td><td><b>Text</b></td><td><b>Route</b></td><td><b>Method</b></td><td><b>Dose</b></td></tr>
                <tr><td>*</td><td>{dosage_text}</td><td>{route['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="https://browser.ihtsdotools.org/">SNOMED CT</a>#{route['code']})</span></td><td>{method} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> ()</span></td><td>{dose_quantity['value']} {dose_quantity['unit']}<span style="background: LightGoldenRodYellow"> (Details: UCUM code {dose_quantity['code']} = '{dose_quantity['unit']}')</span></td></tr>
            </table>
            <p><b>eventHistory</b>: <a name="signature"> </a></p>
            <blockquote>
                <p/><p><a name="signature"> </a></p>
                <p><b>target</b>: <a href="servicerequest-example2.html">ServiceRequest/physiotherapy</a></p>
                <p><b>recorded</b>: {recorded_time.strftime('%d %b %Y, %I:%M:%S %p')}</p>
                <h3>Agents</h3>
                <table class="grid">
                    <tr><td>-</td><td><b>Role</b></td><td><b>Who</b></td></tr>
                    <tr><td>*</td><td>{performer_role['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-v3-ParticipationType.html">ParticipationType</a>#{performer_role['code']})</span></td><td><a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a> &quot;Dr. {fake.last_name()}&quot;</td></tr>
                </table>
                <h3>Signatures</h3>
                <table class="grid">
                    <tr><td>-</td><td><b>Type</b></td><td><b>When</b></td><td><b>Who</b></td><td><b>TargetFormat</b></td><td><b>SigFormat</b></td><td><b>Data</b></td></tr>
                    <tr><td>*</td><td>{signature_type['display']} (Details: {signature_type['system']} code {signature_type['code']} = '{signature_type['display']}', stated as '{signature_type['display']}')</td><td>{recorded_time.strftime('%d %b %Y, %I:%M:%S %p')}</td><td><a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a> &quot;Dr. {fake.last_name()}&quot;</td><td>application/fhir+xml</td><td>application/signature+xml</td><td>{signature_data}</td></tr>
                </table>
            </blockquote>
        </div>"""
    }
    
    return medication_administration
