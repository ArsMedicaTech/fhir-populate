"""
Common care plan data for FHIR CarePlan resources.
Includes categories, activities, goals, and care team details.
"""

# Care plan statuses
CARE_PLAN_STATUSES = [
    "draft",
    "active",
    "on-hold",
    "revoked",
    "completed",
    "entered-in-error"
]

# Care plan intents
CARE_PLAN_INTENTS = [
    "proposal",
    "plan",
    "order",
    "option"
]

# Care plan categories
CARE_PLAN_CATEGORIES = [
    {
        "text": "Weight management plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18776-5",
                "display": "Weight management plan"
            }
        ]
    },
    {
        "text": "Diabetes management plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18777-3",
                "display": "Diabetes management plan"
            }
        ]
    },
    {
        "text": "Hypertension management plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18778-1",
                "display": "Hypertension management plan"
            }
        ]
    },
    {
        "text": "Cardiac rehabilitation plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18779-9",
                "display": "Cardiac rehabilitation plan"
            }
        ]
    },
    {
        "text": "Mental health treatment plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18780-7",
                "display": "Mental health treatment plan"
            }
        ]
    },
    {
        "text": "Pain management plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18781-5",
                "display": "Pain management plan"
            }
        ]
    },
    {
        "text": "Physical therapy plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18782-3",
                "display": "Physical therapy plan"
            }
        ]
    },
    {
        "text": "Occupational therapy plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18783-1",
                "display": "Occupational therapy plan"
            }
        ]
    },
    {
        "text": "Speech therapy plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18784-9",
                "display": "Speech therapy plan"
            }
        ]
    },
    {
        "text": "Nutritional therapy plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18785-6",
                "display": "Nutritional therapy plan"
            }
        ]
    },
    {
        "text": "Medication management plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18786-4",
                "display": "Medication management plan"
            }
        ]
    },
    {
        "text": "Fall prevention plan",
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "18787-2",
                "display": "Fall prevention plan"
            }
        ]
    }
]

# Care plan activities (SNOMED CT codes)
# TODO: VERIFY THESE...
CARE_PLAN_ACTIVITIES = [
    {
        "code": "6397004",
        "display": "Muscular strength development exercise",
        "text": "Strength Training",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "229065009",
        "display": "Exercise therapy",
        "text": "Exercise Therapy",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226029000",
        "display": "Walking exercise",
        "text": "Walking",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226030005",
        "display": "Running exercise",
        "text": "Running",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226031009",
        "display": "Swimming exercise",
        "text": "Swimming",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226032002",
        "display": "Cycling exercise",
        "text": "Cycling",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226033007",
        "display": "Aerobic exercise",
        "text": "Aerobic Exercise",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226034001",
        "display": "Flexibility exercise",
        "text": "Stretching",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226035000",
        "display": "Balance exercise",
        "text": "Balance Training",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226036004",
        "display": "Endurance exercise",
        "text": "Endurance Training",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226037008",
        "display": "Coordination exercise",
        "text": "Coordination Training",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226038003",
        "display": "Relaxation exercise",
        "text": "Relaxation Techniques",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226039006",
        "display": "Breathing exercise",
        "text": "Breathing Exercises",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226040008",
        "display": "Posture exercise",
        "text": "Posture Training",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226041007",
        "display": "Range of motion exercise",
        "text": "Range of Motion",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226042000",
        "display": "Gait training",
        "text": "Gait Training",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226043005",
        "display": "Transfer training",
        "text": "Transfer Training",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226044004",
        "display": "Activities of daily living training",
        "text": "ADL Training",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226045003",
        "display": "Cognitive training",
        "text": "Cognitive Training",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "226046002",
        "display": "Speech therapy",
        "text": "Speech Therapy",
        "system": "http://snomed.info/sct"
    }
]

# Care plan goals
CARE_PLAN_GOALS = [
    "Achieve target weight",
    "Maintain blood pressure within normal range",
    "Control blood glucose levels",
    "Improve cardiovascular fitness",
    "Reduce pain levels",
    "Increase mobility and flexibility",
    "Improve balance and coordination",
    "Enhance cognitive function",
    "Improve speech and communication",
    "Increase independence in daily activities",
    "Reduce fall risk",
    "Improve medication adherence",
    "Enhance quality of life",
    "Manage stress and anxiety",
    "Improve sleep quality",
    "Increase energy levels",
    "Reduce inflammation",
    "Improve joint function",
    "Enhance muscle strength",
    "Improve endurance"
]

# Care plan descriptions
CARE_PLAN_DESCRIPTIONS = [
    "Manage obesity and weight loss",
    "Control diabetes and blood sugar levels",
    "Manage hypertension and blood pressure",
    "Improve cardiovascular health",
    "Address mental health concerns",
    "Manage chronic pain",
    "Improve physical function and mobility",
    "Enhance occupational performance",
    "Improve speech and language skills",
    "Optimize nutritional status",
    "Ensure proper medication management",
    "Prevent falls and injuries",
    "Promote overall wellness",
    "Support recovery and rehabilitation",
    "Maintain independence and quality of life"
]

