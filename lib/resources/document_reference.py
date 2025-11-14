"""
Generates FHIR DocumentReference resources with clinical notes for encounters.
"""
import uuid
import random
import base64
from datetime import datetime, timedelta
from faker import Faker
from typing import Dict, Any, Optional

from lib.data.document_references import (
    DOCUMENT_TYPES, DOCUMENT_CATEGORIES, DOCUMENT_REFERENCE_STATUSES,
    DOCUMENT_STATUSES, ATTESTATION_MODES, CLINICAL_NOTE_TEMPLATES
)

# Initialize Faker to generate random data
fake = Faker()


def generate_clinical_note_content(document_type: Dict[str, str], patient_id: str, 
                                   practitioner_name: str, encounter_date: datetime) -> str:
    """
    Generates realistic clinical note content based on document type.
    
    :param document_type: The document type dictionary with code, display, text, system.
    :param patient_id: The patient ID for the note.
    :param practitioner_name: The name of the practitioner authoring the note.
    :param encounter_date: The date/time of the encounter.
    :return: A string containing the clinical note content.
    """
    doc_text = document_type.get("text", "Clinical Note")
    template = CLINICAL_NOTE_TEMPLATES.get(doc_text, CLINICAL_NOTE_TEMPLATES["Progress Note"])
    
    # Generate random clinical data
    chief_complaints = [
        "chest pain", "shortness of breath", "abdominal pain", "headache",
        "fever and chills", "cough", "dizziness", "fatigue", "joint pain",
        "back pain", "nausea and vomiting", "diarrhea", "rash", "sore throat"
    ]
    
    chief_complaint = random.choice(chief_complaints)
    
    # Generate vital signs
    bp_systolic = random.randint(100, 150)
    bp_diastolic = random.randint(60, 90)
    hr = random.randint(60, 100)
    rr = random.randint(12, 20)
    temp = round(random.uniform(97.0, 99.5), 1)
    o2_sat = random.randint(95, 100)
    
    # Generate assessment/plan items
    assessments = [
        "Acute upper respiratory infection",
        "Hypertension, well controlled",
        "Type 2 diabetes mellitus, stable",
        "Acute gastroenteritis",
        "Musculoskeletal strain",
        "Anxiety disorder",
        "Chronic pain syndrome",
        "Acute bronchitis"
    ]
    
    assessment = random.choice(assessments)
    
    plans = [
        "Continue current medications. Follow up in 2 weeks.",
        "Start new medication. Recheck in 1 week.",
        "Order laboratory tests. Follow up with results.",
        "Refer to specialist. Continue current treatment.",
        "Lifestyle modifications recommended. Follow up in 1 month.",
        "Physical therapy referral. Return if symptoms worsen."
    ]
    
    plan = random.choice(plans)
    
    # Fill in template based on document type
    if doc_text == "Progress Note":
        return template.format(
            chief_complaint=chief_complaint,
            additional_symptoms=fake.sentence(),
            bp_systolic=bp_systolic,
            bp_diastolic=bp_diastolic,
            hr=hr,
            rr=rr,
            temp=temp,
            o2_sat=o2_sat,
            general_appearance="Well-appearing, in no acute distress",
            physical_exam=fake.paragraph(),
            assessment=assessment,
            plan=plan
        )
    elif doc_text == "Discharge Summary":
        admission_date = encounter_date - timedelta(days=random.randint(1, 7))
        return template.format(
            admission_date=admission_date.strftime("%Y-%m-%d"),
            discharge_date=encounter_date.strftime("%Y-%m-%d"),
            admitting_diagnosis=assessment,
            discharge_diagnosis=assessment,
            hospital_course=fake.paragraph(),
            discharge_medications="Continue home medications as prescribed.",
            discharge_instructions=plan,
            follow_up="Follow up with primary care physician in 1 week."
        )
    elif doc_text == "History and Physical":
        return template.format(
            chief_complaint=chief_complaint,
            history_present_illness=fake.paragraph(),
            past_medical_history=fake.sentence(),
            physical_examination=fake.paragraph(),
            assessment_plan=f"{assessment}. {plan}"
        )
    elif doc_text == "Consultation Note":
        return template.format(
            reason_for_consultation=chief_complaint,
            history=fake.paragraph(),
            physical_examination=fake.paragraph(),
            assessment=assessment,
            recommendations=plan
        )
    elif doc_text == "Emergency Department Note":
        dispositions = ["Discharged home", "Admitted to hospital", "Transferred to another facility"]
        return template.format(
            chief_complaint=chief_complaint,
            history_present_illness=fake.paragraph(),
            physical_examination=fake.paragraph(),
            assessment=assessment,
            plan=plan,
            disposition=random.choice(dispositions)
        )
    else:
        # Default progress note format
        return template.format(
            chief_complaint=chief_complaint,
            additional_symptoms=fake.sentence(),
            bp_systolic=bp_systolic,
            bp_diastolic=bp_diastolic,
            hr=hr,
            rr=rr,
            temp=temp,
            o2_sat=o2_sat,
            general_appearance="Well-appearing, in no acute distress",
            physical_exam=fake.paragraph(),
            assessment=assessment,
            plan=plan
        )


