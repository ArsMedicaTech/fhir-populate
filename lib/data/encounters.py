"""
Common encounter data for FHIR Encounter resources.
Includes encounter types, classes, statuses, priorities, and reasons.
"""

# Encounter classes (ActCode)
ENCOUNTER_CLASSES = [
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "AMB",
                "display": "ambulatory"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "EMER",
                "display": "emergency"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "IMP",
                "display": "inpatient encounter"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "ACUTE",
                "display": "inpatient acute"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "NONAC",
                "display": "inpatient non-acute"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "PRENC",
                "display": "pre-admission"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "SS",
                "display": "short stay"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "VR",
                "display": "virtual"
            }
        ]
    }
]

# Encounter statuses
ENCOUNTER_STATUSES = [
    "planned",
    "arrived", 
    "triaged",
    "in-progress",
    "onleave",
    "finished",
    "cancelled",
    "entered-in-error",
    "unknown"
]

# Encounter priorities (SNOMED CT)
ENCOUNTER_PRIORITIES = [
    {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "394848005",
                "display": "Normal"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "394849002",
                "display": "High"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "88694003",
                "display": "Immediate"
            }
        ]
    },
]

# Common encounter reasons
ENCOUNTER_REASONS = [
    "Routine follow-up visit",
    "Annual physical examination",
    "Symptom evaluation",
    "Medication management",
    "Lab results review",
    "Blood pressure check",
    "Diabetes management",
    "Chest pain evaluation",
    "Headache assessment",
    "Abdominal pain evaluation",
    "Fever and chills",
    "Cough and congestion",
    "Shortness of breath",
    "Joint pain and stiffness",
    "Skin rash evaluation",
    "Eye examination",
    "Ear pain and hearing issues",
    "Dental consultation",
    "Mental health assessment",
    "Pre-operative evaluation",
    "Post-operative follow-up",
    "Emergency care",
    "Urgent care visit",
    "Specialist consultation",
    "Therapy session",
    "Vaccination appointment",
    "Screening examination",
    "Chronic condition management",
    "Medication adjustment",
    "Side effect evaluation",
    "Allergy assessment",
    "Injury evaluation",
    "Infection treatment",
    "Pain management",
    "Rehabilitation services",
    "Counseling session",
    "Health education",
    "Preventive care",
    "Wellness check",
    "Family planning consultation"
]

# Participant types
PARTICIPANT_TYPES = [
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                "code": "PPRF",
                "display": "primary performer"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                "code": "SPRF",
                "display": "secondary performer"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                "code": "CON",
                "display": "consultant"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                "code": "ATND",
                "display": "attending"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                "code": "RESP",
                "display": "responsible party"
            }
        ]
    }
]