# Care plan addresses (conditions)
CARE_PLAN_ADDRESSES = [
    "Obesity",
    "Type 2 Diabetes",
    "Hypertension",
    "Heart Disease",
    "Depression",
    "Anxiety",
    "Chronic Pain",
    "Arthritis",
    "Stroke",
    "COPD",
    "Asthma",
    "Osteoporosis",
    "Dementia",
    "Parkinson's Disease",
    "Multiple Sclerosis",
    "Cancer",
    "Kidney Disease",
    "Liver Disease",
    "Sleep Apnea",
    "Fibromyalgia"
]

# Care plan based on references
CARE_PLAN_BASED_ON = [
    "Management of Type 2 Diabetes",
    "Hypertension Treatment Protocol",
    "Cardiac Rehabilitation Guidelines",
    "Mental Health Treatment Standards",
    "Pain Management Protocol",
    "Physical Therapy Guidelines",
    "Occupational Therapy Standards",
    "Speech Therapy Protocol",
    "Nutritional Therapy Guidelines",
    "Medication Management Protocol",
    "Fall Prevention Program",
    "Wellness and Prevention Guidelines"
]

# Care plan replaces references
CARE_PLAN_REPLACES = [
    "Plan from urgent care clinic",
    "Previous emergency department plan",
    "Initial assessment plan",
    "Temporary care plan",
    "Interim treatment plan",
    "Preliminary care plan",
    "Draft care plan",
    "Trial care plan",
    "Experimental care plan",
    "Pilot care plan"
]

# Care plan part of references
CARE_PLAN_PART_OF = [
    "Overall wellness plan",
    "Comprehensive treatment plan",
    "Integrated care plan",
    "Multidisciplinary care plan",
    "Coordinated care plan",
    "Patient-centered care plan",
    "Evidence-based care plan",
    "Standardized care plan",
    "Protocol-based care plan",
    "Guideline-based care plan"
]

# Care plan instantiates URIs
CARE_PLAN_INSTANTIATES_URI = [
    "http://example.org/protocol-for-obesity",
    "http://example.org/diabetes-management-protocol",
    "http://example.org/hypertension-treatment-protocol",
    "http://example.org/cardiac-rehabilitation-protocol",
    "http://example.org/mental-health-treatment-protocol",
    "http://example.org/pain-management-protocol",
    "http://example.org/physical-therapy-protocol",
    "http://example.org/occupational-therapy-protocol",
    "http://example.org/speech-therapy-protocol",
    "http://example.org/nutritional-therapy-protocol",
    "http://example.org/medication-management-protocol",
    "http://example.org/fall-prevention-protocol"
]

# Care plan notes
CARE_PLAN_NOTES = [
    "Patient education provided",
    "Family involvement encouraged",
    "Regular follow-up scheduled",
    "Progress monitoring established",
    "Risk factors identified",
    "Barriers to care addressed",
    "Resources provided",
    "Support system activated",
    "Goals reviewed and updated",
    "Interventions adjusted as needed",
    "Patient preferences considered",
    "Cultural factors incorporated",
    "Language barriers addressed",
    "Accessibility needs met",
    "Safety measures implemented"
]

# Care plan activity details
CARE_PLAN_ACTIVITY_DETAILS = [
    {
        "kind": "Appointment",
        "code": "appointment",
        "display": "Schedule regular appointments"
    },
    {
        "kind": "CommunicationRequest",
        "code": "communication",
        "display": "Patient communication"
    },
    {
        "kind": "DeviceRequest",
        "code": "device",
        "display": "Medical device request"
    },
    {
        "kind": "MedicationRequest",
        "code": "medication",
        "display": "Medication prescription"
    },
    {
        "kind": "NutritionOrder",
        "code": "nutrition",
        "display": "Nutritional therapy order"
    },
    {
        "kind": "ServiceRequest",
        "code": "service",
        "display": "Healthcare service request"
    },
    {
        "kind": "Task",
        "code": "task",
        "display": "Care task assignment"
    },
    {
        "kind": "VisionPrescription",
        "code": "vision",
        "display": "Vision care prescription"
    }
]

# Care plan activity status
CARE_PLAN_ACTIVITY_STATUS = [
    "not-started",
    "scheduled",
    "in-progress",
    "on-hold",
    "completed",
    "cancelled",
    "stopped",
    "unknown",
    "entered-in-error"
]

# Care plan activity outcome
CARE_PLAN_ACTIVITY_OUTCOME = [
    "successful",
    "partially-successful",
    "unsuccessful",
    "cancelled",
    "stopped",
    "unknown"
]
