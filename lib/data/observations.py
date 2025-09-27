"""
Common laboratory observations for FHIR Observation resources.
Generated from official LOINC database.
Includes LOINC codes, normal ranges, units, and interpretations.
"""

OBSERVATIONS = [
    {
        "code": "13945-1",
        "display": "Erythrocytes [#/area] in Urine sediment by Microscopy high power field",
        "text": "RBC #/area UrnS HPF",
        "system": "http://loinc.org",
        "category": "laboratory",
        "unit": "/HPF",
        "unit_system": "http://unitsofmeasure.org",
        "unit_code": "/HPF",
        "normal_range": {'low': 0, 'high': 100},
        "interpretations": {'LOW': {'low': 0, 'high': 0}, 'NORMAL': {'low': 1, 'high': 100}, 'HIGH': {'low': 101, 'high': 1000}}
    },
    {
        "code": "5821-4",
        "display": "Leukocytes [#/area] in Urine sediment by Microscopy high power field",
        "text": "WBC #/area UrnS HPF",
        "system": "http://loinc.org",
        "category": "laboratory",
        "unit": "/HPF",
        "unit_system": "http://unitsofmeasure.org",
        "unit_code": "/HPF",
        "normal_range": {'low': 3.5, 'high': 5.0},
        "interpretations": {'LOW': {'low': 2.0, 'high': 3.4}, 'NORMAL': {'low': 3.5, 'high': 5.0}, 'HIGH': {'low': 5.1, 'high': 8.0}}
    },
    {
        "code": "2161-8",
        "display": "Creatinine [Mass/volume] in Urine",
        "text": "Creat Ur-mCnc",
        "system": "http://loinc.org",
        "category": "laboratory",
        "unit": "mg/dL",
        "unit_system": "http://unitsofmeasure.org",
        "unit_code": "mg/dL",
        "normal_range": {'low': 0.6, 'high': 1.2},
        "interpretations": {'LOW': {'low': 0.0, 'high': 0.5}, 'NORMAL': {'low': 0.6, 'high': 1.2}, 'HIGH': {'low': 1.3, 'high': 2.4}}
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
