"""
Common allergy intolerance data for FHIR AllergyIntolerance resources.
Includes allergens, categories, manifestations, and clinical details.
"""

# Clinical status codes
CLINICAL_STATUSES = [
    {
        "code": "active",
        "display": "Active",
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical"
    },
    {
        "code": "inactive",
        "display": "Inactive",
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical"
    },
    {
        "code": "resolved",
        "display": "Resolved",
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical"
    }
]

# Verification status codes
VERIFICATION_STATUSES = [
    {
        "code": "unconfirmed",
        "display": "Unconfirmed",
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification"
    },
    {
        "code": "confirmed",
        "display": "Confirmed",
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification"
    },
    {
        "code": "refuted",
        "display": "Refuted",
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification"
    },
    {
        "code": "entered-in-error",
        "display": "Entered in Error",
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification"
    }
]

# Allergy categories
ALLERGY_CATEGORIES = [
    "medication",
    "food",
    "environment",
    "biologic"
]

# Criticality levels
CRITICALITY_LEVELS = [
    "low",
    "high",
    "unable-to-assess"
]

# Common medication allergens (RxNorm codes)
# TODO: VERIFY THESE...
MEDICATION_ALLERGENS = [
    {
        "code": "7980",
        "display": "Penicillin G",
        "text": "Penicillin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7981",
        "display": "Penicillin V",
        "text": "Penicillin V",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7982",
        "display": "Ampicillin",
        "text": "Ampicillin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7983",
        "display": "Amoxicillin",
        "text": "Amoxicillin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7984",
        "display": "Cephalexin",
        "text": "Cephalexin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7985",
        "display": "Cefazolin",
        "text": "Cefazolin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7986",
        "display": "Sulfamethoxazole",
        "text": "Sulfamethoxazole",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7987",
        "display": "Trimethoprim",
        "text": "Trimethoprim",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7988",
        "display": "Vancomycin",
        "text": "Vancomycin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7989",
        "display": "Gentamicin",
        "text": "Gentamicin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7990",
        "display": "Tobramycin",
        "text": "Tobramycin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7991",
        "display": "Ciprofloxacin",
        "text": "Ciprofloxacin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7992",
        "display": "Levofloxacin",
        "text": "Levofloxacin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7993",
        "display": "Aspirin",
        "text": "Aspirin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7994",
        "display": "Ibuprofen",
        "text": "Ibuprofen",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7995",
        "display": "Naproxen",
        "text": "Naproxen",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7996",
        "display": "Acetaminophen",
        "text": "Acetaminophen",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7997",
        "display": "Morphine",
        "text": "Morphine",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7998",
        "display": "Codeine",
        "text": "Codeine",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    },
    {
        "code": "7999",
        "display": "Insulin",
        "text": "Insulin",
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm"
    }
]

# Common food allergens (SNOMED CT codes)
# TODO: VERIFY THESE...
FOOD_ALLERGENS = [
    {
        "code": "762952008",
        "display": "Food containing milk",
        "text": "Milk",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "762953003",
        "display": "Food containing egg",
        "text": "Eggs",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "762954009",
        "display": "Food containing peanut",
        "text": "Peanuts",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "762955005",
        "display": "Food containing tree nut",
        "text": "Tree Nuts",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "762956006",
        "display": "Food containing wheat",
        "text": "Wheat",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "762957002",
        "display": "Food containing soy",
        "text": "Soy",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "762958007",
        "display": "Food containing fish",
        "text": "Fish",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "762959004",
        "display": "Food containing shellfish",
        "text": "Shellfish",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "762960009",
        "display": "Food containing sesame",
        "text": "Sesame",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "762961008",
        "display": "Food containing sulfite",
        "text": "Sulfites",
        "system": "http://snomed.info/sct"
    }
]

# Common environmental allergens (SNOMED CT codes)
# TODO: VERIFY THESE...
ENVIRONMENTAL_ALLERGENS = [
    {
        "code": "256259004",
        "display": "Pollen",
        "text": "Pollen",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256260009",
        "display": "Dust mite",
        "text": "Dust Mites",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256261008",
        "display": "Animal dander",
        "text": "Animal Dander",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256262001",
        "display": "Mold",
        "text": "Mold",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256263006",
        "display": "Latex",
        "text": "Latex",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256264000",
        "display": "Bee sting",
        "text": "Bee Sting",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256265004",
        "display": "Wasp sting",
        "text": "Wasp Sting",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256266003",
        "display": "Grass",
        "text": "Grass",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256267007",
        "display": "Tree",
        "text": "Trees",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256268002",
        "display": "Weed",
        "text": "Weeds",
        "system": "http://snomed.info/sct"
    }
]

