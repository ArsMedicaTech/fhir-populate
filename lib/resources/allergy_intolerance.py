"""
AllergyIntolerance resource generation function.
"""
import uuid
import random
from datetime import timedelta
from faker import Faker
from typing import Dict, Any, Optional

from common import get_fhir_version
from lib.data.allergy_intolerances import (CLINICAL_STATUSES, VERIFICATION_STATUSES, ALLERGY_CATEGORIES,
                                         CRITICALITY_LEVELS, MEDICATION_ALLERGENS, FOOD_ALLERGENS,
                                         ENVIRONMENTAL_ALLERGENS, BIOLOGIC_ALLERGENS, ALLERGY_MANIFESTATIONS,
                                         PARTICIPANT_FUNCTIONS, ALLERGY_NOTES, ONSET_DESCRIPTIONS,
                                         SEVERITY_DESCRIPTIONS)


# Initialize Faker to generate random data
fake = Faker()


def generate_allergy_intolerance(patient_id: str, practitioner_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Generates a single FHIR AllergyIntolerance resource.
    
    :param patient_id: The ID of the patient with the allergy.
    :param practitioner_id: Optional ID of the practitioner who recorded the allergy.
    :return: A dictionary representing the FHIR AllergyIntolerance resource.
    """
    allergy_id = str(uuid.uuid4())
    clinical_status = random.choice(CLINICAL_STATUSES)
    verification_status = random.choice(VERIFICATION_STATUSES)
    category = random.choice(ALLERGY_CATEGORIES)
    criticality = random.choice(CRITICALITY_LEVELS)
    participant_function = random.choice(PARTICIPANT_FUNCTIONS)
    note = random.choice(ALLERGY_NOTES)
    onset_description = random.choice(ONSET_DESCRIPTIONS)
    severity_description = random.choice(SEVERITY_DESCRIPTIONS)
    
    # Select allergen based on category
    if category == "medication":
        allergen = random.choice(MEDICATION_ALLERGENS)
    elif category == "food":
        allergen = random.choice(FOOD_ALLERGENS)
    elif category == "environment":
        allergen = random.choice(ENVIRONMENTAL_ALLERGENS)
    else:  # biologic
        allergen = random.choice(BIOLOGIC_ALLERGENS)
    
    # Generate recorded date (1-10 years ago)
    recorded_date = fake.date_between(start_date='-10y', end_date='-1d')
    
    # Get FHIR version to determine field structure
    fhir_version = get_fhir_version()
    
    # Generate 1-3 manifestations
    num_manifestations = random.randint(1, 3)
    selected_manifestations = random.sample(ALLERGY_MANIFESTATIONS, num_manifestations)
    
    manifestations = []
    for manifestation in selected_manifestations:
        if fhir_version == "R4":
            # FHIR R4: manifestation is CodeableConcept directly
            manifestations.append({
                "coding": [
                    {
                        "system": manifestation["system"],
                        "code": manifestation["code"],
                        "display": manifestation["display"]
                    }
                ]
            })
        else:  # FHIR R5
            # FHIR R5: manifestation uses concept wrapper
            manifestations.append({
                "concept": {
                    "coding": [
                        {
                            "system": manifestation["system"],
                            "code": manifestation["code"],
                            "display": manifestation["display"]
                        }
                    ]
                }
            })
    
    # Create the allergy intolerance resource
    allergy_intolerance = {
        "resourceType": "AllergyIntolerance",
        "id": allergy_id,
        "verificationStatus": {
            "coding": [
                {
                    "system": verification_status["system"],
                    "code": verification_status["code"],
                    "display": verification_status["display"]
                }
            ]
        },
        "category": [category],
        "criticality": criticality,
        "code": {
            "coding": [
                {
                    "system": allergen["system"],
                    "code": allergen["code"],
                    "display": allergen["display"]
                }
            ],
            "text": allergen["text"]
        },
        "patient": {
            "reference": f"Patient/{patient_id}",
            "display": f"Patient {patient_id[:8]}"
        },
        "recordedDate": recorded_date.isoformat(),
        "reaction": [
            {
                "manifestation": manifestations
            }
        ]
    }
    
    # Add clinicalStatus only if verificationStatus is not "entered-in-error" (constraint ait-2)
    if verification_status["code"] != "entered-in-error":
        allergy_intolerance["clinicalStatus"] = {
            "coding": [
                {
                    "system": clinical_status["system"],
                    "code": clinical_status["code"],
                    "display": clinical_status["display"]
                }
            ]
        }
    
    # Add participant if practitioner provided (only in R5)
    if practitioner_id and fhir_version != "R4":
        allergy_intolerance["participant"] = [
            {
                "function": {
                    "coding": [
                        {
                            "system": participant_function["system"],
                            "code": participant_function["code"],
                            "display": participant_function["display"]
                        }
                    ]
                },
                "actor": {
                    "reference": f"Practitioner/{practitioner_id}",
                    "display": f"Dr. {fake.last_name()}"
                }
            }
        ]
    
    # Add note if present (70% chance)
    if random.random() < 0.7:
        allergy_intolerance["note"] = [
            {
                "text": note
            }
        ]
    
    # Add onset information (50% chance)
    if random.random() < 0.5:
        allergy_intolerance["reaction"][0]["onset"] = fake.date_between(
            start_date=recorded_date - timedelta(days=365),
            end_date=recorded_date
        ).isoformat()
    
    # Add severity information (60% chance)
    if random.random() < 0.6:
        allergy_intolerance["reaction"][0]["severity"] = random.choice([
            "mild",
            "moderate", 
            "severe"
        ])
    
    # Add description (40% chance)
    if random.random() < 0.4:
        allergy_intolerance["reaction"][0]["description"] = f"{severity_description} reaction with {onset_description.lower()}"
    
    # Generate text narrative
    if fhir_version == "R4":
        manifestation_texts = [m["coding"][0]["display"] for m in manifestations]
    else:
        manifestation_texts = [m["concept"]["coding"][0]["display"] for m in manifestations]
    manifestation_list = ", ".join(manifestation_texts)
    
    allergy_intolerance["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: AllergyIntolerance</b><a name="{allergy_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource AllergyIntolerance &quot;{allergy_id}&quot; </p>
            </div>
            <p><b>clinicalStatus</b>: {clinical_status['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-allergyintolerance-clinical.html">AllergyIntolerance Clinical Status Codes</a>#{clinical_status['code']})</span></p>
            <p><b>verificationStatus</b>: {verification_status['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-allergyintolerance-verification.html">AllergyIntolerance Verification Status</a>#{verification_status['code']})</span></p>
            <p><b>category</b>: {category}</p>
            <p><b>criticality</b>: {criticality}</p>
            <p><b>code</b>: <span title="  subtance, coded from {allergen['system'].split('/')[-1]}  ">{allergen['text']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-v3-rxNorm.html">{allergen['system'].split('/')[-1]}</a>#{allergen['code']})</span></span></p>
            <p><b>patient</b>: <span title="  the patient that actually has the risk of adverse reaction  "><a href="patient-{patient_id}.html">Patient/{patient_id}</a> &quot;Patient {patient_id[:8]}&quot;</span></p>
            <p><b>recordedDate</b>: <span title="  the date that this entry was recorded  ">{recorded_date.strftime('%Y-%m-%d')}</span></p>
            {f'<h3>Participants</h3><table class="grid"><tr><td>-</td><td><b>Function</b></td><td><b>Actor</b></td></tr><tr><td>*</td><td>{participant_function["display"]} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-provenance-participant-type.html">Provenance participant type</a>#{participant_function["code"]})</span></td><td><a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a> &quot;Dr. {fake.last_name()}&quot;</td></tr></table>' if practitioner_id else ''}
            <blockquote>
                <p><b>reaction</b></p>
                <h3>Manifestations</h3>
                <table class="grid">
                    <tr><td>-</td><td><b>Concept</b></td></tr>
                    {''.join([f'<tr><td>*</td><td>{(m["coding"][0] if fhir_version == "R4" else m["concept"]["coding"][0])["display"]} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="https://browser.ihtsdotools.org/">SNOMED CT</a>#{(m["coding"][0] if fhir_version == "R4" else m["concept"]["coding"][0])["code"]})</span></td></tr>' for m in manifestations])}
                </table>
            </blockquote>
        </div>"""
    }
    
    return allergy_intolerance


