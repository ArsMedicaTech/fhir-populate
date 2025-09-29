"""
Common clinical impression data for FHIR ClinicalImpression resources.
Includes impression types, findings, and clinical descriptions.
"""

# Clinical impression statuses
CLINICAL_IMPESSION_STATUSES = [
    "in-progress", 
    "completed",
    "entered-in-error"
]

# Common clinical impression descriptions
CLINICAL_IMPESSION_DESCRIPTIONS = [
    "Patient presents with acute onset of symptoms requiring immediate evaluation",
    "Follow-up assessment following recent procedure",
    "Routine clinical evaluation for ongoing condition management",
    "Emergency evaluation following traumatic injury",
    "Comprehensive assessment for diagnostic workup",
    "Post-operative evaluation and monitoring",
    "Chronic condition management and assessment",
    "Pre-operative clinical assessment",
    "Symptom evaluation and differential diagnosis",
    "Treatment response assessment and monitoring",
    "Clinical evaluation for medication management",
    "Comprehensive geriatric assessment",
    "Pediatric developmental assessment",
    "Mental health evaluation and assessment",
    "Cardiovascular risk assessment and evaluation"
]

# Common clinical problems/conditions
CLINICAL_PROBLEMS = [
    "Acute myocardial infarction",
    "Pneumonia",
    "Stroke",
    "Motor vehicle accident",
    "Chest pain",
    "Abdominal pain",
    "Headache",
    "Shortness of breath",
    "Fever",
    "Hypertension",
    "Diabetes mellitus",
    "Chronic obstructive pulmonary disease",
    "Heart failure",
    "Atrial fibrillation",
    "Sepsis",
    "Traumatic brain injury",
    "Fracture",
    "Infection",
    "Dehydration",
    "Anxiety disorder",
    "Depression",
    "Dementia",
    "Cancer",
    "Kidney disease",
    "Liver disease"
]

# Common clinical findings (ICD-9/ICD-10 codes)
# TODO: Verify (or pull using ICD script)...
CLINICAL_FINDINGS = [
    {
        "code": "850.0",
        "display": "Concussion with no loss of consciousness",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "410.01",
        "display": "Acute myocardial infarction, anterior wall, initial episode",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "486",
        "display": "Pneumonia, organism unspecified",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "434.91",
        "display": "Cerebral artery occlusion, unspecified, with cerebral infarction",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "789.00",
        "display": "Abdominal pain, unspecified site",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "784.0",
        "display": "Headache",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "786.05",
        "display": "Shortness of breath",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "780.6",
        "display": "Fever and other physiologic disturbances of temperature regulation",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "401.9",
        "display": "Essential hypertension, unspecified",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "250.00",
        "display": "Diabetes mellitus without mention of complication, type II or unspecified type",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "496",
        "display": "Chronic airway obstruction, not elsewhere classified",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "428.0",
        "display": "Congestive heart failure, unspecified",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "427.31",
        "display": "Atrial fibrillation",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "038.9",
        "display": "Unspecified septicemia",
        "system": "http://hl7.org/fhir/sid/icd-9"
    },
    {
        "code": "850.9",
        "display": "Concussion, unspecified",
        "system": "http://hl7.org/fhir/sid/icd-9"
    }
]

# Common clinical summaries
CLINICAL_SUMMARIES = [
    "Provisional diagnosis of acute condition requiring immediate intervention",
    "Chronic condition management with stable clinical status",
    "Post-procedural evaluation shows good recovery progress",
    "Symptom evaluation suggests need for further diagnostic testing",
    "Treatment response assessment indicates positive clinical improvement",
    "Comprehensive evaluation reveals multiple contributing factors",
    "Clinical assessment supports current treatment plan continuation",
    "Emergency evaluation confirms acute condition requiring hospitalization",
    "Follow-up assessment shows resolution of previous symptoms",
    "Clinical impression suggests need for specialist consultation",
    "Assessment indicates medication adjustment may be beneficial",
    "Evaluation reveals new onset of chronic condition",
    "Clinical findings consistent with expected post-operative course",
    "Assessment suggests need for lifestyle modifications",
    "Evaluation indicates stable condition with ongoing monitoring required"
]

# Investigation types
INVESTIGATION_TYPES = [
    "Initial Examination",
    "Physical Assessment",
    "Neurological Evaluation",
    "Cardiovascular Assessment",
    "Respiratory Examination",
    "Abdominal Examination",
    "Musculoskeletal Evaluation",
    "Mental Status Examination",
    "Vital Signs Assessment",
    "Laboratory Review",
    "Imaging Review",
    "Medication Review",
    "Social History Assessment",
    "Family History Review",
    "Allergy Assessment"
]

# Investigation findings
INVESTIGATION_FINDINGS = [
    "Normal vital signs",
    "Elevated blood pressure",
    "Tachycardia present",
    "Fever noted",
    "Respiratory distress",
    "Chest pain on palpation",
    "Abdominal tenderness",
    "Neurological deficits",
    "Altered mental status",
    "Decreased level of consciousness",
    "Disoriented to time and place",
    "Restless and agitated",
    "Deep laceration noted",
    "Bruising and swelling",
    "Limited range of motion",
    "Abnormal reflexes",
    "Weakness in extremities",
    "Numbness or tingling",
    "Vision changes",
    "Hearing impairment",
    "Speech difficulties",
    "Memory problems",
    "Mood changes",
    "Sleep disturbances",
    "Appetite changes"
]
