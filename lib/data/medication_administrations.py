"""
Common medication administration data for FHIR MedicationAdministration resources.
Includes medications, routes, methods, and administration details.
"""

# Medication administration statuses
MEDICATION_ADMINISTRATION_STATUSES = [
    "in-progress",
    "not-done",
    "on-hold",
    "completed",
    "entered-in-error",
    "stopped",
    "unknown"
]

# Common medications for administration (NDC codes)
# TODO: VERIFY THESE...
MEDICATIONS = [
    {
        "code": "0409-6531-02",
        "display": "Vancomycin Hydrochloride (VANCOMYCIN HYDROCHLORIDE)",
        "text": "Vancomycin",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7501-01",
        "display": "Morphine Sulfate (MORPHINE SULFATE)",
        "text": "Morphine",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7502-01",
        "display": "Fentanyl Citrate (FENTANYL CITRATE)",
        "text": "Fentanyl",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7503-01",
        "display": "Lidocaine Hydrochloride (LIDOCAINE HYDROCHLORIDE)",
        "text": "Lidocaine",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7504-01",
        "display": "Dexamethasone Sodium Phosphate (DEXAMETHASONE SODIUM PHOSPHATE)",
        "text": "Dexamethasone",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7505-01",
        "display": "Ondansetron Hydrochloride (ONDANSETRON HYDROCHLORIDE)",
        "text": "Ondansetron",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7506-01",
        "display": "Metoclopramide Hydrochloride (METOCLOPRAMIDE HYDROCHLORIDE)",
        "text": "Metoclopramide",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7507-01",
        "display": "Dopamine Hydrochloride (DOPAMINE HYDROCHLORIDE)",
        "text": "Dopamine",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7508-01",
        "display": "Norepinephrine Bitartrate (NOREPINEPHRINE BITARTRATE)",
        "text": "Norepinephrine",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7509-01",
        "display": "Epinephrine (EPINEPHRINE)",
        "text": "Epinephrine",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7510-01",
        "display": "Atropine Sulfate (ATROPINE SULFATE)",
        "text": "Atropine",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7511-01",
        "display": "Digoxin (DIGOXIN)",
        "text": "Digoxin",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7512-01",
        "display": "Furosemide (FUROSEMIDE)",
        "text": "Furosemide",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7513-01",
        "display": "Insulin Regular (INSULIN REGULAR)",
        "text": "Insulin Regular",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7514-01",
        "display": "Heparin Sodium (HEPARIN SODIUM)",
        "text": "Heparin",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7515-01",
        "display": "Warfarin Sodium (WARFARIN SODIUM)",
        "text": "Warfarin",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7516-01",
        "display": "Aspirin (ASPIRIN)",
        "text": "Aspirin",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7517-01",
        "display": "Acetaminophen (ACETAMINOPHEN)",
        "text": "Acetaminophen",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7518-01",
        "display": "Ibuprofen (IBUPROFEN)",
        "text": "Ibuprofen",
        "system": "http://hl7.org/fhir/sid/ndc"
    },
    {
        "code": "0002-7519-01",
        "display": "Prednisone (PREDNISONE)",
        "text": "Prednisone",
        "system": "http://hl7.org/fhir/sid/ndc"
    }
]

# Routes of administration (SNOMED CT codes)
# TODO: VERIFY THESE...
ADMINISTRATION_ROUTES = [
    {
        "code": "47625008",
        "display": "Intravenous route (qualifier value)",
        "text": "IV",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "78421000",
        "display": "Intramuscular route (qualifier value)",
        "text": "IM",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "26643006",
        "display": "Oral route (qualifier value)",
        "text": "PO",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "34206005",
        "display": "Subcutaneous route (qualifier value)",
        "text": "SC",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "46713006",
        "display": "Inhalation route (qualifier value)",
        "text": "Inhalation",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "54402000",
        "display": "Topical route (qualifier value)",
        "text": "Topical",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "372449004",
        "display": "Intranasal route (qualifier value)",
        "text": "Intranasal",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "372450004",
        "display": "Intraocular route (qualifier value)",
        "text": "Intraocular",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "372451000",
        "display": "Intra-articular route (qualifier value)",
        "text": "Intra-articular",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "372452007",
        "display": "Intrathecal route (qualifier value)",
        "text": "Intrathecal",
        "system": "http://snomed.info/sct"
    }
]

# Administration methods
ADMINISTRATION_METHODS = [
    "IV Push",
    "IV Infusion",
    "IV Bolus",
    "IM Injection",
    "SC Injection",
    "Oral Tablet",
    "Oral Liquid",
    "Oral Capsule",
    "Inhalation",
    "Topical Cream",
    "Topical Ointment",
    "Nasal Spray",
    "Eye Drops",
    "Ear Drops",
    "Sublingual",
    "Buccal",
    "Rectal Suppository",
    "Vaginal Suppository",
    "Transdermal Patch",
    "Intra-articular Injection"
]

