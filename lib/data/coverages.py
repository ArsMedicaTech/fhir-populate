"""
Common coverage data for FHIR Coverage resources.
Includes insurance types, classes, and coverage details.
"""

# Coverage statuses
COVERAGE_STATUSES = [
    "active",
    "cancelled",
    "draft",
    "entered-in-error"
]

# Coverage kinds
COVERAGE_KINDS = [
    "insurance",
    "cash",
    "benefit"
]

# Coverage types (HL7 v3 ActCode)
# TODO: VERIFY THESE...
COVERAGE_TYPES = [
    {
        "code": "EHCPOL",
        "display": "extended healthcare",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    },
    {
        "code": "HS",
        "display": "health service",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    },
    {
        "code": "DENTAL",
        "display": "dental",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    },
    {
        "code": "VISION",
        "display": "vision",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    },
    {
        "code": "DRUG",
        "display": "drug",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    },
    {
        "code": "MED",
        "display": "medical",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    },
    {
        "code": "HOSP",
        "display": "hospital",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    },
    {
        "code": "LTC",
        "display": "long term care",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    },
    {
        "code": "DIS",
        "display": "disability",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    },
    {
        "code": "LIFE",
        "display": "life",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    }
]

# Coverage relationships
COVERAGE_RELATIONSHIPS = [
    {
        "code": "self",
        "display": "Self",
        "system": "http://terminology.hl7.org/CodeSystem/subscriber-relationship"
    },
    {
        "code": "spouse",
        "display": "Spouse",
        "system": "http://terminology.hl7.org/CodeSystem/subscriber-relationship"
    },
    {
        "code": "child",
        "display": "Child",
        "system": "http://terminology.hl7.org/CodeSystem/subscriber-relationship"
    },
    {
        "code": "other",
        "display": "Other",
        "system": "http://terminology.hl7.org/CodeSystem/subscriber-relationship"
    }
]

# Coverage class types
COVERAGE_CLASS_TYPES = [
    {
        "code": "group",
        "display": "Group",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "subgroup",
        "display": "Subgroup",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "plan",
        "display": "Plan",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "subplan",
        "display": "Subplan",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "class",
        "display": "Class",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "subclass",
        "display": "Subclass",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "sequence",
        "display": "Sequence",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "rxid",
        "display": "Rx ID",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "rxbin",
        "display": "Rx BIN",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "rxgroup",
        "display": "Rx Group",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    },
    {
        "code": "rxpcn",
        "display": "Rx PCN",
        "system": "http://terminology.hl7.org/CodeSystem/coverage-class"
    }
]

# Insurance companies
INSURANCE_COMPANIES = [
    {
        "name": "Blue Cross Blue Shield",
        "code": "BCBS",
        "display": "Blue Cross Blue Shield"
    },
    {
        "name": "Aetna",
        "code": "AETNA",
        "display": "Aetna Inc."
    },
    {
        "name": "Cigna",
        "code": "CIGNA",
        "display": "Cigna Corporation"
    },
    {
        "name": "UnitedHealth Group",
        "code": "UHC",
        "display": "UnitedHealth Group"
    },
    {
        "name": "Humana",
        "code": "HUMANA",
        "display": "Humana Inc."
    },
    {
        "name": "Kaiser Permanente",
        "code": "KP",
        "display": "Kaiser Permanente"
    },
    {
        "name": "Anthem",
        "code": "ANTHEM",
        "display": "Anthem Inc."
    },
    {
        "name": "Molina Healthcare",
        "code": "MOLINA",
        "display": "Molina Healthcare"
    },
    {
        "name": "Centene Corporation",
        "code": "CENTENE",
        "display": "Centene Corporation"
    },
    {
        "name": "WellCare Health Plans",
        "code": "WELLCARE",
        "display": "WellCare Health Plans"
    }
]

# Coverage plan names
COVERAGE_PLAN_NAMES = [
    "Basic Health Plan",
    "Standard Health Plan",
    "Premium Health Plan",
    "Family Health Plan",
    "Individual Health Plan",
    "Employee Health Plan",
    "Student Health Plan",
    "Senior Health Plan",
    "Medicare Advantage Plan",
    "Medicaid Plan",
    "HMO Plan",
    "PPO Plan",
    "EPO Plan",
    "POS Plan",
    "HDHP Plan",
    "Catastrophic Plan",
    "Short-term Plan",
    "Supplemental Plan",
    "Dental Plan",
    "Vision Plan",
    "Prescription Plan",
    "Mental Health Plan",
    "Maternity Plan",
    "Pediatric Plan",
    "Geriatric Plan"
]

