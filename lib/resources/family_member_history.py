"""
FamilyMemberHistory resource generation function.
"""
import uuid
import random
from faker import Faker
from typing import Dict, Any

from common import get_fhir_version
from lib.data.family_member_history import (FAMILY_MEMBER_STATUSES, FAMILY_RELATIONSHIPS, 
                                          ADMINISTRATIVE_GENDERS, FAMILY_CONDITIONS, 
                                          PARTICIPANT_FUNCTIONS, FAMILY_CONDITION_NOTES,
                                          AGE_RANGES, CAUSES_OF_DEATH)


# Initialize Faker to generate random data
fake = Faker()


def generate_family_member_history(patient_id: str, practitioner_id: str = None) -> Dict[str, Any]:
    """
    Generates a single FHIR FamilyMemberHistory resource.
    
    :param patient_id: The ID of the patient whose family member history this is.
    :param practitioner_id: Optional ID of the practitioner who recorded the history.
    :return: A dictionary representing the FHIR FamilyMemberHistory resource.
    """
    family_member_id = str(uuid.uuid4())
    status = random.choice(FAMILY_MEMBER_STATUSES)
    relationship = random.choice(FAMILY_RELATIONSHIPS)
    gender = random.choice(ADMINISTRATIVE_GENDERS)
    participant_function = random.choice(PARTICIPANT_FUNCTIONS)
    
    # Generate age range based on relationship
    age_range = AGE_RANGES.get(relationship["code"], (20, 80))
    age_at_onset = random.randint(age_range[0], age_range[1])
    current_age = age_at_onset + random.randint(0, 20)
    
    # Generate conditions (1-3 conditions per family member)
    num_conditions = random.randint(1, 3)
    selected_conditions = random.sample(FAMILY_CONDITIONS, num_conditions)
    
    # Generate date when history was recorded
    record_date = fake.date_between(start_date='-2y', end_date='today')
    
    # Generate identifier
    identifier_value = f"FMH-{fake.random_number(digits=5)}"
    
    # Get FHIR version to determine field structure
    fhir_version = get_fhir_version()
    
    # Create the family member history resource
    family_member_history = {
        "resourceType": "FamilyMemberHistory",
        "id": family_member_id,
        "identifier": [
            {
                "value": identifier_value
            }
        ],
        "instantiatesUri": [
            "http://example.org/family-member-history-questionnaire"
        ],
        "status": status,
        "patient": {
            "reference": f"Patient/{patient_id}",
            "display": f"Patient {patient_id[:8]}"
        },
        "date": record_date.isoformat(),
        "relationship": {
            "coding": [
                {
                    "system": relationship["system"],
                    "code": relationship["code"],
                    "display": relationship["display"]
                }
            ]
        },
        "sex": {
            "coding": [
                {
                    "system": gender["system"],
                    "code": gender["code"],
                    "display": gender["display"]
                }
            ]
        }
    }
    
    # Add participant if practitioner is provided (R5 only - not in R4)
    if practitioner_id and fhir_version != "R4":
        family_member_history["participant"] = [
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
                    "reference": f"Practitioner/{practitioner_id}"
                }
            }
        ]
    
    # Add conditions
    conditions = []
    for condition in selected_conditions:
        # Determine if condition contributed to death
        contributed_to_death = random.choice([True, False]) and random.random() < 0.3
        
        # Generate onset age
        min_onset_age = max(age_range[0], 1)
        max_onset_age = min(age_range[1], current_age - 1)
        
        # Ensure we have a valid range
        if min_onset_age > max_onset_age:
            min_onset_age = max(1, current_age - 10)
            max_onset_age = current_age - 1
        
        # If still invalid, use a default range
        if min_onset_age > max_onset_age:
            min_onset_age = 1
            max_onset_age = current_age - 1 if current_age > 1 else 1
        
        onset_age = random.randint(min_onset_age, max_onset_age)
        
        condition_entry = {
            "code": {
                "coding": [
                    {
                        "system": condition["system"],
                        "code": condition["code"],
                        "display": condition["display"]
                    }
                ],
                "text": condition["text"]
            },
            "contributedToDeath": contributed_to_death,
            "onsetAge": {
                "value": onset_age,
                "unit": "yr",
                "system": "http://unitsofmeasure.org",
                "code": "a"
            },
            "note": [
                {
                    "text": random.choice(FAMILY_CONDITION_NOTES)
                }
            ]
        }
        
        # Add death information if condition contributed to death
        if contributed_to_death:
            death_age = onset_age + random.randint(1, 20)
            condition_entry["note"].append({
                "text": f"Passed away at age {death_age} from {random.choice(CAUSES_OF_DEATH).lower()}"
            })
        
        conditions.append(condition_entry)
    
    family_member_history["condition"] = conditions
    
    # Generate text narrative
    relationship_display = relationship["display"]
    gender_display = gender["display"]
    
    # Create a simple narrative
    if contributed_to_death:
        death_cause = random.choice(CAUSES_OF_DEATH)
        narrative_text = f"{relationship_display.capitalize()} died of {death_cause.lower()} aged {death_age}"
    else:
        if current_age > age_range[1]:
            narrative_text = f"{relationship_display.capitalize()} is deceased, had {', '.join([c['text'] for c in selected_conditions])}"
        else:
            narrative_text = f"{relationship_display.capitalize()} (age {current_age}) has {', '.join([c['text'] for c in selected_conditions])}"
    
    family_member_history["text"] = {
        "status": "generated",
        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">{narrative_text}</div>"
    }
    
    return family_member_history