def generate_allergy_intolerance_custom(patient_id: str, substance: str, 
                                        practitioner_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Generates a single FHIR AllergyIntolerance resource with a specific substance.

    :param patient_id: The ID of the patient with the allergy.
    :param substance: The name of the substance causing the allergy.
    :param practitioner_id: Optional ID of the practitioner who recorded the allergy.
    :return: A dictionary representing the FHIR AllergyIntolerance resource.
    """
    allergy_id = str(uuid.uuid4())
    clinical_status = random.choice(CLINICAL_STATUSES)
    verification_status = random.choice(VERIFICATION_STATUSES)
    
    # Determine category based on substance (simple heuristic)
    substance_lower = substance.lower()
    if any(med in substance_lower for med in ['penicillin', 'aspirin', 'ibuprofen', 'medication', 'drug']):
        category = "medication"
        allergen = {
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
            "code": "UNKNOWN",
            "display": substance,
            "text": substance
        }
    elif any(food in substance_lower for food in ['peanut', 'milk', 'egg', 'wheat', 'soy', 'fish', 'shellfish', 'tree nut']):
        category = "food"
        allergen = {
            "system": "http://snomed.info/sct",
            "code": "UNKNOWN",
            "display": substance,
            "text": substance
        }
    else:
        category = random.choice(["environment", "food", "medication"])
        allergen = {
            "system": "http://snomed.info/sct",
            "code": "UNKNOWN",
            "display": substance,
            "text": substance
        }
    
    criticality = random.choice(CRITICALITY_LEVELS)
    participant_function = random.choice(PARTICIPANT_FUNCTIONS)
    note = random.choice(ALLERGY_NOTES)
    onset_description = random.choice(ONSET_DESCRIPTIONS)
    severity_description = random.choice(SEVERITY_DESCRIPTIONS)
    
    # Generate recorded date (1-10 years ago)
    recorded_date = fake.date_between(start_date='-10y', end_date='-1d')
    
    # Get FHIR version to determine field structure
    fhir_version = get_fhir_version()
    
    # Generate 1-3 manifestations
    num_manifestations = random.randint(1, 3)
    selected_manifestations = random.sample(ALLERGY_MANIFESTATIONS, num_manifestations)
    
    manifestations = []
    for manifestation in selected_manifestations:
        if fhir_version == "R4":
            manifestations.append({
                "coding": [{
                    "system": manifestation["system"],
                    "code": manifestation["code"],
                    "display": manifestation["display"]
                }]
            })
        else:
            manifestations.append({
                "concept": {
                    "coding": [{
                        "system": manifestation["system"],
                        "code": manifestation["code"],
                        "display": manifestation["display"]
                    }]
                }
            })
    
    # Create the allergy intolerance resource
    allergy_intolerance = {
        "resourceType": "AllergyIntolerance",
        "id": allergy_id,
        "verificationStatus": {
            "coding": [{
                "system": verification_status["system"],
                "code": verification_status["code"],
                "display": verification_status["display"]
            }]
        },
        "category": [category],
        "criticality": criticality,
        "code": {
            "coding": [{
                "system": allergen["system"],
                "code": allergen["code"],
                "display": allergen["display"]
            }],
            "text": allergen["text"]
        },
        "patient": {
            "reference": f"Patient/{patient_id}",
            "display": f"Patient {patient_id[:8]}"
        },
        "recordedDate": recorded_date.isoformat(),
        "reaction": [{
            "manifestation": manifestations
        }]
    }
    
    # Add clinicalStatus only if verificationStatus is not "entered-in-error"
    if verification_status["code"] != "entered-in-error":
        allergy_intolerance["clinicalStatus"] = {
            "coding": [{
                "system": clinical_status["system"],
                "code": clinical_status["code"],
                "display": clinical_status["display"]
            }]
        }
    
    # Add participant if practitioner provided (only in R5)
    if practitioner_id and fhir_version != "R4":
        allergy_intolerance["participant"] = [{
            "function": {
                "coding": [{
                    "system": participant_function["system"],
                    "code": participant_function["code"],
                    "display": participant_function["display"]
                }]
            },
            "actor": {
                "reference": f"Practitioner/{practitioner_id}",
                "display": f"Dr. {fake.last_name()}"
            }
        }]
    
    # Add note
    allergy_intolerance["note"] = [{
        "text": note
    }]
    
    # Add onset information
    allergy_intolerance["reaction"][0]["onset"] = fake.date_between(
        start_date=recorded_date - timedelta(days=365),
        end_date=recorded_date
    ).isoformat()
    
    # Add severity information
    allergy_intolerance["reaction"][0]["severity"] = random.choice([
        "mild",
        "moderate", 
        "severe"
    ])
    
    # Add description
    allergy_intolerance["reaction"][0]["description"] = f"{severity_description} reaction with {onset_description.lower()}"
    
    # Generate text narrative
    if fhir_version == "R4":
        manifestation_texts = [m["coding"][0]["display"] for m in manifestations]
    else:
        manifestation_texts = [m["concept"]["coding"][0]["display"] for m in manifestations]
    manifestation_list = ", ".join(manifestation_texts)
    
    allergy_intolerance["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: AllergyIntolerance</b><a name="{allergy_id}"> </a></p>
            <p><b>code</b>: {substance}</p>
            <p><b>patient</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>recordedDate</b>: {recorded_date.strftime('%Y-%m-%d')}</p>
        </div>"""
    }
    
    return allergy_intolerance