def generate_document_reference(patient_id: str, practitioner_id: str, 
                               encounter_id: str, binary_id: str,
                               encounter_date: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Generates a single FHIR DocumentReference resource for a clinical note.
    
    :param patient_id: The ID of the patient for the document.
    :param practitioner_id: The ID of the practitioner who authored the document.
    :param encounter_id: The ID of the encounter this document is associated with.
    :param binary_id: The ID of the Binary resource containing the actual note content.
    :param encounter_date: Optional date/time of the encounter. If not provided, generates a random date.
    :return: A dictionary representing the FHIR DocumentReference resource.
    """
    document_reference_id = str(uuid.uuid4())
    document_type = random.choice(DOCUMENT_TYPES)
    category = random.choice(DOCUMENT_CATEGORIES)
    status = random.choice(DOCUMENT_REFERENCE_STATUSES)
    doc_status = random.choice(DOCUMENT_STATUSES)
    
    # Use provided encounter date or generate a random one
    if encounter_date is None:
        document_date = fake.date_time_between(start_date='-1y', end_date='now')
    else:
        # Document is typically created shortly after or during the encounter
        document_date = encounter_date + timedelta(minutes=random.randint(0, 120))
    
    # Generate identifier
    identifier_value = f"DOC-{fake.random_number(digits=8)}"
    
    # Generate practitioner name for note content
    practitioner_name = f"Dr. {fake.last_name()}"
    
    # Create the DocumentReference resource
    document_reference = {
        "resourceType": "DocumentReference",
        "id": document_reference_id,
        "identifier": [
            {
                "system": "http://example.org/documents",
                "value": identifier_value
            }
        ],
        "status": status,
        "docStatus": doc_status,
        "type": {
            "coding": [
                {
                    "system": document_type["system"],
                    "code": document_type["code"],
                    "display": document_type["display"]
                }
            ],
            "text": document_type["text"]
        },
        "category": [category],
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "date": document_date.isoformat(),
        "author": [
            {
                "reference": f"Practitioner/{practitioner_id}",
                "display": practitioner_name
            }
        ],
        "context": {
            "reference": f"Encounter/{encounter_id}"
        },
        "content": [
            {
                "attachment": {
                    "contentType": "text/plain",
                    "language": "en-US",
                    "url": f"Binary/{binary_id}",
                    "creation": document_date.isoformat()
                }
            }
        ]
    }
    
    # Add attestation (70% chance)
    if random.random() < 0.7:
        attestation_mode = random.choice(ATTESTATION_MODES)
        attestation_time = document_date + timedelta(minutes=random.randint(5, 60))
        document_reference["attester"] = [
            {
                "mode": attestation_mode,
                "time": attestation_time.isoformat(),
                "party": {
                    "reference": f"Practitioner/{practitioner_id}",
                    "display": practitioner_name
                }
            }
        ]
    
    # Add description
    document_reference["description"] = f"{document_type['text']} for encounter {encounter_id[:8]}"
    
    # Add period if we have encounter date
    if encounter_date:
        document_reference["period"] = {
            "start": encounter_date.isoformat(),
            "end": (encounter_date + timedelta(minutes=random.randint(15, 120))).isoformat()
        }
    
    # Add text narrative
    document_reference["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: DocumentReference</b><a name="{document_reference_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource DocumentReference &quot;{document_reference_id}&quot; </p>
            </div>
            <p><b>identifier</b>: id: {identifier_value}</p>
            <p><b>status</b>: {status}</p>
            <p><b>docStatus</b>: {doc_status}</p>
            <p><b>type</b>: {document_type['text']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> ({document_type['system']}#{document_type['code']})</span></p>
            <p><b>subject</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>date</b>: {document_date.strftime('%Y-%m-%dT%H:%M:%S')}</p>
            <p><b>author</b>: <a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a> ({practitioner_name})</p>
            <p><b>context</b>: <a href="encounter-{encounter_id}.html">Encounter/{encounter_id}</a></p>
            <p><b>content</b>: <a href="binary-{binary_id}.html">Binary/{binary_id}</a></p>
        </div>"""
    }
    
    return document_reference


def generate_binary_resource(patient_id: str, practitioner_id: str, 
                             document_type: Dict[str, str], encounter_date: datetime) -> Dict[str, Any]:
    """
    Generates a FHIR Binary resource containing the actual clinical note content.
    
    :param patient_id: The ID of the patient for the note.
    :param practitioner_id: The ID of the practitioner authoring the note.
    :param document_type: The document type dictionary.
    :param encounter_date: The date/time of the encounter.
    :return: A dictionary representing the FHIR Binary resource.
    """
    binary_id = str(uuid.uuid4())
    practitioner_name = f"Dr. {fake.last_name()}"
    
    # Generate the clinical note content
    note_content = generate_clinical_note_content(
        document_type, patient_id, practitioner_name, encounter_date
    )
    
    # Encode content as base64
    content_base64 = base64.b64encode(note_content.encode('utf-8')).decode('utf-8')
    
    # Create the Binary resource
    binary_resource = {
        "resourceType": "Binary",
        "id": binary_id,
        "contentType": "text/plain",
        "data": content_base64
    }
    
    return binary_resource

