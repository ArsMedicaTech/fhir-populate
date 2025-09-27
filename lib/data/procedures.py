"""
Common medical procedures for FHIR Procedure resources.
Includes CPT codes, procedure names, and descriptions.
"""

PROCEDURES = [
    {
        "code": "ECH15",
        "display": "Echo - Transthoracic Echo +Doppler",
        "text": "Echo - Transthoracic Echo +Doppler",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99213",
        "display": "Office or other outpatient visit for the evaluation and management of an established patient",
        "text": "Office visit - established patient",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99214",
        "display": "Office or other outpatient visit for the evaluation and management of an established patient",
        "text": "Office visit - established patient (detailed)",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99215",
        "display": "Office or other outpatient visit for the evaluation and management of an established patient",
        "text": "Office visit - established patient (comprehensive)",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99202",
        "display": "Office or other outpatient visit for the evaluation and management of a new patient",
        "text": "Office visit - new patient",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "36415",
        "display": "Collection of venous blood by venipuncture",
        "text": "Blood draw - venipuncture",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "93000",
        "display": "Electrocardiogram, routine ECG with at least 12 leads",
        "text": "Electrocardiogram (ECG)",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "71020",
        "display": "Radiologic examination, chest, 2 views, frontal and lateral",
        "text": "Chest X-ray - 2 views",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "73060",
        "display": "Radiologic examination; knee, 2 or 3 views",
        "text": "Knee X-ray - 2-3 views",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "73070",
        "display": "Radiologic examination; elbow, 2 or 3 views",
        "text": "Elbow X-ray - 2-3 views",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "76700",
        "display": "Abdominal ultrasound, complete",
        "text": "Abdominal ultrasound",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "76705",
        "display": "Abdominal ultrasound, limited",
        "text": "Abdominal ultrasound - limited",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "76770",
        "display": "Retroperitoneal ultrasound, complete",
        "text": "Retroperitoneal ultrasound",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "80053",
        "display": "Comprehensive metabolic panel",
        "text": "Comprehensive metabolic panel",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "80061",
        "display": "Lipid panel",
        "text": "Lipid panel",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "85025",
        "display": "Blood count; complete (CBC), automated (Hgb, Hct, RBC, WBC and platelet count)",
        "text": "Complete blood count (CBC)",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "85610",
        "display": "Prothrombin time",
        "text": "Prothrombin time (PT)",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "85730",
        "display": "Thromboplastin time, partial (PTT); plasma or whole blood",
        "text": "Partial thromboplastin time (PTT)",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "93015",
        "display": "Cardiovascular stress test using maximal or submaximal treadmill or bicycle exercise",
        "text": "Cardiovascular stress test",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "93016",
        "display": "Cardiovascular stress test using maximal or submaximal treadmill or bicycle exercise",
        "text": "Cardiovascular stress test with monitoring",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "93017",
        "display": "Cardiovascular stress test using maximal or submaximal treadmill or bicycle exercise",
        "text": "Cardiovascular stress test with interpretation",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "93040",
        "display": "Rhythm ECG, 1-3 leads; with interpretation and report",
        "text": "Rhythm ECG with interpretation",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "93041",
        "display": "Rhythm ECG, 1-3 leads; tracing only, without interpretation and report",
        "text": "Rhythm ECG - tracing only",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "93042",
        "display": "Rhythm ECG, 1-3 leads; interpretation and report only",
        "text": "Rhythm ECG - interpretation only",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "94010",
        "display": "Spirometry, including graphic record, total and timed vital capacity",
        "text": "Spirometry",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "94060",
        "display": "Bronchodilation responsiveness, spirometry as in 94010, pre- and post-bronchodilator administration",
        "text": "Bronchodilation responsiveness test",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "94640",
        "display": "Pressurized or nonpressurized inhalation treatment for acute airway obstruction",
        "text": "Inhalation treatment for airway obstruction",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "94664",
        "display": "Demonstration and/or evaluation of patient utilization of an aerosol generator",
        "text": "Aerosol generator demonstration",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99281",
        "display": "Emergency department visit for the evaluation and management of a patient",
        "text": "Emergency department visit - level 1",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99282",
        "display": "Emergency department visit for the evaluation and management of a patient",
        "text": "Emergency department visit - level 2",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99283",
        "display": "Emergency department visit for the evaluation and management of a patient",
        "text": "Emergency department visit - level 3",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99284",
        "display": "Emergency department visit for the evaluation and management of a patient",
        "text": "Emergency department visit - level 4",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99285",
        "display": "Emergency department visit for the evaluation and management of a patient",
        "text": "Emergency department visit - level 5",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99291",
        "display": "Critical care, evaluation and management of the critically ill or critically injured patient",
        "text": "Critical care - first 30-74 minutes",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99292",
        "display": "Critical care, evaluation and management of the critically ill or critically injured patient",
        "text": "Critical care - each additional 30 minutes",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99444",
        "display": "Online evaluation and management service provided by a physician or other qualified health care professional",
        "text": "Online evaluation and management service",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99446",
        "display": "Interprofessional telephone/Internet/electronic health record assessment and management service",
        "text": "Interprofessional telephone assessment",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99447",
        "display": "Interprofessional telephone/Internet/electronic health record assessment and management service",
        "text": "Interprofessional telephone assessment - additional 15 minutes",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99448",
        "display": "Interprofessional telephone/Internet/electronic health record assessment and management service",
        "text": "Interprofessional telephone assessment - additional 15 minutes",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99449",
        "display": "Interprofessional telephone/Internet/electronic health record assessment and management service",
        "text": "Interprofessional telephone assessment - additional 15 minutes",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99495",
        "display": "Transitional care management services with moderate medical decision complexity",
        "text": "Transitional care management - moderate complexity",
        "system": "http://www.ama-assn.org/go/cpt"
    },
    {
        "code": "99496",
        "display": "Transitional care management services with high medical decision complexity",
        "text": "Transitional care management - high complexity",
        "system": "http://www.ama-assn.org/go/cpt"
    }
]

# Common procedure statuses
PROCEDURE_STATUSES = ["preparation", "in-progress", "not-done", "on-hold", "stopped", "completed", "entered-in-error", "unknown"]

# Common procedure categories
PROCEDURE_CATEGORIES = [
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/procedure-category",
                "code": "diagnostic",
                "display": "Diagnostic"
            }
        ],
        "text": "Diagnostic"
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/procedure-category",
                "code": "therapeutic",
                "display": "Therapeutic"
            }
        ],
        "text": "Therapeutic"
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/procedure-category",
                "code": "surgical",
                "display": "Surgical"
            }
        ],
        "text": "Surgical"
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/procedure-category",
                "code": "laboratory",
                "display": "Laboratory"
            }
        ],
        "text": "Laboratory"
    }
]