# Coverage class names
COVERAGE_CLASS_NAMES = [
    "Corporate Benefits",
    "Individual Benefits",
    "Family Benefits",
    "Employee Benefits",
    "Student Benefits",
    "Senior Benefits",
    "Medicare Benefits",
    "Medicaid Benefits",
    "Group Benefits",
    "Union Benefits",
    "Professional Benefits",
    "Association Benefits",
    "Government Benefits",
    "Military Benefits",
    "Retiree Benefits",
    "Part-time Benefits",
    "Full-time Benefits",
    "Temporary Benefits",
    "Contractor Benefits",
    "Volunteer Benefits"
]

# Coverage tier names
COVERAGE_TIER_NAMES = [
    "Bronze",
    "Silver",
    "Gold",
    "Platinum",
    "Basic",
    "Standard",
    "Premium",
    "Elite",
    "Essential",
    "Comprehensive",
    "Limited",
    "Extended",
    "Full Coverage",
    "Partial Coverage",
    "Supplemental Coverage"
]

# Coverage subclass names
COVERAGE_SUBCLASS_NAMES = [
    "Low deductible",
    "High deductible",
    "No deductible",
    "Copay plan",
    "Coinsurance plan",
    "HSA eligible",
    "FSA eligible",
    "Network only",
    "Out of network",
    "Preferred provider",
    "Non-preferred provider",
    "Emergency only",
    "Urgent care only",
    "Primary care only",
    "Specialist only"
]

# Coverage identifiers
COVERAGE_IDENTIFIERS = [
    {
        "system": "http://benefitsinc.com/certificate",
        "value_prefix": "CERT"
    },
    {
        "system": "http://insurance.com/policy",
        "value_prefix": "POL"
    },
    {
        "system": "http://healthplan.com/member",
        "value_prefix": "MEM"
    },
    {
        "system": "http://coverage.com/group",
        "value_prefix": "GRP"
    },
    {
        "system": "http://benefits.com/subscriber",
        "value_prefix": "SUB"
    },
    {
        "system": "http://plan.com/enrollment",
        "value_prefix": "ENR"
    },
    {
        "system": "http://coverage.com/account",
        "value_prefix": "ACC"
    },
    {
        "system": "http://insurance.com/contract",
        "value_prefix": "CON"
    }
]

# Coverage cost sharing
COVERAGE_COST_SHARING = [
    {
        "type": "copay",
        "display": "Copay",
        "amount": 20
    },
    {
        "type": "copay",
        "display": "Copay",
        "amount": 25
    },
    {
        "type": "copay",
        "display": "Copay",
        "amount": 30
    },
    {
        "type": "copay",
        "display": "Copay",
        "amount": 50
    },
    {
        "type": "copay",
        "display": "Copay",
        "amount": 75
    },
    {
        "type": "copay",
        "display": "Copay",
        "amount": 100
    },
    {
        "type": "coinsurance",
        "display": "Coinsurance",
        "percentage": 10
    },
    {
        "type": "coinsurance",
        "display": "Coinsurance",
        "percentage": 20
    },
    {
        "type": "coinsurance",
        "display": "Coinsurance",
        "percentage": 30
    },
    {
        "type": "deductible",
        "display": "Deductible",
        "amount": 500
    },
    {
        "type": "deductible",
        "display": "Deductible",
        "amount": 1000
    },
    {
        "type": "deductible",
        "display": "Deductible",
        "amount": 1500
    },
    {
        "type": "deductible",
        "display": "Deductible",
        "amount": 2000
    },
    {
        "type": "deductible",
        "display": "Deductible",
        "amount": 3000
    },
    {
        "type": "deductible",
        "display": "Deductible",
        "amount": 5000
    }
]

# Coverage network types
COVERAGE_NETWORK_TYPES = [
    "HMO",
    "PPO",
    "EPO",
    "POS",
    "HDHP",
    "Indemnity",
    "Point of Service",
    "Preferred Provider",
    "Exclusive Provider",
    "Health Maintenance Organization"
]

# Coverage benefit types
COVERAGE_BENEFIT_TYPES = [
    "Medical",
    "Dental",
    "Vision",
    "Pharmacy",
    "Mental Health",
    "Behavioral Health",
    "Substance Abuse",
    "Maternity",
    "Pediatric",
    "Geriatric",
    "Emergency",
    "Urgent Care",
    "Primary Care",
    "Specialist Care",
    "Preventive Care",
    "Wellness",
    "Rehabilitation",
    "Physical Therapy",
    "Occupational Therapy",
    "Speech Therapy"
]
