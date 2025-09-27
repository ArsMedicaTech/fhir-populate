"""
CarePlan resource generation function.
"""
import uuid
import random
from datetime import timedelta
from faker import Faker
from typing import Dict, Any, Optional

from lib.data.care_plans import (CARE_PLAN_STATUSES, CARE_PLAN_INTENTS, CARE_PLAN_CATEGORIES,
                                CARE_PLAN_ACTIVITIES, CARE_PLAN_GOALS, CARE_PLAN_DESCRIPTIONS,
                                CARE_PLAN_ADDRESSES, CARE_PLAN_BASED_ON, CARE_PLAN_REPLACES,
                                CARE_PLAN_PART_OF, CARE_PLAN_INSTANTIATES_URI, CARE_PLAN_NOTES,
                                CARE_PLAN_ACTIVITY_DETAILS, CARE_PLAN_ACTIVITY_STATUS,
                                CARE_PLAN_ACTIVITY_OUTCOME)


# Initialize Faker to generate random data
fake = Faker()


def generate_care_plan(patient_id: str, practitioner_id: str, encounter_id: Optional[str] = None,
                      condition_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Generates a single FHIR CarePlan resource.
    
    :param patient_id: The ID of the patient the care plan is for.
    :param practitioner_id: The ID of the practitioner creating the care plan.
    :param encounter_id: Optional ID of the encounter this care plan is associated with.
    :param condition_id: Optional ID of the condition this care plan addresses.
    :return: A dictionary representing the FHIR CarePlan resource.
    """
    care_plan_id = str(uuid.uuid4())
    status = random.choice(CARE_PLAN_STATUSES)
    intent = random.choice(CARE_PLAN_INTENTS)
    category = random.choice(CARE_PLAN_CATEGORIES)
    description = random.choice(CARE_PLAN_DESCRIPTIONS)
    addresses = random.choice(CARE_PLAN_ADDRESSES)
    based_on = random.choice(CARE_PLAN_BASED_ON)
    replaces = random.choice(CARE_PLAN_REPLACES)
    part_of = random.choice(CARE_PLAN_PART_OF)
    instantiates_uri = random.choice(CARE_PLAN_INSTANTIATES_URI)
    note = random.choice(CARE_PLAN_NOTES)
    
    # Generate dates
    created_date = fake.date_between(start_date='-2y', end_date='-1d')
    start_date = created_date
    end_date = start_date + timedelta(days=random.randint(30, 365))
    
    # Generate identifier
    identifier_value = f"CP-{fake.random_number(digits=6)}"
    
    # Generate 1-3 goals
    num_goals = random.randint(1, 3)
    selected_goals = random.sample(CARE_PLAN_GOALS, num_goals)
    goals = [{"reference": f"Goal/{str(uuid.uuid4())}"} for _ in selected_goals]
    
    # Generate 2-5 activities
    num_activities = random.randint(2, 5)
    selected_activities = random.sample(CARE_PLAN_ACTIVITIES, num_activities)
    
    activities = []
    for activity in selected_activities:
        activity_detail = random.choice(CARE_PLAN_ACTIVITY_DETAILS)
        activity_status = random.choice(CARE_PLAN_ACTIVITY_STATUS)
        activity_outcome = random.choice(CARE_PLAN_ACTIVITY_OUTCOME) if activity_status == "completed" else None
        
        activity_entry = {
            "performedActivity": [
                {
                    "concept": {
                        "coding": [
                            {
                                "system": activity["system"],
                                "code": activity["code"],
                                "display": activity["display"]
                            }
                        ],
                        "text": activity["text"]
                    }
                }
            ],
            "plannedActivityReference": {
                "reference": f"{activity_detail['kind']}/{str(uuid.uuid4())}"
            },
            "status": activity_status
        }
        
        if activity_outcome:
            activity_entry["outcome"] = activity_outcome
        
        activities.append(activity_entry)
    
    # Create contained condition if condition_id not provided
    contained_condition_id = f"p{random.randint(1, 999)}"
    contained_condition = {
        "resourceType": "Condition",
        "id": contained_condition_id,
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active"
                }
            ]
        },
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "code": "confirmed"
                }
            ]
        },
        "code": {
            "text": addresses
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": f"Patient {patient_id[:8]}"
        }
    }
    
    # Create the care plan resource
    care_plan = {
        "resourceType": "CarePlan",
        "id": care_plan_id,
        "contained": [contained_condition],
        "identifier": [
            {
                "value": identifier_value
            }
        ],
        "instantiatesUri": [instantiates_uri],
        "basedOn": [
            {
                "display": based_on
            }
        ],
        "replaces": [
            {
                "display": replaces
            }
        ],
        "partOf": [
            {
                "display": part_of
            }
        ],
        "status": status,
        "intent": intent,
        "category": [category],
        "description": description,
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": f"Patient {patient_id[:8]}"
        },
        "period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        },
        "created": created_date.isoformat(),
        "custodian": {
            "reference": f"Practitioner/{practitioner_id}",
            "display": f"Dr. {fake.last_name()}"
        },
        "careTeam": [
            {
                "reference": f"CareTeam/{str(uuid.uuid4())}"
            }
        ],
        "addresses": [
            {
                "reference": {
                    "reference": f"#{contained_condition_id}",
                    "display": addresses.lower()
                }
            }
        ],
        "goal": goals,
        "activity": activities
    }
    
    # Add encounter reference if provided
    if encounter_id:
        care_plan["encounter"] = {
            "reference": f"Encounter/{encounter_id}"
        }
    
    # Add note if present (80% chance)
    if random.random() < 0.8:
        care_plan["note"] = [
            {
                "text": note
            }
        ]
    
    # Generate text narrative
    goals_text = ", ".join(selected_goals)
    activities_text = ", ".join([a["text"] for a in selected_activities])
    
    care_plan["text"] = {
        "status": "additional",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p>A comprehensive care plan to {description.lower()} for {addresses.lower()}.</p>
            <p><b>Goals:</b> {goals_text}</p>
            <p><b>Activities:</b> {activities_text}</p>
            <p><b>Status:</b> {status}</p>
            <p><b>Intent:</b> {intent}</p>
            <p><b>Period:</b> {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}</p>
        </div>"""
    }
    
    return care_plan
