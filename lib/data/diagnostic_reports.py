"""
Common diagnostic report types and categories for FHIR DiagnosticReport resources.
Includes LOINC codes for various laboratory and imaging reports.
"""

# Common diagnostic report types
DIAGNOSTIC_REPORT_TYPES = [
    {
        "code": "58410-2",
        "display": "Complete blood count (hemogram) panel - Blood by Automated count",
        "text": "Complete Blood Count",
        "system": "http://loinc.org",
        "category": "laboratory"
    },
    {
        "code": "24356-8",
        "display": "Comprehensive metabolic panel - Serum or Plasma",
        "text": "Comprehensive Metabolic Panel",
        "system": "http://loinc.org",
        "category": "laboratory"
    },
    {
        "code": "24323-8",
        "display": "Lipid panel - Serum or Plasma",
        "text": "Lipid Panel",
        "system": "http://loinc.org",
        "category": "laboratory"
    },
    {
        "code": "11502-2",
        "display": "Laboratory report",
        "text": "Laboratory Report",
        "system": "http://loinc.org",
        "category": "laboratory"
    },
    {
        "code": "18748-4",
        "display": "Diagnostic imaging study",
        "text": "Diagnostic Imaging Study",
        "system": "http://loinc.org",
        "category": "imaging"
    },
    {
        "code": "11526-1",
        "display": "Pathology report",
        "text": "Pathology Report",
        "system": "http://loinc.org",
        "category": "pathology"
    }
]

# Common diagnostic report statuses
DIAGNOSTIC_REPORT_STATUSES = ["registered", "partial", "preliminary", "final", "amended", "corrected", "cancelled", "entered-in-error", "unknown"]

# Common diagnostic report categories
DIAGNOSTIC_REPORT_CATEGORIES = [
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                "code": "LAB",
                "display": "Laboratory"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                "code": "HM",
                "display": "Hematology"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                "code": "RAD",
                "display": "Radiology"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                "code": "PAT",
                "display": "Pathology"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                "code": "SP",
                "display": "Surgical Pathology"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                "code": "CH",
                "display": "Chemistry"
            }
        ]
    }
]

# Common laboratory names
LABORATORY_NAMES = [
    "Acme Laboratory, Inc",
    "Metro Health Laboratory",
    "Central Medical Lab",
    "Premier Diagnostic Services",
    "Advanced Clinical Labs",
    "Regional Medical Laboratory",
    "City Health Lab Services",
    "Professional Diagnostic Center"
]

# Common pathologist names
PATHOLOGIST_NAMES = [
    "Dr. Pete Pathologist",
    "Dr. Sarah Smith",
    "Dr. Michael Johnson",
    "Dr. Emily Davis",
    "Dr. Robert Wilson",
    "Dr. Lisa Anderson",
    "Dr. David Brown",
    "Dr. Jennifer Taylor"
]
