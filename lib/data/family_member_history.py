"""
Common family member history data for FHIR FamilyMemberHistory resources.
Includes relationships, conditions, and participant types.
"""

# Family member history statuses
FAMILY_MEMBER_STATUSES = [
    "partial",
    "completed",
    "entered-in-error",
    "health-unknown"
]

# Family relationships
FAMILY_RELATIONSHIPS = [
    {
        "code": "FTH",
        "display": "father",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "MTH",
        "display": "mother",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "BRO",
        "display": "brother",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "SIS",
        "display": "sister",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "GRFTH",
        "display": "grandfather",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "GRMTH",
        "display": "grandmother",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "UNCLE",
        "display": "uncle",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "AUNT",
        "display": "aunt",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "COUSN",
        "display": "cousin",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "NEPHEW",
        "display": "nephew",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    },
    {
        "code": "NIECE",
        "display": "niece",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
    }
]

# Administrative genders
ADMINISTRATIVE_GENDERS = [
    {
        "code": "male",
        "display": "Male",
        "system": "http://hl7.org/fhir/administrative-gender"
    },
    {
        "code": "female",
        "display": "Female",
        "system": "http://hl7.org/fhir/administrative-gender"
    },
    {
        "code": "other",
        "display": "Other",
        "system": "http://hl7.org/fhir/administrative-gender"
    },
    {
        "code": "unknown",
        "display": "Unknown",
        "system": "http://hl7.org/fhir/administrative-gender"
    }
]


# TODO: Verify these (or pull using SNOMED script)...

# Common family member conditions
FAMILY_CONDITIONS = [
    {
        "code": "315619001",
        "display": "Myocardial Infarction",
        "text": "Heart Attack",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "44054006",
        "display": "Diabetes mellitus",
        "text": "Diabetes",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "38341003",
        "display": "Hypertensive disorder, systemic arterial",
        "text": "High Blood Pressure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "363358000",
        "display": "Malignant neoplastic disease",
        "text": "Cancer",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "195967001",
        "display": "Asthma",
        "text": "Asthma",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "13645005",
        "display": "Congestive heart failure",
        "text": "Heart Failure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "230690007",
        "display": "Stroke",
        "text": "Stroke",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "267036007",
        "display": "Dyslipidemia",
        "text": "High Cholesterol",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "35489007",
        "display": "Depressive disorder",
        "text": "Depression",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "268620009",
        "display": "Anxiety disorder",
        "text": "Anxiety",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "26929004",
        "display": "Alzheimer disease",
        "text": "Alzheimer's Disease",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "195967001",
        "display": "Chronic obstructive pulmonary disease",
        "text": "COPD",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "237602007",
        "display": "Chronic kidney disease",
        "text": "Kidney Disease",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "235719002",
        "display": "Liver disease",
        "text": "Liver Disease",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "254837009",
        "display": "Osteoporosis",
        "text": "Osteoporosis",
        "system": "http://snomed.info/sct"
    }
]

# Participant function types
PARTICIPANT_FUNCTIONS = [
    {
        "code": "verifier",
        "display": "Verifier",
        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type"
    },
    {
        "code": "author",
        "display": "Author",
        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type"
    },
    {
        "code": "informant",
        "display": "Informant",
        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type"
    }
]

# Common notes for family member conditions
FAMILY_CONDITION_NOTES = [
    "Diagnosed in early 60s",
    "Developed after retirement",
    "Family history of this condition",
    "Managed well with medication",
    "Required surgery",
    "Passed away from complications",
    "Still living with condition",
    "Diagnosed at young age",
    "Multiple family members affected",
    "No known family history",
    "Condition was well-controlled",
    "Led to other health problems",
    "Diagnosed during routine screening",
    "Symptoms appeared suddenly",
    "Gradual onset over years"
]

# Age ranges for different family members
AGE_RANGES = {
    "FTH": (45, 85),  # Father
    "MTH": (40, 85),  # Mother
    "BRO": (20, 70),  # Brother
    "SIS": (20, 70),  # Sister
    "GRFTH": (65, 95),  # Grandfather
    "GRMTH": (65, 95),  # Grandmother
    "UNCLE": (30, 80),  # Uncle
    "AUNT": (30, 80),   # Aunt
    "COUSN": (15, 60),  # Cousin
    "NEPHEW": (5, 40),  # Nephew
    "NIECE": (5, 40)    # Niece
}

# Common causes of death
CAUSES_OF_DEATH = [
    "Heart attack",
    "Cancer",
    "Stroke",
    "Heart failure",
    "Pneumonia",
    "Kidney failure",
    "Liver disease",
    "Alzheimer's disease",
    "Accident",
    "Natural causes",
    "Unknown"
]
