"""
Common service request types and data for FHIR ServiceRequest resources.
Includes LOINC codes for various medical services and procedures.
"""

# Common service request types
# TODO: VERIFY THESE (OR PULL FROM LOINC SCRIPT)
SERVICE_REQUEST_TYPES = [
    {
        "code": "24627-2",
        "display": "Chest CT",
        "text": "Chest CT",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24620-7",
        "display": "Chest X-ray",
        "text": "Chest X-ray",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24623-1",
        "display": "CT of abdomen and pelvis",
        "text": "CT Abdomen and Pelvis",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24624-9",
        "display": "CT of head",
        "text": "CT Head",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24625-6",
        "display": "CT of spine",
        "text": "CT Spine",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24626-4",
        "display": "MRI of brain",
        "text": "MRI Brain",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24627-2",
        "display": "MRI of chest",
        "text": "MRI Chest",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24628-0",
        "display": "MRI of spine",
        "text": "MRI Spine",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24629-8",
        "display": "Ultrasound of abdomen",
        "text": "Ultrasound Abdomen",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24630-6",
        "display": "Ultrasound of heart",
        "text": "Echocardiogram",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24631-4",
        "display": "Ultrasound of pelvis",
        "text": "Ultrasound Pelvis",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24632-2",
        "display": "Mammography",
        "text": "Mammography",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24633-0",
        "display": "Bone density scan",
        "text": "Bone Density Scan",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24634-8",
        "display": "Nuclear medicine scan",
        "text": "Nuclear Medicine Scan",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24635-5",
        "display": "PET scan",
        "text": "PET Scan",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "24636-3",
        "display": "Cardiac stress test",
        "text": "Cardiac Stress Test",
        "system": "http://loinc.org",
        "category": "cardiology"
    },
    {
        "code": "24637-1",
        "display": "Electrocardiogram",
        "text": "ECG",
        "system": "http://loinc.org",
        "category": "cardiology"
    },
    {
        "code": "24638-9",
        "display": "Holter monitor",
        "text": "Holter Monitor",
        "system": "http://loinc.org",
        "category": "cardiology"
    },
    {
        "code": "24639-7",
        "display": "Pulmonary function test",
        "text": "Pulmonary Function Test",
        "system": "http://loinc.org",
        "category": "pulmonology"
    },
    {
        "code": "24640-5",
        "display": "Sleep study",
        "text": "Sleep Study",
        "system": "http://loinc.org",
        "category": "pulmonology"
    }
]

# Service request statuses
SERVICE_REQUEST_STATUSES = [
    "draft",
    "active", 
    "on-hold",
    "revoked",
    "completed",
    "entered-in-error",
    "unknown"
]

# Service request intents
SERVICE_REQUEST_INTENTS = [
    "proposal",
    "plan",
    "directive",
    "order",
    "original-order",
    "reflex-order",
    "filler-order",
    "instance-order",
    "option"
]

# Service request priorities
SERVICE_REQUEST_PRIORITIES = [
    "routine",
    "urgent",
    "asap",
    "stat"
]

# Common reasons for service requests
SERVICE_REQUEST_REASONS = [
    "Check for metastatic disease",
    "Evaluate chest pain",
    "Assess abdominal pain",
    "Monitor treatment response",
    "Routine screening",
    "Follow-up examination",
    "Pre-operative assessment",
    "Post-operative monitoring",
    "Evaluate symptoms",
    "Diagnostic workup",
    "Staging evaluation",
    "Treatment planning",
    "Emergency evaluation",
    "Routine surveillance",
    "Baseline assessment"
]

# Body site codes for service requests
# TODO: VERIFY THESE (OR PULL FROM SNOMED SCRIPT)
BODY_SITE_CODES = [
    {
        "code": "51185008",
        "display": "Thoracic structure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "113197003",
        "display": "Abdomen",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "12611008",
        "display": "Head",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "421060004",
        "display": "Spine",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "302551006",
        "display": "Pelvis",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "80248007",
        "display": "Heart",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "39607008",
        "display": "Lung",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "76752008",
        "display": "Breast",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "71341001",
        "display": "Brain",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "244466001",
        "display": "Extremity",
        "system": "http://snomed.info/sct"
    }
]