# Common biologic allergens (SNOMED CT codes)
# TODO: VERIFY THESE...
BIOLOGIC_ALLERGENS = [
    {
        "code": "256269005",
        "display": "Contrast media",
        "text": "Contrast Media",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256270006",
        "display": "Vaccine",
        "text": "Vaccines",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256271005",
        "display": "Blood product",
        "text": "Blood Products",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256272003",
        "display": "Plasma",
        "text": "Plasma",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "256273008",
        "display": "Serum",
        "text": "Serum",
        "system": "http://snomed.info/sct"
    }
]

# Common allergy manifestations (SNOMED CT codes)
# TODO: VERIFY THESE...
ALLERGY_MANIFESTATIONS = [
    {
        "code": "247472004",
        "display": "Hives",
        "text": "Hives",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247473009",
        "display": "Urticaria",
        "text": "Urticaria",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247474003",
        "display": "Angioedema",
        "text": "Angioedema",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247475002",
        "display": "Rash",
        "text": "Rash",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247476001",
        "display": "Pruritus",
        "text": "Itching",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247477005",
        "display": "Erythema",
        "text": "Redness",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247478000",
        "display": "Swelling",
        "text": "Swelling",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247479008",
        "display": "Nausea",
        "text": "Nausea",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247480006",
        "display": "Vomiting",
        "text": "Vomiting",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247481005",
        "display": "Diarrhea",
        "text": "Diarrhea",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247482003",
        "display": "Abdominal pain",
        "text": "Abdominal Pain",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247483008",
        "display": "Dyspnea",
        "text": "Shortness of Breath",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247484002",
        "display": "Wheezing",
        "text": "Wheezing",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247485001",
        "display": "Cough",
        "text": "Cough",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247486000",
        "display": "Chest tightness",
        "text": "Chest Tightness",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247487009",
        "display": "Anaphylaxis",
        "text": "Anaphylaxis",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247488004",
        "display": "Hypotension",
        "text": "Low Blood Pressure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247489007",
        "display": "Tachycardia",
        "text": "Rapid Heart Rate",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247490003",
        "display": "Dizziness",
        "text": "Dizziness",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "247491004",
        "display": "Syncope",
        "text": "Fainting",
        "system": "http://snomed.info/sct"
    }
]

# Participant function types
PARTICIPANT_FUNCTIONS = [
    {
        "code": "author",
        "display": "Author",
        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type"
    },
    {
        "code": "informant",
        "display": "Informant",
        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type"
    },
    {
        "code": "verifier",
        "display": "Verifier",
        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type"
    },
    {
        "code": "validator",
        "display": "Validator",
        "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type"
    }
]

# Common allergy notes
ALLERGY_NOTES = [
    "Patient reports severe reaction",
    "Confirmed by skin testing",
    "Confirmed by blood testing",
    "Patient reports mild reaction",
    "Family history of similar allergy",
    "Reaction occurred in childhood",
    "Reaction occurred in adulthood",
    "Patient carries epinephrine auto-injector",
    "Avoid all products containing this allergen",
    "Cross-reactivity with similar substances",
    "Reaction severity has increased over time",
    "Reaction severity has decreased over time",
    "No known reaction to similar substances",
    "Patient education provided",
    "Emergency action plan discussed"
]

# Common allergy onset descriptions
ONSET_DESCRIPTIONS = [
    "Immediate (within minutes)",
    "Rapid (within 1 hour)",
    "Delayed (1-24 hours)",
    "Late (24-72 hours)",
    "Unknown onset time",
    "Gradual onset over hours",
    "Sudden onset",
    "Progressive worsening",
    "Intermittent episodes",
    "Chronic ongoing"
]

# Common allergy severity descriptions
SEVERITY_DESCRIPTIONS = [
    "Mild",
    "Moderate",
    "Severe",
    "Life-threatening",
    "Unknown severity",
    "Mild to moderate",
    "Moderate to severe",
    "Severe to life-threatening"
]
