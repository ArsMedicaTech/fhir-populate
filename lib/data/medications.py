"""
Common medications for FHIR MedicationRequest resources.
Includes medication names, dosages, routes, and timing information.
"""

MEDICATIONS = [
    {
        "name": "FONDAPARINUX 2.5 MG/0.5 ML SC SYRG",
        "text": "Fondaparinux 2.5mg subcutaneous injection",
        "dosage": {
            "value": 2.5,
            "unit": "mg"
        },
        "route": "Subcutaneous",
        "timing": "DAILY"
    },
    {
        "name": "METFORMIN 500 MG TAB",
        "text": "Metformin 500mg tablet",
        "dosage": {
            "value": 500,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "TWICE DAILY"
    },
    {
        "name": "LISINOPRIL 10 MG TAB",
        "text": "Lisinopril 10mg tablet",
        "dosage": {
            "value": 10,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "ATORVASTATIN 20 MG TAB",
        "text": "Atorvastatin 20mg tablet",
        "dosage": {
            "value": 20,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "OMEPRAZOLE 20 MG CAP",
        "text": "Omeprazole 20mg capsule",
        "dosage": {
            "value": 20,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "AMLODIPINE 5 MG TAB",
        "text": "Amlodipine 5mg tablet",
        "dosage": {
            "value": 5,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "LEVOTHYROXINE 50 MCG TAB",
        "text": "Levothyroxine 50mcg tablet",
        "dosage": {
            "value": 50,
            "unit": "mcg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "SERTRALINE 50 MG TAB",
        "text": "Sertraline 50mg tablet",
        "dosage": {
            "value": 50,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "WARFARIN 5 MG TAB",
        "text": "Warfarin 5mg tablet",
        "dosage": {
            "value": 5,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "FUROSEMIDE 40 MG TAB",
        "text": "Furosemide 40mg tablet",
        "dosage": {
            "value": 40,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "PREDNISONE 20 MG TAB",
        "text": "Prednisone 20mg tablet",
        "dosage": {
            "value": 20,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "ALBUTEROL 90 MCG INH",
        "text": "Albuterol 90mcg inhaler",
        "dosage": {
            "value": 90,
            "unit": "mcg"
        },
        "route": "Inhalation",
        "timing": "AS NEEDED"
    },
    {
        "name": "INSULIN GLARGINE 100 UNITS/ML",
        "text": "Insulin glargine 100 units/mL",
        "dosage": {
            "value": 20,
            "unit": "units"
        },
        "route": "Subcutaneous",
        "timing": "DAILY"
    },
    {
        "name": "MORPHINE 10 MG TAB",
        "text": "Morphine 10mg tablet",
        "dosage": {
            "value": 10,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "EVERY 4 HOURS"
    },
    {
        "name": "DIGOXIN 0.25 MG TAB",
        "text": "Digoxin 0.25mg tablet",
        "dosage": {
            "value": 0.25,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "DAILY"
    },
    {
        "name": "CIPROFLOXACIN 500 MG TAB",
        "text": "Ciprofloxacin 500mg tablet",
        "dosage": {
            "value": 500,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "TWICE DAILY"
    },
    {
        "name": "ACETAMINOPHEN 500 MG TAB",
        "text": "Acetaminophen 500mg tablet",
        "dosage": {
            "value": 500,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "EVERY 6 HOURS"
    },
    {
        "name": "IBUPROFEN 400 MG TAB",
        "text": "Ibuprofen 400mg tablet",
        "dosage": {
            "value": 400,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "EVERY 8 HOURS"
    },
    {
        "name": "LORAZEPAM 1 MG TAB",
        "text": "Lorazepam 1mg tablet",
        "dosage": {
            "value": 1,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "AS NEEDED"
    },
    {
        "name": "DIPHENHYDRAMINE 25 MG TAB",
        "text": "Diphenhydramine 25mg tablet",
        "dosage": {
            "value": 25,
            "unit": "mg"
        },
        "route": "Oral",
        "timing": "EVERY 6 HOURS"
    }
]

# Common medication request statuses
MEDICATION_STATUSES = ["active", "completed", "cancelled", "stopped", "draft"]

# Common medication request intents
MEDICATION_INTENTS = ["order", "plan", "proposal", "original-order", "reflex-order", "filler-order", "instance-order"]
