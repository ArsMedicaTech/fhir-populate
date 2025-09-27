"""
Common laboratory observations for FHIR Observation resources.
Includes LOINC codes, normal ranges, units, and interpretations.
"""

OBSERVATIONS = [
    {
        "code": "33747-0",
        "display": "BNP",
        "text": "BNP",
        "system": "http://loinc.org",
        "category": "laboratory",
        "unit": "pg/mL",
        "unit_system": "http://unitsofmeasure.org",
        "unit_code": "pg/mL",
        "normal_range": {"low": 0, "high": 100},
        "interpretations": {
            "LOW": {"low": 0, "high": 0},
            "NORMAL": {"low": 1, "high": 100},
            "HIGH": {"low": 101, "high": 1000}
        }
    },
    {
        "code": "33747-0",
        "display": "Hemoglobin A1c",
        "text": "Hemoglobin A1c",
        "system": "http://loinc.org",
        "category": "laboratory",
        "unit": "%",
        "unit_system": "http://unitsofmeasure.org",
        "unit_code": "%",
        "normal_range": {"low": 4.0, "high": 5.6},
        "interpretations": {
            "LOW": {"low": 0, "high": 3.9},
            "NORMAL": {"low": 4.0, "high": 5.6},
            "HIGH": {"low": 5.7, "high": 15.0}
        }
    },
    {
        "code": "33747-0",
        "display": "Glucose",
        "text": "Glucose",
        "system": "http://loinc.org",
        "category": "laboratory",
        "unit": "mg/dL",
        "unit_system": "http://unitsofmeasure.org",
        "unit_code": "mg/dL",
        "normal_range": {"low": 70, "high": 100},
        "interpretations": {
            "LOW": {"low": 0, "high": 69},
            "NORMAL": {"low": 70, "high": 100},
            "HIGH": {"low": 101, "high": 500}
        }
    },

]

# Common observation statuses
OBSERVATION_STATUSES = ["registered", "preliminary", "final", "amended", "cancelled", "entered-in-error", "unknown"]

# Common observation categories
OBSERVATION_CATEGORIES = [
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "laboratory",
                "display": "Laboratory"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "vital-signs",
                "display": "Vital Signs"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "imaging",
                "display": "Imaging"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "social-history",
                "display": "Social History"
            }
        ]
    }
]

# Interpretation codes
INTERPRETATION_CODES = {
    "LOW": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
        "code": "L",
        "display": "Low"
    },
    "NORMAL": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
        "code": "N",
        "display": "Normal"
    },
    "HIGH": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
        "code": "H",
        "display": "High"
    }
}