# Reasons for medication administration
# TODO: VERIFY THESE...
ADMINISTRATION_REASONS = [
    {
        "code": "b",
        "display": "Given as Ordered",
        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given"
    },
    {
        "code": "a",
        "display": "Given as Alternative",
        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given"
    },
    {
        "code": "c",
        "display": "Given as Emergency",
        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given"
    },
    {
        "code": "d",
        "display": "Given as Required",
        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given"
    },
    {
        "code": "e",
        "display": "Given as Requested",
        "system": "http://terminology.hl7.org/CodeSystem/reason-medication-given"
    }
]

# Common dosage texts
DOSAGE_TEXTS = [
    "500mg IV q6h x 3 days",
    "10mg IM q4h PRN",
    "100mg PO q8h",
    "2.5mg SC q12h",
    "1 tablet PO q6h",
    "5ml PO q8h",
    "1 spray each nostril q12h",
    "2 drops each eye q6h",
    "1 patch q24h",
    "50mg IV push over 2 minutes",
    "1000mg IV infusion over 1 hour",
    "0.5mg IM stat",
    "2.5mg PO q4h PRN pain",
    "10mg SC q24h",
    "1 capsule PO q12h with food",
    "2.5ml PO q6h",
    "1 puff q4h PRN",
    "1 suppository PR q12h",
    "5mg IV q4h",
    "25mg PO q8h with meals"
]

# Common dose quantities
DOSE_QUANTITIES = [
    {"value": 500, "unit": "mg", "code": "mg"},
    {"value": 1000, "unit": "mg", "code": "mg"},
    {"value": 250, "unit": "mg", "code": "mg"},
    {"value": 50, "unit": "mg", "code": "mg"},
    {"value": 25, "unit": "mg", "code": "mg"},
    {"value": 10, "unit": "mg", "code": "mg"},
    {"value": 5, "unit": "mg", "code": "mg"},
    {"value": 2.5, "unit": "mg", "code": "mg"},
    {"value": 1, "unit": "mg", "code": "mg"},
    {"value": 0.5, "unit": "mg", "code": "mg"},
    {"value": 0.25, "unit": "mg", "code": "mg"},
    {"value": 0.1, "unit": "mg", "code": "mg"},
    {"value": 5, "unit": "ml", "code": "ml"},
    {"value": 10, "unit": "ml", "code": "ml"},
    {"value": 2.5, "unit": "ml", "code": "ml"},
    {"value": 1, "unit": "ml", "code": "ml"},
    {"value": 0.5, "unit": "ml", "code": "ml"},
    {"value": 2, "unit": "drops", "code": "drops"},
    {"value": 1, "unit": "tablet", "code": "tablet"},
    {"value": 1, "unit": "capsule", "code": "capsule"}
]

# Common administration notes
ADMINISTRATION_NOTES = [
    "Administered as ordered",
    "Patient tolerated well",
    "No adverse reactions",
    "Monitor for side effects",
    "Given with food",
    "Given on empty stomach",
    "Slow IV push over 2 minutes",
    "Monitor vital signs",
    "Patient education provided",
    "Allergy check completed",
    "Dose adjusted for weight",
    "Given with 100ml NS",
    "Flush line after administration",
    "Check blood pressure before",
    "Monitor blood glucose",
    "Given PRN for pain",
    "Patient refused previous dose",
    "Given as emergency medication",
    "Alternative medication used",
    "Dose held due to contraindication"
]

# Performer roles
PERFORMER_ROLES = [
    {
        "code": "AUT",
        "display": "author (originator)",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"
    },
    {
        "code": "INF",
        "display": "informant",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"
    },
    {
        "code": "VER",
        "display": "verifier",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"
    },
    {
        "code": "VRF",
        "display": "verifier",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"
    }
]

# Signature types
# TODO: VERIFY THESE...
SIGNATURE_TYPES = [
    {
        "code": "1.2.840.10065.1.12.1.1",
        "display": "Author's Signature",
        "system": "urn:iso-astm:E1762-95:2013"
    },
    {
        "code": "1.2.840.10065.1.12.1.2",
        "display": "Co-author's Signature",
        "system": "urn:iso-astm:E1762-95:2013"
    },
    {
        "code": "1.2.840.10065.1.12.1.3",
        "display": "Co-participant's Signature",
        "system": "urn:iso-astm:E1762-95:2013"
    }
]

# Common frequency patterns
FREQUENCY_PATTERNS = [
    "q6h",  # every 6 hours
    "q8h",  # every 8 hours
    "q12h", # every 12 hours
    "q24h", # every 24 hours
    "q4h",  # every 4 hours
    "q2h",  # every 2 hours
    "q1h",  # every hour
    "BID",  # twice daily
    "TID",  # three times daily
    "QID",  # four times daily
    "PRN",  # as needed
    "STAT", # immediately
    "q48h", # every 48 hours
    "q72h", # every 72 hours
    "weekly" # weekly
]
