"""
Common document reference data for FHIR DocumentReference resources.
Includes document types, categories, statuses, and clinical note templates.
"""

# Document types (LOINC codes for clinical notes)
DOCUMENT_TYPES = [
    {
        "code": "11506-3",
        "display": "Progress note",
        "text": "Progress Note",
        "system": "http://loinc.org"
    },
    {
        "code": "18842-5",
        "display": "Discharge summary",
        "text": "Discharge Summary",
        "system": "http://loinc.org"
    },
    {
        "code": "34117-2",
        "display": "History and physical note",
        "text": "History and Physical",
        "system": "http://loinc.org"
    },
    {
        "code": "51848-0",
        "display": "Evaluation and management note",
        "text": "Evaluation and Management Note",
        "system": "http://loinc.org"
    },
    {
        "code": "18726-0",
        "display": "Physician attending progress note",
        "text": "Attending Progress Note",
        "system": "http://loinc.org"
    },
    {
        "code": "11504-8",
        "display": "Consultation note",
        "text": "Consultation Note",
        "system": "http://loinc.org"
    },
    {
        "code": "11505-5",
        "display": "Nursing progress note",
        "text": "Nursing Progress Note",
        "system": "http://loinc.org"
    },
    {
        "code": "11507-1",
        "display": "Procedure note",
        "text": "Procedure Note",
        "system": "http://loinc.org"
    },
    {
        "code": "11508-9",
        "display": "Surgical operation note",
        "text": "Surgical Operation Note",
        "system": "http://loinc.org"
    },
    {
        "code": "51852-2",
        "display": "Emergency department note",
        "text": "Emergency Department Note",
        "system": "http://loinc.org"
    }
]

# Document categories
DOCUMENT_CATEGORIES = [
    {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "LP173837-6",
                "display": "Progress note"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "LP173421-1",
                "display": "Discharge summary"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "LP173422-9",
                "display": "History and physical"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "LP173424-5",
                "display": "Consultation note"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "LP173425-2",
                "display": "Procedure note"
            }
        ]
    }
]

# DocumentReference statuses
DOCUMENT_REFERENCE_STATUSES = [
    "current",
    "superseded",
    "entered-in-error"
]

# Document statuses (CompositionStatus)
DOCUMENT_STATUSES = [
    "preliminary",
    "final",
    "amended",
    "entered-in-error",
    "deprecated"
]

# Attestation modes
ATTESTATION_MODES = [
    {
        "coding": [
            {
                "system": "http://hl7.org/fhir/composition-attestation-mode",
                "code": "personal",
                "display": "Personal"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://hl7.org/fhir/composition-attestation-mode",
                "code": "professional",
                "display": "Professional"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://hl7.org/fhir/composition-attestation-mode",
                "code": "legal",
                "display": "Legal"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://hl7.org/fhir/composition-attestation-mode",
                "code": "official",
                "display": "Official"
            }
        ]
    }
]

# Clinical note templates for generating realistic content
CLINICAL_NOTE_TEMPLATES = {
    "Progress Note": """SUBJECTIVE:
Patient presents for follow-up visit. Reports {chief_complaint}. 
{additional_symptoms}

OBJECTIVE:
Vital Signs: BP {bp_systolic}/{bp_diastolic}, HR {hr}, RR {rr}, Temp {temp}°F, O2 Sat {o2_sat}%
General: {general_appearance}
{physical_exam}

ASSESSMENT:
{assessment}

PLAN:
{plan}""",
    
    "Discharge Summary": """DISCHARGE SUMMARY

ADMISSION DATE: {admission_date}
DISCHARGE DATE: {discharge_date}
ADMITTING DIAGNOSIS: {admitting_diagnosis}
DISCHARGE DIAGNOSIS: {discharge_diagnosis}

HOSPITAL COURSE:
{hospital_course}

DISCHARGE MEDICATIONS:
{discharge_medications}

DISCHARGE INSTRUCTIONS:
{discharge_instructions}

FOLLOW-UP:
{follow_up}""",
    
    "History and Physical": """HISTORY AND PHYSICAL

CHIEF COMPLAINT: {chief_complaint}

HISTORY OF PRESENT ILLNESS:
{history_present_illness}

PAST MEDICAL HISTORY:
{past_medical_history}

PHYSICAL EXAMINATION:
{physical_examination}

ASSESSMENT AND PLAN:
{assessment_plan}""",
    
    "Consultation Note": """CONSULTATION NOTE

REASON FOR CONSULTATION: {reason_for_consultation}

HISTORY:
{history}

PHYSICAL EXAMINATION:
{physical_examination}

ASSESSMENT:
{assessment}

RECOMMENDATIONS:
{recommendations}""",
    
    "Emergency Department Note": """EMERGENCY DEPARTMENT NOTE

CHIEF COMPLAINT: {chief_complaint}

HISTORY OF PRESENT ILLNESS:
{history_present_illness}

PHYSICAL EXAMINATION:
{physical_examination}

ASSESSMENT:
{assessment}

PLAN:
{plan}

DISPOSITION: {disposition}"""
}

